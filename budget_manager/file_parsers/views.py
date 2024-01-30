from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from file_parsers.forms import CSVUploadForm
from file_parsers.models import CSVFile
from file_parsers.parsers.csv.nest import NestCSVParser
from file_parsers.parsers.csv.revolut import RevolutCSVParser
from file_parsers.parsers.csv.santander import SantanderCSVParser


class CSVUploadView(LoginRequiredMixin, FormView):
    template_name = "upload_csv.html"
    form_class = CSVUploadForm
    success_url = reverse_lazy("upload_csv")

    def form_valid(self, form):
        csv_file = form.cleaned_data["csv_file"]
        selected_bank = self.request.POST.get("bank", "")

        bank_parser_mapping = {
            "santander": SantanderCSVParser,
            "nest": NestCSVParser,
            "revolut": RevolutCSVParser,
        }

        parser_class = bank_parser_mapping.get(selected_bank)

        if parser_class:
            parser = parser_class()

        csv_file_instance = CSVFile.objects.create(user=self.request.user, csv_file=csv_file)

        csv_file_path = csv_file_instance.csv_file.path

        parsed_data = parser.parse_csv(csv_file_path, user=self.request.user)
        incomes, expenses = parsed_data

        return self.render_to_response({"form": form, "incomes": incomes, "expenses": expenses})
