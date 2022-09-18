import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import namespace_package, ImportTestCase


class Test(ImportTestCase):
    def test_usage_len(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            len(fakepackage)

    def test_usage_get_item(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage[0]

    def test_usage_list(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            list(fakepackage)

    def test_usage_list(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage[1:2]

    def test_usage_in(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            5 in fakepackage