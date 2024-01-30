from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from file_parsers.forms import CSVUploadForm


class CSVUploadFormTest(TestCase):
    def test_csv_upload_form_valid(self):
        csv_content = b"test data,123\n456,789"
        csv_file = SimpleUploadedFile("testfile.csv", csv_content)

        form_data = {"csv_file": csv_file}

        form = CSVUploadForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())

    def test_csv_upload_form_invalid_empty_file(self):
        empty_file = SimpleUploadedFile("emptyfile.csv", b"")

        form_data = {"csv_file": empty_file}

        form = CSVUploadForm(data=form_data, files=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("csv_file", form.errors)
        self.assertEqual(form.errors["csv_file"][0], "The submitted file is empty.")

    def test_csv_upload_form_invalid_wrong_file_type(self):
        text_file = SimpleUploadedFile("textfile.txt", b"some text content")

        form_data = {"csv_file": text_file}

        form = CSVUploadForm(data=form_data, files=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("csv_file", form.errors)
        self.assertEqual(form.errors["csv_file"][0], "File must have a .csv extension.")
