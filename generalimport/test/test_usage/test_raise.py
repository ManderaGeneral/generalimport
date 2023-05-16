import unittest

from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_raise_exception(self):
        generalimport("missing_dep")

        from missing_dep import MyException

        with self.assertRaises(MissingDependencyException):
            raise MyException

    def test_raise_error(self):
        generalimport("missing_dep")

        from missing_dep import MyError

        with self.assertRaises(MissingDependencyException):
            raise MyError

    def test_raise_error_attribute(self):
        generalimport("missing_dep")

        import missing_dep

        with self.assertRaises(MissingDependencyException):
            raise missing_dep.MyError

    def test_try_catch(self):
        from generalimport import generalimport
        generalimport("missing_dep")

        from missing_dep import LangDetectException, detect

        try:
            detect("foo")
        except LangDetectException:
            pass

    @unittest.skip("Catching raise currently relies on suffix.")
    def test_raise_error_bad_suffix(self):
        generalimport("missing_dep")

        from missing_dep import ErrorBadSuffix

        with self.assertRaises(MissingDependencyException):
            raise ErrorBadSuffix