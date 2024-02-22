from datetime import datetime

import factory
from file_parsers.models import CSVFile
from users.factories import UserFactory


class CSVFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CSVFile

    user = factory.SubFactory(UserFactory)
    csv_file = factory.django.FileField(filename="example.csv")
    uploaded_at = datetime(year=2024, month=1, day=30)
