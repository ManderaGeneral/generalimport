import importlib
import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase
from generalimport.generalimport_bottom import _safe_import


class Test(ImportTestCase):
    def test_get_installed_packages(self):
        self.assertIn("generalimport", get_installed_modules_names())
        self.assertIn("mmap", get_installed_modules_names())  # built-in
        self.assertNotIn("doesntexist", get_installed_modules_names())

    def test_package_is_installed(self):
        self.assertEqual(True, module_is_installed("generalimport"))
        self.assertEqual(True, module_is_installed("setuptools"))
        self.assertEqual(False, module_is_installed("doesntexist"))
    
    def test_package_is_imported(self):
        self.assertEqual(True, is_imported("generalimport"))
        self.assertEqual(False, is_imported("setuptools"))
        self.assertEqual(False, is_imported("doesntexist"))

    def test_MissingDependencyException(self):
        self.assertEqual("foo", MissingDependencyException("foo").msg)
        self.assertIn("foo", repr(MissingDependencyException("foo")))
        self.assertIn("foo", str(MissingDependencyException("foo")))

        self.assertIn("MissingDependencyException", repr(MissingDependencyException()))
        self.assertEqual(str(AttributeError()), str(MissingDependencyException()))

    def test_GeneralImporter(self):
        generalimport("packagethatdoesntexist")

        self.assertIn(get_importer(), sys.meta_path)

        self.assertRaises(AssertionError, GeneralImporter)  # Singleton

        import packagethatdoesntexist
        self.assertRaises(MissingDependencyException, packagethatdoesntexist)

        from packagethatdoesntexist.module import fakefunc
        self.assertRaises(MissingDependencyException, fakefunc)

        import packagethatdoesntexist.module.fakefunc2
        self.assertRaises(MissingDependencyException, packagethatdoesntexist.module.fakefunc2)

        with self.assertRaises(ImportError):
            import notexisting

        with self.assertRaises(ImportError):
            from notexisting import hi

        with self.assertRaises(ImportError):
            from notexisting.hey import hi

        with self.assertRaises(ImportError):
            import notexisting.hi.hey

    def test_find_module_relay(self):
        """ pkg_resources is one of the few packages always included in venv. """
        generalimport("pkg_resources")
        sys.modules.pop("pkg_resources", None)
        import pkg_resources
        fake_module_check(pkg_resources)

    def test_wildcard(self):
        generalimport("*")

        from whateverz import this
        self.assertRaises(MissingDependencyException, this)

        from whateverz.hi import that
        self.assertRaises(MissingDependencyException, that)

        import hiii
        self.assertRaises(MissingDependencyException, hiii)

        import heyyyy.foo
        self.assertRaises(MissingDependencyException, heyyyy.foo)

    def test_import_module(self):
        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")

        generalimport("thisdoesntexist")
        thisdoesntexist = import_module("thisdoesntexist")

        self.assertRaises(MissingDependencyException, thisdoesntexist)

        self.assertIs(import_module("generalimport"), gi)
        import_module("generalimport")

    def test_import_module_namespace(self):
        self.assertIs(None, import_module("namespace", error=False))
        self.assertRaises(ModuleNotFoundError, import_module, "namespace")

    def test_namespace_importer(self):
        self.assertEqual(True, module_name_is_namespace("namespace"))
        self.assertEqual(True, module_name_is_namespace("namespace"))

        generalimport("namespace")

        from namespace.mod import func

        self.assertRaises(MissingDependencyException, func)

    def test_generalimport(self):
        self.assertEqual(True, module_name_is_namespace("namespace"))
        self.assertEqual(True, module_name_is_namespace("namespace"))

        catcher = generalimport("namespace", "missing_dep")
        self.assertEqual(2, len(catcher.names))

        catcher2 = generalimport("another_missing")
        self.assertEqual(1, len(catcher2.names))

        import namespace
        import missing_dep
        import another_missing

        self.assertRaises(MissingDependencyException, namespace.func)
        self.assertRaises(MissingDependencyException, missing_dep.func)
        self.assertRaises(MissingDependencyException, another_missing.func)

    def test_fake_module_check(self):
        generalimport("fakepackage")
        import fakepackage

        self.assertRaises(MissingDependencyException, fake_module_check, fakepackage)
        self.assertIs(True, fake_module_check(fakepackage, error=False))

        fake_module_check(sys)
        self.assertIs(False, fake_module_check(sys, error=False))

    def test_import_catcher_scope(self):
        catcher = generalimport("hi")
        self.assertIn("test", catcher._scope)

    def test_import_catcher_outside_scope(self):
        catcher = generalimport("fakepackage")
        catcher._scope = "some/random/path"

        self.assertRaises(ImportError, import_module, "fakepackage")

    def test_import_catcher_scope_is_none(self):
        catcher = generalimport("fakepackage")
        catcher._scope = None

        import fakepackage

        self.assertIs(True, fake_module_check(fakepackage, error=False))

    def test_latest_scope_filename_import(self):
        catcher = generalimport("hi")

        import hi
        self.assertIs(True, fake_module_check(hi, error=False))
        self.assertIn("test_generalimport.py", catcher.latest_scope_filename)

    def test_latest_scope_filename_import_module(self):
        catcher = generalimport("hi")

        hi = import_module("hi")
        self.assertIs(True, fake_module_check(hi, error=False))
        self.assertIn("test_generalimport.py", catcher.latest_scope_filename)

    def test_latest_scope_filename_safe_import(self):
        catcher = generalimport("hi")

        hi = _safe_import("hi")
        self.assertIs(True, fake_module_check(hi, error=False))
        self.assertIn("test_generalimport.py", catcher.latest_scope_filename)

    def test_latest_scope_filename_importlib(self):
        catcher = generalimport("hi")

        hi = importlib.import_module("hi")
        self.assertIs(True, fake_module_check(hi, error=False))
        self.assertIn("test_generalimport.py", catcher.latest_scope_filename)

    def test_correct_message(self):
        from generalimport import generalimport
        generalimport("missing_dep")

    def test_logging_message(self):
        generalimport("nonexisting", "missing_dep")
        import nonexisting

        with self.assertLogs('generalimport', level='DEBUG') as cm:
            with self.assertRaises(MissingDependencyException):
                nonexisting.func()

        self.assertIn("nonexisting", cm.output[0])
        self.assertIn("__call__", cm.output[0])

        from missing_dep import foo
        from missing_dep import bar

        try:
            foo()
        except MissingDependencyException as e:
            self.assertIn("foo", str(e))
        else:
            self.fail("Error not raised")

        try:
            bar()
        except MissingDependencyException as e:
            self.assertIn("bar", str(e))
        else:
            self.fail("Error not raised")





















