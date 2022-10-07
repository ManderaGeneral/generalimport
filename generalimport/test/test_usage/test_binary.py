import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_ilshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            fakepackage <<= 5

    def test_irshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            fakepackage >>= 5

    def test_invert(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            ~fakepackage

    def test_ixor(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            fakepackage ^= 5

    def test_lshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            fakepackage << 5

    def test_rlshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            5 << fakepackage

    def test_rrshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            5 >> fakepackage

    def test_rshift(self):
        generalimport("fakepackage")
        import fakepackage
        with self.assertRaises(MissingOptionalDependency):
            fakepackage >> 5


