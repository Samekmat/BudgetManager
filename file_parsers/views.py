import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponseServerError
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
        else:
            return HttpResponseServerError("Parser not found for the selected bank.")

        # Save the file to S3 within the 'csv_files' directory
        file_name = os.path.join("csv_files", csv_file.name)
        file_path = default_storage.save(file_name, csv_file)

        try:
            csv_file_instance = CSVFile.objects.create(user=self.request.user, csv_file=file_path)
        except Exception as e:
            return HttpResponseServerError(f"Error occurred: {str(e)}")

        try:
            # Download the file from S3 to a temporary location
            local_file_path = f"/tmp/{file_name}"
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # Ensure directory exists
            with open(local_file_path, "wb") as local_file:
                csv_file.open("rb")
                local_file.write(csv_file.read())
        except Exception as e:
            csv_file_instance.delete()
            return HttpResponseServerError(f"Error occurred while saving CSV file: {str(e)}")

        try:
            parsed_data = parser.parse_csv(local_file_path, user=self.request.user)
            incomes, expenses = parsed_data
        except Exception as e:
            csv_file_instance.delete()
            os.remove(local_file_path)  # Remove the temporary file
            return HttpResponseServerError(f"Error occurred while parsing CSV file: {str(e)}")

        # Remove the temporary file
        os.remove(local_file_path)

        return self.render_to_response({"form": form, "incomes": incomes, "expenses": expenses})


# Local func
# class CSVUploadView(LoginRequiredMixin, FormView):
#     template_name = "upload_csv.html"
#     form_class = CSVUploadForm
#     success_url = reverse_lazy("upload_csv")
#
#     def form_valid(self, form):
#         csv_file = form.cleaned_data["csv_file"]
#         selected_bank = self.request.POST.get("bank", "")
#
#         bank_parser_mapping = {
#             "santander": SantanderCSVParser,
#             "nest": NestCSVParser,
#             "revolut": RevolutCSVParser,
#         }
#
#         parser_class = bank_parser_mapping.get(selected_bank)
#
#         if parser_class:
#             parser = parser_class()
#
#         csv_file_instance = CSVFile.objects.create(user=self.request.user, csv_file=csv_file)
#
#         csv_file_path = csv_file_instance.csv_file.path
#
#         parsed_data = parser.parse_csv(csv_file_path, user=self.request.user)
#         incomes, expenses = parsed_data
#
#         return self.render_to_response({"form": form, "incomes": incomes, "expenses": expenses})
