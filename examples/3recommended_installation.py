""" Put this in your `__init__.py` file to affect *all* imports inside the folder `__init__.py` resides in. """

from generalimport import generalimport
generalimport("your", "optional", "dependencies")

""" You can also write `generalimport("*")` to make **any** package importable."""
