# -*- coding: utf-8 -*-
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

tests_require=['zope.testing', 'zc.buildout']

setup(name='gs.recipe.setupgs',
      version=version,
      description="Setup GroupServer instance in Zope",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
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
      zip_safe=True,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'gs.recipe.setupgs.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

