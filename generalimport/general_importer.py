import importlib
import sys
from logging import getLogger

from generalimport import FakeModule, spec_is_namespace, _get_top_name, get_spec, fake_module_check, module_is_namespace


class GeneralImporter:
    """ Creates fake packages if they don't exist.
        These fake packages' attrs are always a function that raises a ModuleNotFoundError when used.
        This lets you write a single line to handle all your optional dependencies.
        If wildcard (default "*") is provided then this will work on any missing package. """

    singleton_instance = None

    def __init__(self):
        self.catchers = []

        self._singleton()
        self._skip_fullname = None
        sys.meta_path.insert(0, self)

    def catch(self, fullname):
        """ Return first catcher that handles given fullname and filename.

            :rtype: generalimport.ImportCatcher """
        for catcher in self.catchers:
            if catcher.handle(fullname=fullname):
                return catcher

    def find_spec(self, fullname, path=None, target=None):
        if self._ignore_next_import(fullname=fullname):
            return self._handle_ignore(fullname=fullname, reason="Recursive break")

        if self._ignore_existing_top_name(fullname=fullname):
            return self._handle_ignore(fullname=fullname, reason="Top name exists and is not namespace")

        spec = get_spec(fullname)
        if not spec:
            return self._handle_handle(fullname=fullname, reason="Doesn't exist")

        if spec_is_namespace(spec=spec):
            return self._handle_handle(fullname=fullname, reason="Namespace package")

        return self._handle_relay(fullname=fullname, spec=spec)

    def create_module(self, spec):
        return FakeModule(spec=spec)

    def exec_module(self, module):
        pass



    def _singleton(self):
        assert self.singleton_instance is None
        GeneralImporter.singleton_instance = self

    def _ignore_existing_top_name(self, fullname):
        name = _get_top_name(fullname=fullname)
        if name == fullname:
            return False
        module = sys.modules.get(name, None)
        module_is_real = not fake_module_check(module, error=False)
        return module_is_real and not module_is_namespace(module)

    def _ignore_next_import(self, fullname):
        if fullname == self._skip_fullname:
            self._skip_fullname = None
            return True
        else:
            self._skip_fullname = fullname
            return False

    def _handle_ignore(self, fullname, reason):
        getLogger(__name__).debug(f"Ignoring '{fullname}' - {reason}")
        return None

    def _handle_handle(self, fullname, reason):
        catcher = self.catch(fullname=fullname)
        if not catcher:
            return self._handle_ignore(fullname=fullname, reason="Unhandled")

        getLogger(__name__).info(f"{catcher} is handling '{fullname}' - {reason}")

        sys.modules.pop(fullname, None)  # Remove possible namespace

        return importlib.util.spec_from_loader(fullname, self)

    def _handle_relay(self, fullname, spec):
        getLogger(__name__).debug(f"'{fullname}' exists, returning it's spec '{spec}'")
        return spec
