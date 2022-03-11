Changelog
=========

1.0 (2022-03-11)
----------------

- Add support for relstorage.
  [pbauer]

- Create dummy image blobs on the fly.
  [ale-rt, mauritsvanrees]


0.5.0 (2018-12-14)
------------------

- Only patch plone.app.blob and Products.ATContentTypes if they are installed.
  This makes this package compatible with a Archetypes-free Plone.
  [gforcada]

0.4.0 (2015-04-29)
------------------

* modify patch to not touch every file but only create file with a string in it when it is missing [pbauer]
* patch ZEO to create missing blob-files [pbauer]
* add logging-message when creating a missing blog-file [pbauer]
* fixed errors when reindexing SearchbleText index [keul]
* Added a patch for ZODB egg that Create the blob folder path and create (touch)
  an empty file for each blob file if it's missing. [sneridagh]

0.3.0 (2011-09-30)
------------------

* fixed dependency on ``collective.monkeypatcher`` >= 1.0 [keul]
* pached also getScale method, used by some atct views [keul]

0.2.0 (2011-06-06)
------------------

* fixed dependencies [keul]
* direct access to files with missing blobs
  now redirect to the view with a warning [keul]

0.1.0 (2010-11-19)
------------------

* initial release
