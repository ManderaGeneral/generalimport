
from unittest import TestCase, skipIf


try:
    import optional
except ImportError:
    optional = None

def func():
    if optional is None:
        raise ModuleNotFoundError("Missing dependency 'optional'.")
    return optional.func()

class Testing(TestCase):
    @skipIf(optional is None)
    def test_method(self):
        self.assertEqual("foobar", optional.func())



from generalimport import generalimport
generalimport("optional")

from unittest import TestCase
import optional


def func():
    return optional.func()

class Testing(TestCase):
    def test_method(self):
        self.assertEqual("foobar", optional.func())



