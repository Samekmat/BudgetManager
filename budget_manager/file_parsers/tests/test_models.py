from datetime import datetime

from django.test import TestCase
from django.utils.timezone import make_aware
from file_parsers.factories import CSVFileFactory
from file_parsers.models import CSVFile
from users.factories import UserFactory


class CSVFileModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.upload_date = make_aware(datetime(year=2024, month=1, day=30))
        self.csv_file = CSVFileFactory(user=self.user, uploaded_at=self.upload_date)

    def test_csv_file_str_method(self):
        self.assertEqual(str(self.csv_file), "testuser - 2024-01-30")

    def test_csv_file_creation(self):
        initial_count = CSVFile.objects.count()
        CSVFileFactory()
        new_count = CSVFile.objects.count()
        self.assertEqual(new_count, initial_count + 1)
