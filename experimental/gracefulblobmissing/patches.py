# -*- coding: utf-8 -*-

from os import fstat
import os.path
from ZODB.POSException import POSKeyError

from Products.CMFCore.utils import getToolByName

from plone.app.blob.utils import openBlob
from plone.app.imaging.interfaces import IImageScaleHandler

def patched_field_get_size(self):
    try:
        blob = openBlob(self.blob)
        size = fstat(blob.fileno()).st_size
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
        RESPONSE.redirect(instance.absolute_url()+'/view')

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
