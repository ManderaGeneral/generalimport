import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_eq(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage == 2

    def test_ge(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage >= 2

    def test_gt(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage > 2

    # https://github.com/ManderaGeneral/generalimport/issues/4
    @skip("Cannot cover `raise X` unless `isinstance(X, Y)` is covered.")
    def test_instancecheck(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            isinstance(fakepackage, int)

        with self.assertRaises(MissingOptionalDependency):
            raise fakepackage  # This should work if we solve isinstance()

    def test_le(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage <= 2

    def test_lt(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage < 2

    def test_ne(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage != 2

    def test_subclasscheck(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            issubclass(int, fakepackage)
