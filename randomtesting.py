from inspect import currentframe

from generalimport import generalimport, get_installed_modules_names

import importlib, sys

generalimport("*")

import pandas

# HERE ** We can distinguish that only pandas should be handled by prints

# import inspect
# inspect.stack()

# for module in get_installed_modules_names():
#     if importlib.util.find_spec(module).loader is None:
#         print(module)


# print(importlib.util.find_spec("namespace"))  # find_spec does not load module!
# Can we see if module is namespace with find_spec

# print("pandas" in sys.modules)

# print(importlib.util.find_spec("pandas").loader.load_module("pandas"))
# print("pandas" in sys.modules)
# exit()

# class GeneralImporter:
#     names = set()
#
#     def __init__(self):
#         self._skip_fullname = None
#
#     def _ignore_next_import(self, fullname):
#         if fullname == self._skip_fullname:
#             self._skip_fullname = None
#             print("skip")
#             return True
#         else:
#             self._skip_fullname = fullname
#             return False
#
#     def find_module(self, fullname, path=None):
#         if self._ignore_next_import(fullname=fullname):
#             return None
#
#         print("find", fullname)
#         self.names.add(fullname)
#         # print("hi", importlib.util.find_spec(fullname).loader)
#         # sys.modules.pop(fullname, None)
#         module = importlib.util.find_spec(fullname)
#         print(dir(module))
#         if not module:
#             print("not module", fullname)
#             return None
#         return module.loader
#
#         # return self
#
#     def load_module(self, fullname):
#         print("load", fullname)
#         sys.modules[fullname] = 5
#
# sys.meta_path.insert(0, GeneralImporter())


