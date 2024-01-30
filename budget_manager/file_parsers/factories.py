import factory
from file_parsers.models import CSVFile
from users.factories import UserFactory


class CSVFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CSVFile

    user = factory.SubFactory(UserFactory)
    csv_file = factory.django.FileField(filename="example.csv")
    uploaded_at = factory.Faker("date_time_this_decade")
