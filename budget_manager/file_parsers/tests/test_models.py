from django.test import TestCase
from file_parsers.factories import CSVFileFactory
from file_parsers.models import CSVFile
from users.factories import UserFactory


class CSVFileModelTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser")
        self.csv_file = CSVFileFactory(user=self.user)

    def test_csv_file_str_method(self):
        expected_str = f"{self.user.username} - {self.csv_file.uploaded_at.strftime('%Y-%m-%d')}"
        self.assertEqual(str(self.csv_file), expected_str)

    def test_csv_file_creation(self):
        initial_count = CSVFile.objects.count()
        CSVFileFactory(user=self.user)
        new_count = CSVFile.objects.count()
        self.assertEqual(new_count, initial_count + 1)
