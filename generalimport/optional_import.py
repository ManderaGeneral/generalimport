import importlib
import sys
import pkg_resources


def get_skip_base_classes():
    from unittest.case import SkipTest
    yield SkipTest

    try:
        from _pytest.outcomes import Skipped
        yield Skipped
    except ImportError:
        pass

def get_installed_packages():
    """ Get a set of all installed packages names. """
    return {pkg.key for pkg in pkg_resources.working_set}

def package_is_installed(*names):
    """ Returns whether a package is installed.
        `find_spec(name) is None` was the previous solution but namespaces returned True. """
    packages = get_installed_packages()
    for name in names:
        if name not in packages:
            return False
    return True

class MissingOptionalDependency(*get_skip_base_classes()):
    def __init__(self, msg=None):
        self.msg = msg

    def __repr__(self):
        if self.msg:
            return f"MissingOptionalDependency: {self.msg}"
        else:
            return f"MissingOptionalDependency"

    def __str__(self):
        return self.msg or "MissingOptionalDependency"

class GeneralImporter:
    """ Creates fake packages if they don't exist.
        These fake packages' attrs are always a function that raises a ModuleNotFoundError when used.
        This lets you write a single line to handle all your optional dependencies.
        If wildcard (default "*") is provided then this will work on any missing package. """
    WILDCARD = "*"

    def __init__(self, *names, handles_namespace=False):
        self.names = set()
        self.added_fullnames = {}

        self.add_names(*names)
        self.handles_namespace = handles_namespace

        self.enable()

    @staticmethod
    def _top_name(fullname):
        return fullname.split(".")[0]

    def _store_loaded_fullname(self, fullname):
        """ Stores fullname in a set in a dict using its' top name as key. """
        name = self._top_name(fullname=fullname)
        if name not in self.added_fullnames:
            self.added_fullnames[name] = set()
        self.added_fullnames[name].add(fullname)

    def find_module(self, fullname, path=None):
        """ Returns self if fullname is in names, or wildcard is present. """
        if self.WILDCARD in self.names or self._top_name(fullname) in self.names:
            return self

    def load_module(self, fullname):
        """ Adds a FakeModule instance to sys.modules and stores fullname in case of disable. """
        module = FakeModule(name=fullname)
        sys.modules[fullname] = module
        self._store_loaded_fullname(fullname=fullname)

    def add_names(self, *names):
        self.names.update(names)

    def remove_names(self, *names):
        """ Removes FakeModule from sys.modules and then name from added_fullnames. """
        for name in names:
            for fullname in self.added_fullnames.get(name, []):
                sys.modules.pop(fullname, None)

        for name in names:
            self.added_fullnames.pop(name, None)

    def is_enabled(self):
        """ Whether importer is in sys.meta_path or not. """
        return self in sys.meta_path

    def enable(self):
        """ Enables importer by adding it to sys.meta_path.
            Starts from scratch if previously disabled. """
        if not self.is_enabled():
            if self.handles_namespace:
                sys.meta_path.insert(0, self)
            else:
                sys.meta_path.append(self)

    def disable(self):
        """ Disable importer by removing it from sys.meta_path.
            Removes any FakeModule instances this importer has added to sys.modules. """
        if self.is_enabled():
            sys.meta_path.remove(self)
            self.remove_names(*self.added_fullnames)

def get_enabled_importers():
    """ List of enabled GeneralImporter instances. """
    return [importer for importer in sys.meta_path if isinstance(importer, GeneralImporter)]

def disable_importers():
    """ Disables all GeneralImporter instances. """
    for importer in get_enabled_importers():
        importer.disable()

def get_importer(handles_namespace):
    importers = get_enabled_importers()
    for importer in importers:
        if importer.handles_namespace is handles_namespace:
            return importer
    return GeneralImporter(handles_namespace=handles_namespace)


class FakeModule:
    """ Behaves like a module but any attrs asked for always returns self.
        Raises a ModuleNotFoundError when used in any way."""
    __path__ = []

    def __init__(self, name):
        self.name = name

    def error_func(self, *args, **kwargs):
        raise MissingOptionalDependency(f"Optional dependency '{self.name}' was used but it isn't installed.")

    def __getattr__(self, item):
        if item == "__version__":  # Maybe do something like this for some attrs
            self.error_func()
        return self

    __call__ = __enter__ = __exit__ = __str__ = __repr__ = __abs__ = __add__ = __all__ = __and__ = __builtins__ = __cached__ = __concat__ = __contains__ = __delitem__ = __doc__ = __eq__ = __file__ = __floordiv__ = __ge__ = __gt__ = __iadd__ = __iand__ = __iconcat__ = __ifloordiv__ = __ilshift__ = __imatmul__ = __imod__ = __imul__ = __index__ = __inv__ = __invert__ = __ior__ = __ipow__ = __irshift__ = __isub__ = __itruediv__ = __ixor__ = __le__ = __loader__ = __lshift__ = __lt__ = __matmul__ = __mod__ = __mul__ = __name__ = __ne__ = __neg__ = __not__ = __or__ = __package__ = __pos__ = __pow__ = __rshift__ = __setitem__ = __spec__ = __sub__ = __truediv__ = __xor__ = error_func

def _safe_import(name):
    try:
        return importlib.import_module(name=name)
    except (ModuleNotFoundError, TypeError) as e:
        return None

def _module_is_namespace(module):
    """ Returns if given module is a namespace, if it is it removes it from sys.modules. """
    is_namespace = module and getattr(module, "__file__", None) is None
    if is_namespace:
        sys.modules.pop(module.__name__, None)
    return is_namespace


def import_module(name, error=True):
    """ Like importlib.import_module with optional error paremeter to return None if errored.
        Also excludes namespaces. """
    module = _safe_import(name=name)
    if _module_is_namespace(module=module):
        module = None

    if module is None and error:
        raise ModuleNotFoundError(f"Module '{name}' is only a namespace.")
    return module

def module_is_namespace(name):
    return _module_is_namespace(module=_safe_import(name=name))

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








































