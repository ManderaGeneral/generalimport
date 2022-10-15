import importlib
import sys
import inspect
from pprint import pprint


from logging import basicConfig

from generalimport import generalimport, get_installed_modules_names, import_module

basicConfig(level=10)

generalimport("*")

import pandas






