# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from os import mkdir
from os.path import exists
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase, main as unittest_main
from gs.recipe.setupgs import Recipe


class TestScriptCreation(TestCase):
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
        self.options['zope_admin'] = 'parannah'
        self.options['instance_id'] = 'ethyl_the_frog'
        self.options['instance_title'] = 'violence'
        self.options['gs_admin_email'] = 'durk@example.com'
        self.options['gs_admin_password'] = 'toad the wet sprocket'
        self.options['gs_timezone'] = 'UTC'
        self.options['gs_host'] = 'groups.example.com'
        self.options['gs_port'] = '42'
        self.options['gs_smtp_host'] = 'smtp.example.com'
        self.options['gs_smtp_port'] = '42'
        self.options['gs_smtp_user'] = ''
        self.options['gs_smtp_password'] = ''
        self.options['database_host'] = 'localhost'
        self.options['database_port'] = '8432'
        self.options['database_admin'] = 'dinsdale'
        self.options['database_username'] = 'ethyl_the_frog'
        self.options['database_password'] = 'toad the wet sprocket'
        self.options['database_name'] = 'ethyl_the_frog'
        self.recipe = Recipe(self.buildout, self.name, self.options)

    def tearDown(self):
        rmtree(self.tempdir)

    def should_run_false_options(self, val):
        '''Test if seting the "run-opnce" option to false always causes
        the should_run method to return True.'''
        self.recipe.options = {'run-once': val}
        with open(self.recipe.fileName, 'w') as togglefile:
            togglefile.write(b'1')
        r = self.recipe.should_run()
        self.assertTrue(r)

    def test_should_run_false(self):
        self.should_run_false_options('false')
        self.should_run_false_options('False')

    def test_should_run_no(self):
        self.should_run_false_options('no')
        self.should_run_false_options('No')

    def test_should_run_off(self):
        self.should_run_false_options('off')
        self.should_run_false_options('Off')

    def test_should_run_no_file(self):
        '''Test if should_run returns True if there is no toggle-file'''
        r = self.recipe.should_run()
        self.assertTrue(r)

    def test_should_run_file(self):
        '''Test if should_run returns False if there is a toggle-file'''
        with open(self.recipe.fileName, 'w') as togglefile:
            togglefile.write(b'1')
        r = self.recipe.should_run()
        self.assertFalse(r)

    def test_quote_command(self):
        c = 'I am a fish'.split()
        expected = '"I" "am" "a" "fish"'
        r = self.recipe.quote_command(c)
        self.assertEqual(expected, r)

    def test_mark_locked(self):
        self.recipe.mark_locked()
        r = exists(self.recipe.fileName)
        self.assertTrue(r)

    def test_create_script(self):
        r = self.recipe.create_script()
        expected = '# -*- coding: utf-8 -*-'
        self.assertEqual(expected, r[:23])

    def test_create_script_options(self):
        r = self.recipe.create_script()
        self.assertIn('example.com', r)
        self.assertIn('SetupGS', r)

    def test_write_script(self):
        outText = 'I am a fish'
        filename = self.recipe.write_script(outText)
        with open(filename, 'r') as infile:
            inText = infile.read()
        self.assertEqual(outText, inText)

    def test_get_script(self):
        filename = self.recipe.get_script()
        with open(filename, 'r') as infile:
            inText = infile.read()
        expected = '# -*- coding: utf-8 -*-'
        self.assertEqual(expected, inText[:23])

    def test_get_script_command(self):
        r = self.recipe.get_script_command()
        self.assertIn('instance', r)
        self.assertIn('run', r)
        self.assertIn(self.tempdir, r)

if __name__ == '__main__':
    unittest_main()
