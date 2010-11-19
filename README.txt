Introduction
============

The `BLOB support in Plone`__ is amazing for a lot of reasons.

__ http://pypi.python.org/pypi/plone.app.blob

A minor reason I like is that: the *Data.fs* now is very little, and you can take it from
customers server quickly, or deploying it for staging purpose without taking also all attachments
that commonly only matters on production.

However, right now, Plone will raise errors when you visit a file content that use BLOB support,
without having also the BLOB file.

I don't know if this is good or not (I opened `an issue`__ relaed to this), but for developers this
can be a little boring.

__ http://dev.plone.org/plone/ticket/11293

This product will simply monkey-pach a pair of points in Plone, so visiting a ATFile without its
BLOB available will not show any errors to visitors.

Requirements
------------

This product has been tested on:
* Plone 3.3 (with plone.app.blob 1.3)
* Plone 4.0

Warning
-------

This is designed only for **development/staging** environment. Do not use in production if you are
not sure of what you are doing!

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/

