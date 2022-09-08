import sys
from unittest import TestCase

import generalimport
from generalimport import *

class Test(TestCase):
    def test_get_installed_packages(self):
        self.assertIn("generalimport", get_installed_packages())
        self.assertIn("setuptools", get_installed_packages())
        self.assertNotIn("doesntexist", get_installed_packages())

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
            x = FakeModule("foo").whatever + 2

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
        GeneralImporter.get_enabled()
        importer = GeneralImporter()
        self.assertIn(importer, GeneralImporter.get_enabled())
        importer.disable()
        self.assertNotIn(importer, GeneralImporter.get_enabled())

    def test_error_func(self):
        self.assertRaises(MissingOptionalDependency, FakeModule("foo").error_func, 1, 2, 3, 4, 5, x=2, y=3)

    def test_disable_all(self):
        importer = GeneralImporter("foobar")
        enabled = GeneralImporter.get_enabled()
        self.assertIn(importer, enabled)
        self.assertEqual(True, importer.is_enabled())

        GeneralImporter.disable_all()
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


    def test_importlib(self):
        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")
        importer = GeneralImporter("thisdoesntexist")

        import_module("thisdoesntexist")
        importer.disable()

        self.assertRaises(ModuleNotFoundError, import_module, "thisdoesntexist")

        self.assertIs(import_module("generalimport"), generalimport)

        import_module("generalimport")





























