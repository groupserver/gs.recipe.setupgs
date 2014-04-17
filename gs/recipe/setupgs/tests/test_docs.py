# -*- coding: utf-8 -*-
"""
Doctest runner for 'gs.recipe.setupgs'.
"""
from __future__ import absolute_import, unicode_literals
import unittest
import zc.buildout.tests
import zc.buildout.testing
from zope.testing import doctest, renormalizing
from gs.recipe.setupgs.tests.scriptcreation import TestScriptCreation

optionflags = (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)


def setUp(test):
    zc.buildout.testing.buildoutSetUp(test)

    # Install the recipe in develop mode
    zc.buildout.testing.install_develop('gs.recipe.setupgs', test)

    # Install any other recipes that should be available in the tests
    #zc.buildout.testing.install('collective.recipe.foobar', test)


def test_suite():
    suite = unittest.TestSuite((
            doctest.DocFileSuite(
                '../README.txt',
                setUp=setUp,
                tearDown=zc.buildout.testing.buildoutTearDown,
                optionflags=optionflags,
                checker=renormalizing.RENormalizing([
                        # If want to clean up the doctest output you
                        # can register additional regexp normalizers
                        # here. The format is a two-tuple with the RE
                        # as the first item and the replacement as the
                        # second item, e.g.
                        # (re.compile('my-[rR]eg[eE]ps'), 'my-regexps')
                        zc.buildout.testing.normalize_path,
                        ]),
                ),
            ))
    suite.addTest(TestScriptCreation)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
