import importlib

from generalfile import Path
from generallibrary import join_with_str
from generalimport import generalimport, get_installed_packages, module_is_namespace, import_module
# generalimport("foobar")

import sys
import pkgutil

# CREATE TRUTH TABLE FROM THIS
# itermodules and piplist can have capital letters
# piplist equals working_set
# itermodules and builtin have no module in common
# working_set has no underscore prefix
# builtin does not include all underscore prefix
# builtin modules are not found anywhere else
# itermodules has every module with venv or global origin, also has some more
# itermodules has no module with a dash ("-") in it
# editable installs are caught by itermodules, not working_set (Unless it's main)
# itermodules can always resolve importlib.util.find_spec(module).loader
# working_set doesn't change dashes to underscores


# HERE ** Loaders with NoneType are previously installed packages picked up by both itermodules and working_set
# They are not handled by import_module nor module_is_namespace


# print(import_module("attrs"))
# exit()
# print(importlib.util.find_spec("openssl").origin)
# exit()

metapath_loaders = [getattr(x, "__name__", getattr(type(x), "__name__")) for x in sys.meta_path]

installed = get_installed_packages()
builtin = set(sys.builtin_module_names)
itermodules = {module.name.lower() for module in pkgutil.iter_modules()}


modules = installed | itermodules
# modules = installed | builtin | itermodules

print(len(modules))

lines = ["module, installed, itermodules, both, origin, hasdash, loader"]

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
        # "B+ ✔" if module in builtin else "B-",
        "C+ ✔" if module in itermodules else "C-",
        # "D+ ✔" if module.startswith("_") else "D-",
        # "E+ ✔" if module in piplist and module not in installed | builtin | itermodules else "E-",
        "F+ ✔" if module in installed and module in itermodules else "F-",
        # origin,
        "venv" if "Venvs" in origin else "global" if "AppData" in origin else "repo" if "repos" in origin else origin,
        "G+ ✔" if "-" in module else "G-",
        loader,
    ]))



Path("data.csv").text.write("\n".join(lines), overwrite=True)


