import sys

from generalimport import GeneralImporter, FakeModule


def _assert_no_dots(names):
    for name in names:
        assert "." not in name, f"Dot found in '{name}', only provide package without dots."

def get_importer():
    """ Return existing or new GeneralImporter instance. """
    return GeneralImporter.singleton_instance or GeneralImporter()

def generalimport(*names):
    """ Adds names to existing or new GeneralImporter instance. """
    _assert_no_dots(names=names)
    importer = get_importer()
    importer.enable()
    importer.add_names(*names)
    return importer

def check_import(obj):
    """ Simple assertion to trigger error_func earlier if module isn't installed. """
    if isinstance(obj, FakeModule):
        obj.error_func()






































