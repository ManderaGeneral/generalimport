import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import namespace_package, ImportTestCase


class Test(ImportTestCase):
    def test_eq(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage == 2







