""" Put this in your `__init__.py` file to affect *all* imports inside the folder `__init__.py` resides in. """

from generalimport import generalimport
generalimport("your", "optional", "dependencies")

"""
`generalimport("*")` makes it handle **all** names (If missing of course)

:warning: `generalimport("*")._scope = None` disables the scope
 - Makes it handle missing imports anywhere
 - For example it will override `pandas` internal custom optional dependency handling
"""
