import sys

from generalimport import GeneralImporter, FakeModule, module_is_namespace


def get_enabled_importers():
    """ List of enabled GeneralImporter instances. """
    return [importer for importer in sys.meta_path if isinstance(importer, GeneralImporter)]

def disable_importers():
    """ Disables all GeneralImporter instances. """
    for importer in get_enabled_importers():
        importer.disable()

def get_importer(handles_namespace: bool):
    """ Return existing or new GeneralImporter. """
    importers = get_enabled_importers()
    for importer in importers:
        if importer.handles_namespace is handles_namespace:
            return importer
    return GeneralImporter(handles_namespace=handles_namespace)


def _seperate_namespaces(names):
    names = set(names)
    namespaces = {name for name in names if module_is_namespace(name=name)}
    names -= namespaces
    return names, namespaces

def _assert_no_dots(names):
    for name in names:
        assert "." not in name, f"Dot found in '{name}', only provide package without dots."

def generalimport(*names):
    """ Adds names to GeneralImporter if they exist or create them.
        Will at most have two instances in sys.meta_path:
        One first to catch namespace imports. One last to catch uninstalled imports. """
    _assert_no_dots(names=names)
    names, namespaces = _seperate_namespaces(names=names)
    if names:
        get_importer(handles_namespace=False).add_names(*names)
    if namespaces:
        get_importer(handles_namespace=True).add_names(*namespaces)

def check_import(obj):
    """ Simple assertion to trigger error_func earlier if module isn't installed. """
    if isinstance(obj, FakeModule):
        obj.error_func()






































