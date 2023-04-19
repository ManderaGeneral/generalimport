import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):

    def test_subclass_class_returning_self(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            pass

        foo = SubClass.bar

        with self.assertRaises(MissingOptionalDependency):
            foo *= 2

    def test_subclass_module(self):
        generalimport("fakepackage")
        import fakepackage

        class X(fakepackage):
            pass

        with self.assertRaises(MissingOptionalDependency):
            X()

    def test_subclass_class(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            def __init__(self):
                raise ValueError("'generalimport' should fail earlier with MissingOptionalDependency")
        
        self.assertRaises(MissingOptionalDependency, SubClass)

    def test_subclass_class_direct_new_call(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            def __init__(self):
                raise ValueError("'generalimport' should fail earlier with MissingOptionalDependency")
        
        with self.assertRaises(MissingOptionalDependency):
            SubClass.__new__(SubClass)
