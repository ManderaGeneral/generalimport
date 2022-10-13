import importlib
import sys
from logging import basicConfig

from generalimport import generalimport, get_installed_modules_names, import_module

basicConfig(level=10)

generalimport("*")

import hi
# import_module("hi")
# _safe_import("hi")
importlib.import_module("hi")






