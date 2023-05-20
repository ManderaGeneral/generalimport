import os
import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_format(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            format(fakepackage)

        with self.assertRaises(MissingDependencyException):
            "{}".format(fakepackage)

    def test_fspath(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            os.fspath(fakepackage)

    def test_repr(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            repr(fakepackage)

    def test_str(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            str(fakepackage)








