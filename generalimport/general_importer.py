import importlib
import sys

from logging import Logger
from pprint import pprint

from generalimport import FakeModule, module_is_namespace, spec_is_namespace

import inspect


class GeneralImporter:
    """ Creates fake packages if they don't exist.
        These fake packages' attrs are always a function that raises a ModuleNotFoundError when used.
        This lets you write a single line to handle all your optional dependencies.
        If wildcard (default "*") is provided then this will work on any missing package. """
    WILDCARD = "*"

    singleton_instance = None

    def __init__(self):
        self._singleton()
        self.names = set()
        self.added_fullnames = {}

        self._skip_fullname = None

    def _singleton(self):
        assert self.singleton_instance is None
        GeneralImporter.singleton_instance = self

    @staticmethod
    def _top_name(fullname):
        return fullname.split(".")[0]

    def _store_loaded_fullname(self, fullname):
        """ Stores fullname in a set in a dict using its' top name as key. """
        top_name = self._top_name(fullname=fullname)
        if top_name not in self.added_fullnames:
            self.added_fullnames[top_name] = set()

        self.added_fullnames[top_name].add(fullname)

    def _ignore_next_import(self, fullname):
        if fullname == self._skip_fullname:
            self._skip_fullname = None
            return True
        else:
            self._skip_fullname = fullname
            return False

    def _handle_this_name(self, fullname):
        top_name = self._top_name(fullname=fullname)

        if self.WILDCARD in self.names:
            is_top_name = top_name == fullname
            top_name_is_added = top_name in self.added_fullnames
            if is_top_name or top_name_is_added:  # Prevent handling existing_module.missing_module
                return True

        elif top_name in self.names:
            return True

        else:
            return False

    def _handle_ignore(self, fullname, reason):
        # print(f"Ignoring '{fullname}' - {reason}")
        Logger(__name__).debug(f"Ignoring '{fullname}' - {reason}")
        return None

    def _handle_handle(self, fullname, reason):
        # print(f"Handling '{fullname}' - {reason}")
        Logger(__name__).info(f"Handling '{fullname}' - {reason}")
        sys.modules.pop(fullname, None)
        return self

    def _handle_relay(self, fullname, loader):
        # print(f"'{fullname}' exists, returning it's loader '{loader}'")
        Logger(__name__).debug(f"'{fullname}' exists, returning it's loader '{loader}'")
        return loader

    def find_module(self, fullname, path=None):
        """ Returns self if fullname is in names, or if wildcard is present. """
        if not self._handle_this_name(fullname=fullname):
            return self._handle_ignore(fullname=fullname, reason="Unhandled")

        if self._ignore_next_import(fullname=fullname):
            return self._handle_ignore(fullname=fullname, reason="Recursive break")

        # if fullname == "pyarrow":
        #     pprint(inspect.stack())
        #     exit()

        spec = importlib.util.find_spec(fullname)

        if not spec:
            return self._handle_handle(fullname=fullname, reason="Doesn't exist")

        if spec_is_namespace(spec=spec):
            return self._handle_handle(fullname=fullname, reason="Namespace package")

        return self._handle_relay(fullname=fullname, loader=spec.loader)



    def load_module(self, fullname):
        """ Adds a FakeModule instance to sys.modules and stores fullname in case of disable. """
        module = FakeModule(name=fullname)
        sys.modules[fullname] = module
        self._store_loaded_fullname(fullname=fullname)

    def add_names(self, *names):
        self.names.update(names)

    def remove_names(self, *names):
        """ Removes FakeModule from sys.modules and then name from added_fullnames and names. """
        if names:
            names = set(names)
        else:
            names = self.names

        for name in names:
            for fullname in self.added_fullnames.get(name, []):
                sys.modules.pop(fullname, None)

        for name in names:
            self.added_fullnames.pop(name, None)

        self.names -= names

    def is_enabled(self):
        """ Whether importer is in sys.meta_path or not. """
        return self in sys.meta_path

    def enable(self):
        """ Enables importer by adding it to sys.meta_path.
            Starts from scratch if previously disabled. """
        if not self.is_enabled():
            sys.meta_path.insert(0, self)

    def disable(self):
        """ Disable importer by removing it from sys.meta_path.
            Removes any FakeModule instances this importer has added to sys.modules. """
        if self.is_enabled():
            sys.meta_path.remove(self)
            self.remove_names(*self.added_fullnames)
