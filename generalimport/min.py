import sys
from unittest.case import SkipTest
from _pytest.outcomes import Skipped

class MissingOptionalDependency(SkipTest, Skipped):
    def __init__(self, msg=None):
        self.msg = msg
    def __repr__(self):
        return f"MissingOptionalDependency: {self.msg}" if self.msg else f"MissingOptionalDependency"
    def __str__(self):
        return self.msg or "MissingOptionalDependency"

class GeneralImporter:
    def __init__(self, *names):
        self.names = names
        sys.meta_path.append(self)
    def find_module(self, fullname, path=None):
        if fullname.split(".")[0] in self.names:
            return self
    def load_module(self, fullname):
        module = FakeModule(name=fullname)
        sys.modules[fullname] = module

class FakeModule:
    __path__ = []
    def __init__(self, name):
        self.name = name
    def __call__(self, *args, **kwargs):
        raise MissingOptionalDependency(f"Optional dependency '{self.name}' was used but it isn't installed.")
    def __getattr__(self, item):
        return self

