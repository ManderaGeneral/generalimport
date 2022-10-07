import importlib
import pkgutil
import sys


def get_installed_modules_names():
    names = {module.name for module in pkgutil.iter_modules()}
    names.update(sys.builtin_module_names)
    return names

def module_is_installed(*names):
    """ Returns whether a package is installed.
        `find_spec(name) is None` was the previous solution but namespaces returned True.
        Todo: Change back to find_spec if spec_is_namespace works. """
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

def import_module(name, error=True):
    """ Like importlib.import_module with optional error paremeter to return None if errored.
        Also excludes namespaces. """
    module = _safe_import(name=name)
    if module_is_namespace(module=module):
        if error:
            raise ModuleNotFoundError(f"Module '{name}' is only a namespace.")
        return None
    else:
        if module is None and error:
            raise ModuleNotFoundError(f"Module '{name}' isn't installed.")
        return module

def spec_is_namespace(spec):
    return spec and spec.loader is None

def module_is_namespace(module):
    """ Returns if given module is a namespace. """
    return module is not None and hasattr(module, "__path__") and getattr(module, "__file__", None) is None

def module_name_is_namespace(name):
    """ Checks if module's name is a namespace without adding it to sys.modules. """
    was_in_modules = name in sys.modules
    module = _safe_import(name=name)
    is_namespace = module_is_namespace(module=module)

    if was_in_modules:
        sys.modules.pop(name, None)

    return is_namespace
