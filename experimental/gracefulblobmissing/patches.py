# -*- coding: utf-8 -*-

from os import fstat
from ZODB.POSException import POSKeyError
from plone.app.blob.utils import openBlob

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