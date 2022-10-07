import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_enter(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            with fakepackage:
                pass

        with self.assertRaises(MissingOptionalDependency):
            fakepackage.__enter__()

    def test_exit(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage.__exit__()








