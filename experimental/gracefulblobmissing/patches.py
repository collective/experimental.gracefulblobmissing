# -*- coding: utf-8 -*-

from plone.app.blob.utils import openBlob
from plone.app.imaging.interfaces import IImageScaleHandler
from Products.CMFCore.utils import getToolByName
from sh import mkdir
from ZEO import ClientStorage
from ZODB.blob import BlobFile
from ZODB.POSException import POSKeyError, ConflictError, Unsupported

import logging
import os

logger = logging.getLogger(__name__)


def patched_field_get_size(self):
    try:
        blob = openBlob(self.blob)
        size = os.fstat(blob.fileno()).st_size
        blob.close()
    except POSKeyError:
        size = 0
    return size


def patched_class_get_size(self):
    f = self.getPrimaryField()
    if f is None:
        return 0
    try:
        return f.get_size(self) or 0
    except POSKeyError:
        return 0


def patched_field_index_html(self, instance, REQUEST=None, RESPONSE=None, disposition='inline'):
    try:
        blob = self._old_index_html(instance, REQUEST=REQUEST, RESPONSE=RESPONSE, disposition=disposition)
        if blob:
            return blob
        raise POSKeyError()
    except POSKeyError:
        if not RESPONSE:
            RESPONSE = instance.REQUEST.RESPONSE
        putils = getToolByName(instance, 'plone_utils')
        putils.addPortalMessage('Missing BLOB file for %s' % instance.absolute_url_path(), type='warning')
        RESPONSE.redirect(instance.absolute_url() + '/view')


def patched_getScale(self, instance, scale=None, **kwargs):
    if scale is None:
        return self.getUnwrapped(instance, **kwargs)
    handler = IImageScaleHandler(self, None)
    if handler is not None:
        try:
            return handler.getScale(instance, scale)
        except POSKeyError:
            pass
    return None


def patched_SearchableText(self):
    data = []
    charset = self.getCharset()
    for field in self.Schema().fields():
        if not field.searchable:
            continue
        method = field.getIndexAccessor(self)
        try:
            datum = method(mimetype="text/plain")
        except TypeError:
            # Retry in case typeerror was raised because accessor doesn't
            # handle the mimetype argument
            try:
                datum = method()
            except (ConflictError, KeyboardInterrupt):
                raise
            except:
                continue
        except POSKeyError:
            datum = ''
        if datum:
            vocab = field.Vocabulary(self)
            if isinstance(datum, list) or isinstance(datum, tuple):
                # Unmangle vocabulary: we index key AND value
                vocab_values = map(lambda value, vocab=vocab: vocab.getValue(value, ''), datum)
                datum = list(datum)
                datum.extend(vocab_values)
                datum = ' '.join(datum)
            elif isinstance(datum, basestring):
                if isinstance(datum, unicode):
                    datum = datum.encode(charset)
                value = vocab.getValue(datum, '')
                if isinstance(value, unicode):
                    value = value.encode(charset)
                datum = "%s %s" % (datum, value, )

            if isinstance(datum, unicode):
                datum = datum.encode(charset)
            data.append(str(datum))

    data = ' '.join(data)
    return data


def patched_blob_init(self, name, mode, blob):
    if not os.path.exists(name):
        create_empty_blob(name)
    super(BlobFile, self).__init__(name, mode + 'b')
    self.blob = blob


def patched_loadBlob(self, oid, serial):
    # Load a blob.  If it isn't present and we have a shared blob
    # directory, then assume that it doesn't exist on the server
    # and return None.

    if self.fshelper is None:
        raise Unsupported("No blob cache directory is configured.")

    blob_filename = self.fshelper.getBlobFilename(oid, serial)
    if self.shared_blob_dir:
        if os.path.exists(blob_filename):
            return blob_filename
        else:
            # create empty file
            create_empty_blob(blob_filename)
        if os.path.exists(blob_filename):
            return blob_filename
        else:
            # We're using a server shared cache.  If the file isn't
            # here, it's not anywhere.
            raise POSKeyError("No blob file", oid, serial)

    if os.path.exists(blob_filename):
        return ClientStorage._accessed(blob_filename)
    else:
        # create empty file
        create_empty_blob(blob_filename)

    if os.path.exists(blob_filename):
        return ClientStorage._accessed(blob_filename)

    # First, we'll create the directory for this oid, if it doesn't exist.
    self.fshelper.createPathForOID(oid)

    # OK, it's not here and we (or someone) needs to get it.  We
    # want to avoid getting it multiple times.  We want to avoid
    # getting it multiple times even accross separate client
    # processes on the same machine. We'll use file locking.

    lock = ClientStorage._lock_blob(blob_filename)
    try:
        # We got the lock, so it's our job to download it.  First,
        # we'll double check that someone didn't download it while we
        # were getting the lock:

        if os.path.exists(blob_filename):
            return ClientStorage._accessed(blob_filename)

        # Ask the server to send it to us.  When this function
        # returns, it will have been sent. (The recieving will
        # have been handled by the asyncore thread.)

        self._server.sendBlob(oid, serial)

        if os.path.exists(blob_filename):
            return ClientStorage._accessed(blob_filename)

        raise POSKeyError("No blob file", oid, serial)

    finally:
        lock.close()


def patched_loadBlob_zodb(self, oid, serial):
    """Return the filename where the blob file can be found.
    """
    filename = self.fshelper.getBlobFilename(oid, serial)
    if not os.path.exists(filename):
        create_empty_blob(filename)
    return filename


def create_empty_blob(filename):
    mkdir("-p", '/'.join(filename.split('/')[:-1]))
    fo = open(filename, 'w')
    fo.write("File created by experimental.gracefulblobmissing.")
    fo.close()
    logger.info("Created missing blob-file %s" % filename)
