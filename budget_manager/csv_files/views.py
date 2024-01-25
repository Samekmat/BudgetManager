from csv_files.bank_csv_parsers import NestParser, RevolutParser, SantanderParser
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
        selected_bank = self.request.POST.get("bank", "")

        if selected_bank == "santander":
            parser = SantanderParser()
        elif selected_bank == "nest":
            parser = NestParser()
        elif selected_bank == "revolut":
            parser = RevolutParser()
        # else:
        #     parser = DefaultParser()

        csv_file_instance = CSVFile(user=self.request.user, csv_file=csv_file)
        csv_file_instance.save()

        csv_file_path = csv_file_instance.csv_file.path

        parsed_data = parser.parse_csv(csv_file_path, user=self.request.user)
        incomes, expenses = parsed_data

        return self.render_to_response({"form": form, "incomes": incomes, "expenses": expenses})
