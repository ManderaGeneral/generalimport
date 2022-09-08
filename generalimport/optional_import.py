import importlib
import sys
import pkg_resources


def get_skip_base_classes():
    try:
        from unittest.case import SkipTest
        yield SkipTest
    except ImportError:
        pass

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

    def __init__(self, *names):
        self.names = names
        self.enable()
        self.added_fullnames = []

    def find_module(self, fullname, path=None):
        """ Returns self if fullname is in names, or wildcard is present. """
        if self.WILDCARD in self.names or fullname.split(".")[0] in self.names:
            return self

    def load_module(self, fullname):
        """ Adds a FakeModule instance to sys.modules and stores fullname in case of disable. """
        module = FakeModule(name=fullname)
        sys.modules[fullname] = module
        self.added_fullnames.append(fullname)

    def is_enabled(self):
        """ Whether importer is in sys.meta_path or not. """
        return self in sys.meta_path

    def enable(self):
        """ Enables importer by adding it to sys.meta_path.
            Starts from scratch if previously disabled. """
        if not self.is_enabled():
            sys.meta_path.append(self)

    def disable(self):
        """ Disable importer by removing it from sys.meta_path.
            Removes any FakeModule instances this importer has added to sys.modules. """
        if self.is_enabled():
            sys.meta_path.remove(self)
        for fullname in self.added_fullnames:
            sys.modules.pop(fullname, None)
        self.added_fullnames.clear()

    @classmethod
    def get_enabled(cls):
        """ List of enabled GeneralImporter instances. """
        return [importer for importer in sys.meta_path if isinstance(importer, GeneralImporter)]

    @classmethod
    def disable_all(cls):
        """ Disables all GeneralImporter instances. """
        for importer in cls.get_enabled():
            importer.disable()


class FakeModule:
    """ Behaves like a module but any attrs asked for always returns self.
        Raises a ModuleNotFoundError when used in any way."""
    __path__ = []

    def __init__(self, name):
        self.name = name

    def error_func(self, *args, **kwargs):
        raise MissingOptionalDependency(f"Optional dependency '{self.name}' was used but it isn't installed.")

    def __getattr__(self, item):
        return self

    __call__ = __enter__ = __exit__ = __str__ = __repr__ = __abs__ = __add__ = __all__ = __and__ = __builtins__ = __cached__ = __concat__ = __contains__ = __delitem__ = __doc__ = __eq__ = __file__ = __floordiv__ = __ge__ = __gt__ = __iadd__ = __iand__ = __iconcat__ = __ifloordiv__ = __ilshift__ = __imatmul__ = __imod__ = __imul__ = __index__ = __inv__ = __invert__ = __ior__ = __ipow__ = __irshift__ = __isub__ = __itruediv__ = __ixor__ = __le__ = __loader__ = __lshift__ = __lt__ = __matmul__ = __mod__ = __mul__ = __name__ = __ne__ = __neg__ = __not__ = __or__ = __package__ = __pos__ = __pow__ = __rshift__ = __setitem__ = __spec__ = __sub__ = __truediv__ = __xor__ = error_func

def import_module(name, error=True):
    """ Like importlib.import_module with optional error paremeter to return None if errored.
        Also excludes namespaces. """
    try:
        module = importlib.import_module(name=name)
    except (ModuleNotFoundError, TypeError) as e:
        if error:
            raise e
    else:
        if getattr(module, "__file__", None):  # Got a namespace module without __file__ so filter those out here
            return module
        elif error:
            raise ModuleNotFoundError(f"Module '{name}' is only a namespace.")

