import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):
    def test_class_getitem(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            type(fakepackage)[5]

    def test_dir(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            dir(fakepackage)

    # https://github.com/ManderaGeneral/generalimport/issues/8
    @skip("Cannot cover __setattr__ as it won't allow `import foo.bar`.")
    def test_setattr(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            fakepackage.x = 5











