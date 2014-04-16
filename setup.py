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
"""
This module contains the tool of gs.recipe.setupgs
"""
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

long_description = (
    file('README.txt').read()
    + '\n' +
    file(os.path.join('docs', 'CONTRIBUTORS.txt')).read()
    + '\n' +
    file(os.path.join('docs', 'CHANGES.txt')).read()
    + '\n'
    )
entry_point = 'gs.recipe.setupgs:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['zope.testing', 'zc.buildout']

setup(name='gs.recipe.setupgs',
      version=version,
      description="Setup GroupServer instance in Zope",
      long_description=long_description,
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        "Development Status :: 4 - Beta",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python",
        ],
      keywords='zope groupserver recipe setup instance',
      author='Richard Waid',
      author_email='richard@onlinegroups.net',
      url='',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zc.buildout',
        'AccessControl',
        'gs.group.member.invite.base',
        'gs.group.member.request',
        'gs.group.messages.post',
        'gs.group.messages.topic',
        'gs.option',
        'gs.profile.email.base',
        'gs.profile.email.verify',
        'gs.profile.password',
        'Products.CustomUserFolder',
        'Products.GroupServer',
        'Products.GSAuditTrail',
        'Products.GSGroupMember',
        'Products.XWFMailingListManager',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='gs.recipe.setupgs.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
