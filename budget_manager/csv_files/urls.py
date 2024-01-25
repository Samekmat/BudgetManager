from csv_files import views
from django.urls import path

app_name = "csv_files"

urlpatterns = [
    path("upload-csv/", views.CSVUploadView.as_view(), name="upload-csv"),
]
