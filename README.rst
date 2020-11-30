.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================
Base Geocoder Extender
======================

    This module exted the base_geocoder functionality:

    Extending: _get_provider -> become multi company

    Extending: geo_find

    Adding: reverse_geo_find (lat,lon) => address

Configuration
-------------
    Map settings go to company. If empty using default logic

Usage
-----
Add base.geocoder as mixin in your model

Use geo_find and reverse_geo_find in your code

Wish list
---------
Map view

Contributors
------------

Polimex Holding Development team

Maintainer
----------

.. image:: https://portal.polimex.co/logo.png
   :alt: Polimex Logo
   :target: https://polimex.co

This module is created and maintained by the Polimex.
