""" The beauty of this package is that the error raised isn't just any exception.
    It has two base classes: `unittest.case.SkipTest` and `_pytest.outcomes.Skipped` (If available).

    This means that if a test method uses an uninstalled optional package then that test is automatically skipped.
    This means no more manual skip decorators for optional dependencies! """

from generalimport import generalimport
generalimport("optional_uninstalled_package")

from optional_uninstalled_package import missing_func

from unittest import TestCase

class MyTest(TestCase):
    def test_missing_func(self):
        self.assertEqual(3, missing_func(1, 2))

"""
```
Ran 1 test in 0.002s

OK (skipped=1)

Skipped: Optional dependency 'optional_uninstalled_package' was used but it isn't installed.
```
"""
