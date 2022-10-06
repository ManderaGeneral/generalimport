import sys

from generalimport import FakeModule


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