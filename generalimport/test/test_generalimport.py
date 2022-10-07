import sys

import generalimport as gi
from generalimport import *
from generalimport import get_installed_modules_names, module_is_installed, GeneralImporter, FakeModule, import_module, module_name_is_namespace

from generalimport.test.funcs import ImportTestCase


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
        importer = generalimport("packagethatdoesntexist")
        self.assertIn(importer, sys.meta_path)

        self.assertRaises(AssertionError, GeneralImporter)

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

        importer.disable()
        self.assertNotIn(importer, sys.meta_path)

    def test_error_func(self):
        self.assertRaises(MissingOptionalDependency, FakeModule("foo").error_func, 1, 2, 3, 4, 5, x=2, y=3)

    def test_load_module(self):
        importer = generalimport("foo")
        importer.load_module("bar")
        self.assertIn("bar", importer.added_fullnames)
        self.assertIn("bar", sys.modules)

        importer.disable()
        self.assertNotIn("bar", importer.added_fullnames)
        self.assertNotIn("bar", sys.modules)

    def test_find_module(self):
        importer = generalimport("foo")
        self.assertIs(importer, importer.find_module("foo"))
        self.assertIs(None, importer.find_module("bar"))

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

    def test_importmodule(self):
        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")
        importer = generalimport("thisdoesntexist")

        import_module("thisdoesntexist")
        importer.disable()

        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")

        self.assertIs(import_module("generalimport"), gi)

        import_module("generalimport")

    def test_namespace_importer(self):
        self.assertEqual(True, module_name_is_namespace("namespace"))
        self.assertEqual(True, module_name_is_namespace("namespace"))

        generalimport("namespace")

        from namespace.mod import func

        self.assertRaises(MissingOptionalDependency, func)

    def test_generalimport(self):
        importer = get_importer()

        self.assertEqual(True, module_name_is_namespace("namespace"))
        self.assertEqual(True, module_name_is_namespace("namespace"))
        self.assertEqual(set(), importer.names)

        generalimport("namespace", "missing_dep")
        self.assertEqual(2, len(importer.names))

        generalimport("another_missing")
        self.assertEqual(3, len(importer.names))

        import namespace
        import missing_dep
        import another_missing


        self.assertRaises(MissingOptionalDependency, namespace.func)
        self.assertRaises(MissingOptionalDependency, missing_dep.func)
        self.assertRaises(MissingOptionalDependency, another_missing.func)

    def test_check_import(self):
        generalimport("fakepackage")
        import fakepackage
        self.assertRaises(MissingOptionalDependency, check_import, fakepackage)
        check_import(sys)





























