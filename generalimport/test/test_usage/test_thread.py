import sys
from unittest import skip, IsolatedAsyncioTestCase

import generalimport as gi
from generalimport import *

from generalimport.test.funcs import ImportTestCase


class Test(IsolatedAsyncioTestCase, ImportTestCase):
    async def test_aenter(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            async with fakepackage():
                pass

    async def test_aiter(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            async for x in fakepackage:
                pass

    async def test_await(self):
        generalimport("fakepackage")
        import fakepackage

        with self.assertRaises(MissingOptionalDependency):
            await fakepackage








