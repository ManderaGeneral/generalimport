from unittest import TestCase

from generalimport import reset_generalimport


class ImportTestCase(TestCase):
    def tearDown(self):
        super().tearDown()
        reset_generalimport()

