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

    def test_MissingOptionalDependency(self):
        self.assertEqual("foo", MissingOptionalDependency("foo").msg)
        self.assertIn("foo", repr(MissingOptionalDependency("foo")))
        self.assertIn("foo", str(MissingOptionalDependency("foo")))

        self.assertEqual(None, MissingOptionalDependency().msg)
        self.assertIn("MissingOptionalDependency", repr(MissingOptionalDependency()))
        self.assertIn("MissingOptionalDependency", str(MissingOptionalDependency()))

    def test_FakeModule(self):
        self.assertRaises(MissingOptionalDependency, FakeModule("foo").anything)
        x = FakeModule("foo").whatever  # No error
        with self.assertRaises(MissingOptionalDependency):
            FakeModule("foo").whatever == "bar"

        fake = FakeModule("bar")
        self.assertIs(fake, fake.these.will.recursively.be.itself)

    def test_GeneralImporter(self):
        generalimport("packagethatdoesntexist")

        self.assertIn(get_importer(), sys.meta_path)

        self.assertRaises(AssertionError, GeneralImporter)  # Singleton

        import packagethatdoesntexist
        self.assertRaises(MissingOptionalDependency, packagethatdoesntexist)

        from packagethatdoesntexist.module import fakefunc
        self.assertRaises(MissingOptionalDependency, fakefunc)

        import packagethatdoesntexist.module.fakefunc2
        self.assertRaises(MissingOptionalDependency, packagethatdoesntexist.module.fakefunc2)

        with self.assertRaises(ImportError):
            import notexisting

        with self.assertRaises(ImportError):
            from notexisting import hi

        with self.assertRaises(ImportError):
            from notexisting.hey import hi

        with self.assertRaises(ImportError):
            import notexisting.hi.hey

    def test_error_func(self):
        self.assertRaises(MissingOptionalDependency, FakeModule("foo").error_func, 1, 2, 3, 4, 5, x=2, y=3)

    def test_load_module(self):
        importer = get_importer()
        importer.load_module("foo")
        self.assertIn("foo", sys.modules)

    def test_find_module(self):
        generalimport("foo")
        importer = get_importer()
        self.assertIs(importer, importer.find_module("foo"))
        self.assertIs(None, importer.find_module("bar"))

    def test_find_module_relay(self):
        """ pkg_resources is one of the few packages always included in venv. """
        generalimport("pkg_resources")
        sys.modules.pop("pkg_resources", None)
        import pkg_resources
        fake_module_check(pkg_resources)

    def test_wildcard(self):
        generalimport("*")

        from whateverz import this
        self.assertRaises(MissingOptionalDependency, this)

        from whateverz.hi import that
        self.assertRaises(MissingOptionalDependency, that)

        import hiii
        self.assertRaises(MissingOptionalDependency, hiii)

        import heyyyy.foo
        self.assertRaises(MissingOptionalDependency, heyyyy.foo)

    def test_import_module(self):
        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")

        generalimport("thisdoesntexist")
        thisdoesntexist = import_module("thisdoesntexist")

        self.assertRaises(MissingOptionalDependency, thisdoesntexist)

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

        self.assertRaises(MissingOptionalDependency, func)

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

        self.assertRaises(MissingOptionalDependency, namespace.func)
        self.assertRaises(MissingOptionalDependency, missing_dep.func)
        self.assertRaises(MissingOptionalDependency, another_missing.func)

    def test_fake_module_check(self):
        generalimport("fakepackage")
        import fakepackage

        self.assertRaises(MissingOptionalDependency, fake_module_check, fakepackage)
        self.assertIs(True, fake_module_check(fakepackage, error=False))

        fake_module_check(sys)
        self.assertIs(False, fake_module_check(sys, error=False))

    def test_import_catcher_scope(self):
        catcher = generalimport("hi")
        self.assertIn("test", catcher.scope)

    def test_import_catcher_outside_scope(self):
        catcher = generalimport("fakepackage")
        catcher.scope = "some/random/path"

        self.assertRaises(ImportError, import_module, "fakepackage")

    def test_import_catcher_scope_is_none(self):
        catcher = generalimport("fakepackage")
        catcher.scope = None

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

























