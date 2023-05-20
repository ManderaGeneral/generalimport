from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_annotations(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__annotations__

    def test_call(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage()

    def test_closure(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__closure__

    def test_code(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__code__

    def test_defaults(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__defaults__

    def test_globals(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__globals__

    def test_kwdefaults(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingDependencyException):
            fakepackage.__kwdefaults__

