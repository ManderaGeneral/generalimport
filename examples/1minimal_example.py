""" Call `generalimport` before importing any optional dependencies. """

from generalimport import generalimport
generalimport("notinstalled")

from notinstalled import missing_func  # No error

missing_func()  # Error occurs here

"""
```
MissingOptionalDependency: Optional dependency 'notinstalled' was used but it isn't installed.
```

Imports fail when they are **used**, *not* imported. 

This means you don't need to keep checking if the package is installed before importing it.
Simply import your optional package and use it like you would any package and let it fail wherever it fails, with a nice error message. """