# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2009, 2010, 2011, 2012, 2013, 2014 OnlineGroups.net and
# Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Recipe setupgs. Many thanks to the collective.recipe.updateplone authors
   :) """
import os
from string import Template
import subprocess
import sys
import tempfile
from zc.buildout import UserError


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.fileName = os.path.join(self.buildout['buildout']['directory'],
                                     'var', "%s.cfg" % self.name)

        # suppress script generation
        self.options['scripts'] = ''
        options['bin-directory'] = buildout['buildout']['bin-directory']

    def should_run(self):
        '''Returns True if the recipe should be run. By setting the
        "run-once" option to false, off, or no then the recipe will always be
        run.'''
        runonce = ((('run-once' in self.options)
                    and self.options['run-once'].lower()) or 'true')
        #We'll use the existance of this file as flag for the run-once option
        retval = True  # Uncharactistic optomisim

        if runonce not in ['false', 'off', 'no']:
            if os.path.exists(self.fileName):
                m = '''
*********************************************************************
Skipped: The setup script %s has already been run. If you want
to run it again set the run-once option to false or delete
%s
*********************************************************************\n\n''' %\
                    (self.name, self.fileName)
                sys.stdout.write(m)
                retval = False
        return retval

    def mark_locked(self):
        with open(self.fileName, 'w') as lockfile:
            lockfile.write('1')

    def create_script(self):
        f = os.path.dirname(__file__)
        mapping = {
            'recipe_egg_path':
                f[:-len(self.options['recipe'])].replace("\\", "/"),
            'zope_admin_name': self.options['zope_admin_name'],
            'zope_admin': self.options['zope_admin'],
            'instance_id': self.options['instance_id'],
            'instance_title': self.options['instance_title'],
            'gs_admin_email': self.options['gs_admin_email'],
            'gs_admin_password': self.options['gs_admin_password'],
            'gs_timezone': self.options['gs_timezone'],
            'gs_host': self.options['gs_host'],
            'gs_port': self.options['gs_port'],
            'gs_smtp_host': self.options['gs_smtp_host'],
            'gs_smtp_port': self.options['gs_smtp_port'],
            'gs_smtp_user': self.options['gs_smtp_user'],
            'gs_smtp_password': self.options['gs_smtp_password'],
            'database_host': self.options['database_host'],
            'database_port': self.options['database_port'],
            'database_admin': self.options['database_admin'],
            'database_username': self.options['database_username'],
            'database_password': self.options['database_password'],
            'database_name': self.options['database_name'],
        }
        templateFileName = os.path.join(os.path.dirname(__file__),
                                        'script.py_tmpl').replace("\\", "/")
        with open(templateFileName, 'r') as infile:
            templateText = infile.read()
        template = Template(templateText)
        retval = template.substitute(mapping)
        return retval

    @staticmethod
    def write_script(scriptText):
        filename = tempfile.mktemp().replace("\\", "/")
        with open(filename, 'w') as outfile:
            outfile.write(scriptText)
        return filename

    def get_script(self):
        scriptText = self.create_script()
        filename = self.write_script(scriptText)
        return filename

    @staticmethod
    def quote_command(command):
        '''Quote the script command represented by the list "command"'''
        if type(command) not in (list, tuple):
            msg = 'Expected a tuple or list, got a "{0}".'.format(type(command))
            raise TypeError(msg)
        # Quote the program name, so it works even if it contains spaces
        command = " ".join(['"%s"' % x for x in command])
        if sys.platform[:3].lower() == 'win':
            # odd, but true: the windows cmd processor can't handle more than
            # one quoted item per string unless you add quotes around the
            # whole line.
            command = '"%s"' % command
        return command

    def get_script_command(self, ):
        binDir = self.buildout['buildout']['bin-directory']
        instanceCommand = os.path.join(binDir, 'instance')
        installScript = self.get_script()
        c = [instanceCommand, "run", installScript]
        retval = self.quote_command(c)
        return retval

    def install(self):
        """Installer"""
        if self.should_run():
            command = self.get_script_command()
            try:
                retcode = subprocess.call(command, shell=True)
                if retcode == 0:
                    self.mark_locked()
                    sys.stdout.write('GroupServer site created\n\n')
                else:
                    m = '%s: Issue running\n\t%s\nReturned %s\n' %\
                        (self.name, command, retcode)
                    raise UserError(m)
            except OSError as e:
                m = '%s: Failed to run\n\t%s\n%s\n' % (self.name, command, e)
                raise UserError(m)

        return tuple()

    def update(self):
        """Updater"""
        self.install()
