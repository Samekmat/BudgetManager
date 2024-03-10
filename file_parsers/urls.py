from django.urls import path

from file_parsers import views

app_name = "file_parsers"

urlpatterns = [
    path("upload-csv/", views.CSVUploadView.as_view(), name="upload-csv"),
]
