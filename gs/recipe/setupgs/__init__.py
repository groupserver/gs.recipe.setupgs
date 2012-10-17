# -*- coding: utf-8 -*-
"""Recipe setupgs. Many thanks to the collective.recipe.updateplone authors
   :) """
import os
from subprocess import call
import sys
import tempfile


def quote_command(command):
    # Quote the program name, so it works even if it contains spaces
    command = " ".join(['"%s"' % x for x in command])
    if sys.platform[:3].lower() == 'win':
        # odd, but true: the windows cmd processor can't handle more than
        # one quoted item per string unless you add quotes around the
        # whole line.
        command = '"%s"' % command
    return command


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.fileName = os.path.join(self.buildout['buildout']['directory'],
                                     'var', "%s.cfg" % self.name)

        # suppress script generation
        self.options['scripts'] = ''
        options['bin-directory'] = buildout['buildout']['bin-directory']

    def should_run(self):
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
            with file(self.fileName, 'w') as lockfile:
                lockfile.write('1')

    def get_script(self):
        # The following assignments look like the are unused, but they are
        # utilised by the locals() magic below:
        #lint:disable
        f = os.path.dirname(__file__)
        recipe_egg_path = f[:-len(self.options['recipe'])].replace("\\", "/")
        zope_admin_name = self.options['zope_admin_name']
        zope_admin = self.options['zope_admin']
        instance_id = self.options['instance_id']
        instance_title = self.options['instance_title']
        gs_admin_email = self.options['gs_admin_email']
        gs_admin_password = self.options['gs_admin_password']
        gs_user_email = self.options['gs_user_email']
        gs_user_password = self.options['gs_user_password']
        gs_support_email = self.options['gs_support_email']
        gs_timezone = self.options['gs_timezone']
        gs_host = self.options['gs_host']
        gs_port = self.options['gs_port']
        gs_smtp_host = self.options['gs_smtp_host']
        gs_smtp_port = self.options['gs_smtp_port']
        gs_smtp_user = self.options['gs_smtp_user']
        gs_smtp_password = self.options['gs_smtp_password']
        database_host = self.options['database_host']
        database_port = self.options['database_port']
        database_admin = self.options['database_admin']
        database_username = self.options['database_username']
        database_password = self.options['database_password']
        database_name = self.options['database_name']
        #lint:enable

        templateFileName = os.path.join(os.path.dirname(__file__),
                                        'script.py_tmpl').replace("\\", "/")
        with file(templateFileName, 'r') as infile:
            template = infile.read()
        template = template % locals()  # Magic

        retval = tempfile.mktemp().replace("\\", "/")
        with file(retval, 'w') as outfile:
            outfile.write(template)
        return retval

    def install(self):
        """Installer"""
        if self.should_run():
            installScript = self.get_script()
            binDir = self.buildout['buildout']['bin-directory']
            instanceCommand = os.path.join(binDir, 'instance')
            command = quote_command([instanceCommand, "run", installScript])
            try:
                retcode = call(command, shell=True)
                if retcode == 0:
                    self.mark_locked()
                    sys.stdout.write('GroupServer site created\n\n')
                else:
                    m = '%s: Issue running\n\t%s\nReturned %s\n' %\
                        (self.name, command, retcode)
                    sys.stderr.write(m)
                    sys.exit(1)
            except OSError, e:
                m = '%s: Failed to run\n\t%s\n%s\n' % (self.name, command, e)
                sys.stderr.write(m)
                sys.exit(1)

        return tuple()

    def update(self):
        """Updater"""
        self.install()
