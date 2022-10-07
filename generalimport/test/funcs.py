
from unittest import TestCase

from generalimport import get_importer


class ImportTestCase(TestCase):
    def tearDown(self):
        super().tearDown()
        importer = get_importer()
        importer.disable()
        importer.remove_names()
