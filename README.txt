=====================
``gs.recipe.setupgs``
=====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A ``zc.buildout`` recipe for setting up a GroupServer instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-04-22
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

This product supplies a ``zc_buildout`` recipe [#buildout]_ for installing
a GroupServer site in a Zope instance. It does the following.

#. Generates a script based on the configuration_.
#. Runs the script with the correct python environment for
   Zope (the ``instancepython``).
#. This script then sets up GroupServer by calling code in
   ``Products.GroupServer`` [#pgs]_.

Configuration
=============

The options for this recipe are specified in the ``confg.cfg`` file, and
are marshalled by the ``instance.cfg`` configuration file.

Acknowledgements
================

Many thanks to the ``collective.recipe.updateplone`` [#update]_ authors for
inspiring this product.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.recipe.setupgs
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#buildout] See <https://pypi.python.org/pypi/zc.buildout/2.2.1>
.. [#update] See <https://pypi.python.org/pypi/collective.recipe.updateplone/0.3>
.. [#pgs] See <https://source.iopen.net/groupserver/Products.GroupServer>
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
