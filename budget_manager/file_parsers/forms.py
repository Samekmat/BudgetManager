from django.core.exceptions import ValidationError
from django.forms import forms


def validate_csv_file(value):
    if not value.name.endswith(".csv"):
        raise ValidationError("File must have a .csv extension.")


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[validate_csv_file])
