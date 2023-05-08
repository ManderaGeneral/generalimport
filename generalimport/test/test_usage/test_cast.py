import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_bool(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            bool(fakepackage)

    def test_bytes(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            bytes(fakepackage)

    def test_complex(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            complex(fakepackage)

    def test_float(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            float(fakepackage)

    def test_int(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            int(fakepackage)

    def test_iter(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            iter(fakepackage)

    def test_hash(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            hash(fakepackage)
