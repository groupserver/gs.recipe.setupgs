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
import codecs
import os
from string import Template
import subprocess
import sys
import tempfile
from zc.buildout import UserError
from gs.recipe.base import Recipe
UTF8 = 'utf-8'


class SetupGSRecipe(Recipe):
    """zc.buildout recipe to set up GroupServer"""

    def create_script(self):
        f = os.path.dirname(__file__)
        mapping = {
            'recipe_egg_path':
                f[:-len(self.options['recipe'])].replace("\\", "/"),
            'zope_admin_name': self.options['zope_admin_name'],
            'instance_id': self.options['instance_id'],
            'instance_title': self.options['instance_title'],
            'support_email': self.options['support_email'],
            'gs_admin_email': self.options['gs_admin_email'],
            'gs_admin_password': self.options['gs_admin_password'],
            'gs_host': self.options['gs_host'],
            'gs_port': self.options['gs_port'],
            'gs_smtp_host': self.options['gs_smtp_host'],
            'gs_smtp_port': self.options['gs_smtp_port'],
            'gs_smtp_user': self.options['gs_smtp_user'],
            'gs_smtp_password': self.options['gs_smtp_password'],
        }
        templateFileName = os.path.join(os.path.dirname(__file__),
                                        'script.py_tmpl').replace("\\", "/")
        with codecs.open(templateFileName, 'r', UTF8) as infile:
            templateText = infile.read()
        template = Template(templateText)
        retval = template.substitute(mapping)
        return retval

    @staticmethod
    def write_script(scriptText):
        filename = tempfile.mktemp().replace("\\", "/")
        with codecs.open(filename, 'w', UTF8) as outfile:
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
