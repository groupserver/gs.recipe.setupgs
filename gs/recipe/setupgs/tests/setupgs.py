# -*- coding: utf-8 -*-
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
