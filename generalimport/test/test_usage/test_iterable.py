import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_len(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            len(fakepackage)

    def test_next(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            next(fakepackage)

    def test_reversed(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            reversed(fakepackage)

    def test_contains(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            5 in fakepackage

    def test_getitem(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage[0]

    def test_index(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__index__()

    def test_setitem(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage[5] = "foo"
