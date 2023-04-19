import sys
from unittest import skip

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(ImportTestCase):

    def test_type_with_module(self):
        generalimport("fakepackage")
        import fakepackage

        def my_function1(something: fakepackage):
            pass
        
        def my_function2(something: int) -> fakepackage:
            pass

        my_function1(1)
        my_function2(1)


    def test_type_with_attribute(self):
        generalimport("fakepackage")
        import fakepackage

        def my_function1(something: fakepackage.something):
            pass

        def my_function2(something) -> fakepackage.something:
            pass

        my_function1(1)
        my_function2(1)



