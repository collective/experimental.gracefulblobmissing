# -*- coding: utf-8 -*-
from pkg_resources import resource_filename
from shutil import copyfile
from ZEO import ClientStorage
from ZODB.blob import BlobFile
from ZODB.POSException import POSKeyError
from ZODB.POSException import Unsupported

import logging
import os


logger = logging.getLogger(__name__)


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


def patched_loadBlob_relstorage(self, cursor, oid, serial):
    # Load a blob.  If it isn't present and we have a shared blob
    # directory, then assume that it doesn't exist on the server
    # and return None.
    from relstorage.blobhelper import _accessed
    from relstorage.blobhelper import _lock_blob

    blob_filename = self.fshelper.getBlobFilename(oid, serial)
    if self.shared_blob_dir:
        if os.path.exists(blob_filename):
            return blob_filename
        else:
            # All the blobs are in a shared directory.  If the
            # file isn't here, it's not anywhere.
            # Here is the patch!
            # raise POSException.POSKeyError("No blob file", oid, serial)
            create_empty_blob(blob_filename)

    if os.path.exists(blob_filename):
        return _accessed(blob_filename)

    # First, we'll create the directory for this oid, if it doesn't exist.
    self.fshelper.getPathForOID(oid, create=True)

    # OK, it's not here and we (or someone) needs to get it.  We
    # want to avoid getting it multiple times.  We want to avoid
    # getting it multiple times even accross separate client
    # processes on the same machine. We'll use file locking.

    lock = _lock_blob(blob_filename)
    try:
        # We got the lock, so it's our job to download it.  First,
        # we'll double check that someone didn't download it while we
        # were getting the lock:

        if os.path.exists(blob_filename):
            return _accessed(blob_filename)

        self.download_blob(cursor, oid, serial, blob_filename)

        if os.path.exists(blob_filename):
            return _accessed(blob_filename)

        # We still raise the error here because if the blob is not in the
        # relstorage-DB something is wrong
        raise POSKeyError("No blob file", oid, serial)

    finally:
        lock.close()


def create_empty_blob(filename):
    dirname = os.path.split(filename)[0]
    if not os.path.isdir(dirname):
        os.makedirs(dirname, 0o700)

    source = resource_filename(
        'experimental.gracefulblobmissing',
        'dummies/blob.png',
    )

    copyfile(source, filename)
    logger.info("Created blob-file for missing %s", filename)
