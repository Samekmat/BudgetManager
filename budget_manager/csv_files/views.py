from csv_files.bank_csv_parsers import SantanderParser
from csv_files.forms import CSVUploadForm
from csv_files.models import CSVFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView


class CSVUploadView(LoginRequiredMixin, FormView):
    template_name = "upload_csv.html"
    form_class = CSVUploadForm
    success_url = reverse_lazy("upload_csv")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csv_file"]

        csv_file_instance = CSVFile(user=self.request.user, csv_file=csv_file)
        csv_file_instance.save()

        csv_file_path = csv_file_instance.csv_file.path

        santander_parser = SantanderParser()
        parsed_data = santander_parser.parse_csv(csv_file_path, user=self.request.user)

        incomes, expenses = parsed_data

        return self.render_to_response({"form": form, "incomes": incomes, "expenses": expenses})
