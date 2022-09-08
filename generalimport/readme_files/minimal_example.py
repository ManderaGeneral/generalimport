from generalimport import GeneralImporter
GeneralImporter("pandas")

import pandas  # Will never error

def func():
    pandas.DataFrame()

func()  # Error occurs here if pandas is missing

""" This 'small' difference makes optional dependencies a breeze. """