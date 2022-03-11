.. contents::

How to use
==========

The `BLOB support in Plone`__ is amazing for a lot of reasons.

__ https://pypi.org/project/plone.app.blob

However Plone will raise errors when you visit a file content that use BLOB support without also having the BLOB file.

For developers this can be a little bit boring.
It's quite common to copy a production ``Data.fs`` for developing using production data, but you don't always want to copy all blobs.

This product monkey-patches parts of Plone, so that visiting objects that store content in the blob storage without having the BLOB available will not lead to errors.
Instead a file only containing the string "File created by experimental.gracefulblobmissing." is created in the place where the blob-file should be.


Catalog
-------

This product also patches the ``SearchableText`` Archetypes method, so you can reindex you catalog without errors.


Requirements
============

This product has been tested on:

* Plone 4.0
* Plone 4.1
* Plone 4.2
* Plone 4.3
* Plone 5.0
* Plone 5.1
* Plone 5.2

For Plone 3 compatiblity stay on version 0.3.0 or lower.


Warning
=======

This is designed only for **development/staging** environment. *Do not use in production* if you are not 100% sure of what you are doing!


Credits
=======

Developed with the support of `S. Anna Hospital, Ferrara`__; S. Anna Hospital supports the `PloneGov initiative`__.

.. image:: http://www.ospfe.it/ospfe-logo.jpg
   :alt: OspFE logo

__ http://www.ospfe.it/
__ http://www.plonegov.it/


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/

