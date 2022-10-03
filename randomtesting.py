import importlib

from generalfile import Path
from generallibrary import join_with_str, Log
from generalimport import *


import sys
import pkgutil

# import win32
# print(win32)
# exit()

# HERE ** see if installed and itermodules are connected both ways - from installed to itermodules look at top_level.txt, might be a reversed way

# Purpose
#   Proper package_is_installed() and module_is_namespace()
#   Answer https://stackoverflow.com/questions/739993/how-do-i-get-a-list-of-locally-installed-python-modules
#   Learn


# Missing origins
# find_spec is case-sensitive!



# CREATE TRUTH TABLE FROM THIS
# itermodules and piplist can have capital letters
# piplist equals working_set
# working_set has no underscore prefix
# builtin does not include all underscore prefix
# builtin modules are not found anywhere else
# itermodules has every module with venv or global origin, also has some more
# itermodules converts dash to underscore
# editable installs are caught by itermodules, not working_set (Unless it's main)
# itermodules can always resolve importlib.util.find_spec(module).loader
# working_set doesn't change dashes to underscores
# installed gets only .dist-info (Not found by find_spec) and .egg-link (editable install)
# installed lowers all names (find_spec is case-sensitive!)

# ---> THE ONLY MODULES INSTALLED FINDS THAT ITERMODULES DONT ARE PURE .dist-info

# Conclusion:
# installed lists distributions
# itermodules lists importable modules



# .dist-info -> pypi's name
# package or module is the same in distribution as it is in site-packages

# pip list uses .dist-info
# installed uses .dist-info but always lowered
# itermodules uses the actual package or module's name





# print(import_module("attrs"))
# exit()
# print(importlib.util.find_spec("openssl").origin)
# exit()

metapath_loaders = [getattr(x, "__name__", getattr(type(x), "__name__")) for x in sys.meta_path]

installed = get_installed_packages()
builtin = set(sys.builtin_module_names)
itermodules = {module.name for module in pkgutil.iter_modules()}

distinfos = {path.stem().split("-")[0].lower() for path in Path("C:\Python\Venvs\dev\Lib\site-packages").get_children(filt=lambda path: path.endswith(".dist-info"))}

# itermodules = {module.name.lower() for module in pkgutil.iter_modules()}


# modules = installed | itermodules
modules = installed | builtin | itermodules

print(len(modules))

lines = ["module, installed, builtin, itermodules, distinfo, underscore, both, origin, loader, duplicate, capital"]

# TRUE = "✔"
# TRUE = '\"True\"'
# FALSE = ""
# FALSE = "❌"
# FALSE = "False"
# TRUE = 1
FALSE = ""

# print(metapath_loaders)

for module in modules:
    module_obj = importlib.util.find_spec(module)
    origin = getattr(module_obj, "origin", "-")
    loader = getattr(module_obj, "loader", None)
    loader = getattr(loader, "__name__", getattr(type(loader), "__name__", None))
    lines.append(join_with_str(",", [
        module,
        "A+ ✔" if module in installed else "A-",
        "B+ ✔" if module in builtin else "B-",
        "C+ ✔" if module in itermodules else "C-",
        "H+ ✔" if module in distinfos else "H-",
        "D+ ✔" if module.startswith("_") else "D-",
        # "E+ ✔" if module in piplist and module not in installed | builtin | itermodules else "E-",
        "F+ ✔" if module in installed and module in itermodules else "F-",
        origin,
        # "venv" if "Venvs" in origin else "global" if "AppData" in origin else "repo" if "repos" in origin else origin,
        # "G+ ✔" if "-" in module else "G-",
        loader,
        module.lower() != module and module.lower() in modules,
        module.lower() != module,
    ]))



Path("data.csv").text.write("\n".join(lines), overwrite=True)


