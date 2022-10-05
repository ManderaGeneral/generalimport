import sys

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import namespace_package, ImportTestCase


class Test(ImportTestCase):
    def test_get_installed_packages(self):
        self.assertIn("generalimport", get_installed_modules_names())
        self.assertIn("setuptools", get_installed_modules_names())
        self.assertIn("mmap", get_installed_modules_names())
        self.assertNotIn("doesntexist", get_installed_modules_names())

    def test_package_is_installed(self):
        self.assertEqual(True, package_is_installed("generalimport"))
        self.assertEqual(True, package_is_installed("setuptools"))
        self.assertEqual(False, package_is_installed("doesntexist"))

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
        importer = GeneralImporter()
        self.assertIn(importer, sys.meta_path)

        importer2 = GeneralImporter("packagethatdoesntexist")
        self.assertIn(importer2, sys.meta_path)

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
        importer2.disable()
        self.assertNotIn(importer, sys.meta_path)
        self.assertNotIn(importer2, sys.meta_path)

    def test_get_enabled(self):
        get_enabled_importers()
        importer = GeneralImporter()
        self.assertIn(importer, get_enabled_importers())
        importer.disable()
        self.assertNotIn(importer, get_enabled_importers())

    def test_error_func(self):
        self.assertRaises(MissingOptionalDependency, FakeModule("foo").error_func, 1, 2, 3, 4, 5, x=2, y=3)

    def test_disable_all(self):
        importer = GeneralImporter("foobar")
        enabled = get_enabled_importers()
        self.assertIn(importer, enabled)
        self.assertEqual(True, importer.is_enabled())

        disable_importers()
        self.assertEqual(False, importer.is_enabled())

        for importer in enabled:
            importer.enable()
        self.assertEqual(True, importer.is_enabled())
        importer.disable()
        self.assertEqual(False, importer.is_enabled())

    def test_load_module(self):
        importer = GeneralImporter("foo")
        importer.load_module("bar")
        self.assertIn("bar", importer.added_fullnames)
        self.assertIn("bar", sys.modules)

        importer.disable()
        self.assertNotIn("bar", importer.added_fullnames)
        self.assertNotIn("bar", sys.modules)

    def test_find_module(self):
        importer = GeneralImporter("foo")
        self.assertIs(importer, importer.find_module("foo"))
        self.assertIs(None, importer.find_module("bar"))

    def test_wildcard(self):
        GeneralImporter("*")

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
        importer = GeneralImporter("thisdoesntexist")

        import_module("thisdoesntexist")
        importer.disable()

        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")

        self.assertIs(import_module("generalimport"), gi)

        import_module("generalimport")

    def test_importmodule_namespace(self):
        with namespace_package("fake_namespace"):
            self.assertEqual(None, import_module("fake_namespace", error=False))
            import fake_namespace
            self.assertEqual("fake_namespace", fake_namespace.__name__)

    def test_namespace_importer(self):
        with namespace_package("fake_namespace"):
            self.assertEqual(True, module_is_namespace("fake_namespace"))
            self.assertEqual(True, module_is_namespace("fake_namespace"))

            generalimport("fake_namespace")

            from fake_namespace.mod import func

            self.assertRaises(MissingOptionalDependency, func)

    def test_generalimport(self):
        with namespace_package("fake_namespace"):
            self.assertEqual(True, module_is_namespace("fake_namespace"))
            self.assertEqual(True, module_is_namespace("fake_namespace"))
            self.assertEqual(0, len(get_enabled_importers()))

            generalimport("fake_namespace", "missing_dep")
            self.assertEqual(2, len(get_enabled_importers()))

            generalimport("another_missing")
            self.assertEqual(2, len(get_enabled_importers()))

            import fake_namespace
            import missing_dep
            import another_missing

            self.assertRaises(MissingOptionalDependency, fake_namespace.func)
            self.assertRaises(MissingOptionalDependency, missing_dep.func)
            self.assertRaises(MissingOptionalDependency, another_missing.func)

    def test_check_import(self):
        generalimport("fakepackage")
        import fakepackage
        self.assertRaises(MissingOptionalDependency, check_import, fakepackage)
        check_import(sys)





























