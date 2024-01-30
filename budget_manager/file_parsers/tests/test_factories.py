from django.test import TestCase
from file_parsers.factories import CSVFileFactory
from file_parsers.models import CSVFile


class FileParsersFactoriesTest(TestCase):
    def test_create_currency_correct_create_object(self):
        CSVFileFactory()

        self.assertEqual(CSVFile.objects.count(), 1)

    def test_create_currency_factory_batch_size_works_correctly(self):
        CSVFileFactory.create_batch(5)

        self.assertEqual(CSVFile.objects.count(), 5)
