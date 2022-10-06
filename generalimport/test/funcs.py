import sys
from contextlib import contextmanager

from unittest import TestCase

from generalimport import get_importer


@contextmanager
def namespace_package(name):
    class Namespace:
        def __init__(self, name):
            self.__name__ = name
            self.__path__ = object()

    class Importer:
        def find_module(self, fullname, path=None):
            if fullname == name:
                return self

        def load_module(self, fullname):
            sys.modules[fullname] = Namespace(fullname)
    importer = Importer()
    sys.meta_path.append(importer)

    try:
        yield
    finally:
        sys.meta_path.remove(importer)


class ImportTestCase(TestCase):
    def tearDown(self):
        super().tearDown()
        importer = get_importer()
        importer.disable()
        importer.remove_names()
