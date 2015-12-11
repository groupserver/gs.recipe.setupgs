# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from mock import patch, MagicMock  # lint:ok
from unittest import TestCase
#from OFS.Application import Application
import gs.recipe.setupgs.setupgs


class TestSetupGS(TestCase):
    def setUp(self):
        gs.recipe.setupgs.setupgs.creation.manage_addGroupserverSite = \
            MagicMock()

    def assertHasAttr(self, obj, attr):
        msg = '{0} does not have an attribute {1}'.format(obj, attr)
        self.assertTrue(hasattr(obj, attr), msg)

    def test_create_site(self):
        'Test a call to SetupGS.create_site that has no errors.'
        # FIXME: learn more about ``mock.patch``, and test
        # ``gs.recipe.setupgs.setupgs.SetupGS.test create_site``.
