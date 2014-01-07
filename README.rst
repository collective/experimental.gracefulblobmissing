.. contents::

How to use
==========

The `BLOB support in Plone`__ is amazing for a lot of reasons.

__ http://pypi.python.org/pypi/plone.app.blob

However, right now, Plone will raise errors when you visit a file content that use BLOB support,
without having also the BLOB file.

I don't know if this is good or not (I opened `an issue`__ related to this), but for developers this
can be a little boring. It's quite common to copy a production ``Data.fs`` for developing something
using production data, but you don't always want to copy all blobs.

__ http://dev.plone.org/plone/ticket/11293

This product monkey-patches some points inside Plone, so visiting objects that store content in blob-Fields (like ATFile/ATImage) without its BLOB available will not show any errors to visitors. Instead a file only containing the string "File created by experimental.gracefulblobmissing." is created in the place where the blob-file should be.


Catalog
-------

This product also patches the ``SearchableText`` Archetypes method, so you can reindex
you catalog without errors.

Requirements
============

This product has been tested on:

* Plone 4.0
* Plone 4.1
* Plone 4.2
* Plone 4.3

For Plone 3 compatiblity, look stay on version 0.3.0 or lower.

Warning
=======

This is designed only for **development/staging** environment. *Do not use in production* if you are
not 100% sure of what you are doing!

Credits
=======

Developed with the support of `S. Anna Hospital, Ferrara`__; S. Anna Hospital supports the
`PloneGov initiative`__.

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

