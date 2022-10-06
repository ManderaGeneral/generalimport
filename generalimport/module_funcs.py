import importlib
import pkgutil
import sys


def get_installed_modules_names():
    names = {module.name for module in pkgutil.iter_modules()}
    names.update(sys.builtin_module_names)
    return names


def package_is_installed(*names):
    """ Returns whether a package is installed.
        `find_spec(name) is None` was the previous solution but namespaces returned True. """
    packages = get_installed_modules_names()
    for name in names:
        if name not in packages:
            return False
    return True


def _safe_import(name):
    try:
        return importlib.import_module(name=name)
    except (ModuleNotFoundError, TypeError, ImportError) as e:
        return None


def _module_is_namespace(module):
    """ Returns if given module is a namespace, if it is it removes it from sys.modules. """
    is_namespace = module is not None and getattr(module, "__file__", None) is None
    if is_namespace:
        sys.modules.pop(module.__name__, None)
    return is_namespace


def import_module(name, error=True):
    """ Like importlib.import_module with optional error paremeter to return None if errored.
        Also excludes namespaces. """
    module = _safe_import(name=name)
    if _module_is_namespace(module=module):
        if error:
            raise ModuleNotFoundError(f"Module '{name}' is only a namespace.")
        return None
    else:
        if module is None and error:
            raise ModuleNotFoundError(f"Module '{name}' isn't installed.")
        return module


def module_is_namespace(name):
    return _module_is_namespace(module=_safe_import(name=name))