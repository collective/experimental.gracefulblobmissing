Introduction
============

The `BLOB support in Plone`__ is amazing for a lot of reasons.

__ http://pypi.python.org/pypi/plone.app.blob

However, right now, Plone will raise errors when you visit a file content that use BLOB support,
without having also the BLOB file.

I don't know if this is good or not (I opened `an issue`__ related to this), but for developers this
can be a little boring. It's quite common to copy a production ``Data.fs`` for developing something
using production data, but you don't always want to copy all blobs.

__ http://dev.plone.org/plone/ticket/11293

This product will simply monkey-pach some points inside Plone, so visiting a ATFile/ATImage without its
BLOB available will not show any errors to visitors.

Requirements
------------

This product has been tested on:

* Plone 3.3 (with plone.app.blob 1.5)
* Plone 4.0
* Plone 4.1

Warning
-------

This is designed only for **development/staging** environment. *Do not use in production* if you are
not sure of what you are doing!

Credits
=======

Developed with the support of `S. Anna Hospital, Ferrara`__; S. Anna Hospital supports the
`PloneGov initiative`__.

__ http://www.ospfe.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

