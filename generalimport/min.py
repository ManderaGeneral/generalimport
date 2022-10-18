import sys
import importlib
from unittest.case import SkipTest
from _pytest.outcomes import Skipped

class MissingOptionalDependency(SkipTest, Skipped):
    def __init__(self, msg=None):
        self.msg = msg
    def __repr__(self):
        return f"MissingOptionalDependency: {self.msg}" if self.msg else f"MissingOptionalDependency"

class GeneralImporter:
    def __init__(self, *names):
        self.names = names
        sys.meta_path.insert(0, self)
    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.names:
            return importlib.util.spec_from_loader(fullname, self)
    def create_module(self, spec):
        return FakeModule(name=spec.name)
    def exec_module(self, module):
        pass

class FakeModule:
    def __init__(self, name):
        self.name = name
    def __call__(self, *args, **kwargs):
        raise MissingOptionalDependency(f"Optional dependency '{self.name}' was used but it isn't installed.")

GeneralImporter("notinstalled")
import notinstalled  # No error
print(notinstalled)  # <__main__.FakeModule object at 0x0000014B7F6D9E80>
notinstalled()  # MissingOptionalDependency: Optional dependency 'notinstalled' was used but it isn't installed.
