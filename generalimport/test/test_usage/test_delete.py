import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_delattr(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            del fakepackage.foo

    def test_delitem(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            del fakepackage[5]








