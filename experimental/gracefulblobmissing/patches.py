# -*- coding: utf-8 -*-

from os import fstat
import os.path
from ZODB.POSException import POSKeyError
from plone.app.blob.utils import openBlob
from Products.CMFCore.utils import getToolByName

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
        putils.addPortalMessage('BLOB file is missing', type='warning')
        RESPONSE.redirect(instance.absolute_url()+'/view')


