""" I recommend to put this at the top of your main `__init__.py` file. """

from generalimport import GeneralImporter
GeneralImporter("your", "optional", "dependencies")

""" This is all you need to write to use this package. 
    Optional dependencies are usually defined in `setup.py`'s `extras_require` parameter. 
    
    You can also write `GeneralImporter("*")` to make **any** package importable."""
