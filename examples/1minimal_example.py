""" Call `GeneralImporter` before importing any optional dependencies.

    Here is a simple minimal example:"""

from generalimport import GeneralImporter
GeneralImporter("pandas")

import pandas  # No error

def func():
    pandas.DataFrame()

func()  # Error occurs here

""" Imports fail when they are **used**, *not* imported. """