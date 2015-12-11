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
import codecs
from os import mkdir
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase, main as unittest_main
from mock import MagicMock, patch
import zc.buildout
import gs.recipe.setupgs.recipe
from gs.recipe.setupgs.recipe import SetupGSRecipe
UTF8 = 'utf-8'


class TestScriptCreation(TestCase):
    'Test the creation of the script.'

    def setUp(self):
        self.tempdir = mkdtemp()
        self.bindir = '{0}/bin'.format(self.tempdir)
        mkdir(self.bindir)
        vardir = '{0}/var'.format(self.tempdir)
        mkdir(vardir)

        self.buildout = {'buildout': {'directory': self.tempdir,
                                        'bin-directory': self.bindir, }, }
        self.name = 'setupgs'
        self.options = {}
        self.options['recipe'] = 'gs.recipe.setupgs'
        self.options['zope_admin_name'] = 'durk'
        self.options['instance_id'] = 'ethyl_the_frog'
        self.options['instance_title'] = 'violence'
        self.options['gs_support_email'] = 'support@example.com'
        self.options['gs_admin_email'] = 'durk@example.com'
        self.options['gs_admin_password'] = 'toad the wet sprocket'
        self.options['gs_timezone'] = 'UTC'
        self.options['gs_host'] = 'groups.example.com'
        self.options['gs_port'] = '42'
        self.options['gs_smtp_host'] = 'smtp.example.com'
        self.options['gs_smtp_port'] = '42'
        self.options['gs_smtp_user'] = ''
        self.options['gs_smtp_password'] = ''
        self.recipe = SetupGSRecipe(self.buildout, self.name, self.options)

    def tearDown(self):
        rmtree(self.tempdir)

    def test_quote_command(self):
        'Test the quote_command function.'
        c = 'I am a fish'.split()
        expected = '"I" "am" "a" "fish"'
        r = self.recipe.quote_command(c)
        self.assertEqual(expected, r)

    def test_create_script(self):
        'Test the creation of a script.'
        r = self.recipe.create_script()
        expected = '# -*- coding: utf-8 -*-'
        self.assertEqual(expected, r[:23])

    def test_create_script_options(self):
        'Test if some of the options are in the script.'
        r = self.recipe.create_script()
        self.assertIn('example.com', r)
        self.assertIn('SetupGS', r)

    def test_write_script(self):
        'Test if the write_script function works.'
        outText = 'I am a fish'
        filename = self.recipe.write_script(outText)
        with codecs.open(filename, 'r', UTF8) as infile:
            inText = infile.read()
        self.assertEqual(outText, inText)

    def test_get_script(self):
        'Test the get_script functiom.'
        filename = self.recipe.get_script()
        with codecs.open(filename, 'r', UTF8) as infile:
            inText = infile.read()
        expected = '# -*- coding: utf-8 -*-'
        self.assertEqual(expected, inText[:23])

    def test_get_script_command(self):
        'Test the get_script_command function'
        r = self.recipe.get_script_command()
        self.assertIn('instance', r)
        self.assertIn('run', r)
        self.assertIn(self.tempdir, r)

    def test_install_success(self):
        'Test if we get a 0 if the install function works.'
        # Note that 0 is success for a command in the Unix shell
        gs.recipe.setupgs.recipe.subprocess.call = MagicMock(return_value=0)
        with patch('gs.recipe.setupgs.recipe.sys.stdout'):
            t = self.recipe.install()
        self.assertEqual(1, gs.recipe.setupgs.recipe.subprocess.call.call_count)
        args, kw_args = gs.recipe.setupgs.recipe.subprocess.call.call_args
        self.assertIn('instance', args[0])
        self.assertEqual(t, tuple())

    def test_install_fail(self):
        'Test that we get a UserError is raised if the install function fails.'
        # Note that 1 is failure for a command in the Unix shell
        gs.recipe.setupgs.recipe.sys.exit = MagicMock()
        gs.recipe.setupgs.recipe.subprocess.call = MagicMock(return_value=1)
        self.assertRaises(zc.buildout.UserError, self.recipe.install)
        self.assertEqual(1, gs.recipe.setupgs.recipe.subprocess.call.call_count)

if __name__ == '__main__':
    unittest_main()
