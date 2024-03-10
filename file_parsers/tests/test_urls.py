from django.test import TestCase
from django.urls import resolve, reverse

from file_parsers.views import CSVUploadView


class FileParsersUrlsTestCase(TestCase):
    def setUp(self):
        self.csv_upload_url = reverse("file_parsers:upload-csv")

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.csv_upload_url).func.view_class, CSVUploadView)

    def test_urls_reverse(self):
        self.assertEqual(self.csv_upload_url, "/upload-csv/")
