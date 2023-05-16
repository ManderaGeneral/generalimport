from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_subclass_class_returning_self(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            pass

        foo = SubClass.bar  # Won't error if SubClass is a FakeModule

        with self.assertRaises(MissingDependencyException):
            foo *= 2

    def test_subclass_module(self):
        generalimport("fakepackage")
        import fakepackage

        class X(fakepackage):
            pass

        with self.assertRaises(MissingDependencyException):
            X()

    def test_subclass_class(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            def __init__(self):
                raise ValueError("'generalimport' should fail earlier with MissingDependencyException")

        self.assertRaises(MissingDependencyException, SubClass)

    def test_subclass_class_direct_new_call(self):
        generalimport("fakepackage")
        import fakepackage

        class SubClass(fakepackage.BaseClass):
            def __init__(self):
                raise ValueError("'generalimport' should fail earlier with MissingDependencyException")

        with self.assertRaises(MissingDependencyException):
            SubClass.__new__(SubClass)
