""" Call `generalimport` before importing any optional dependencies.

    Here is a minimal example:"""

from generalimport import generalimport
generalimport("notinstalled")

import notinstalled  # No error

def func():
    notinstalled.missing_func()  # Error occurs here

func()

"""
```
MissingOptionalDependency: Optional dependency 'notinstalled' was used but it isn't installed.
```

Imports fail when they are **used**, *not* imported. 

This means you don't need to keep checking if the package is installed before importing it.
Simply import your optional package and use it like you would any package and let it fail wherever it fails, with a nice error message. """