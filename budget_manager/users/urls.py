from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(template_name="logout.html"), name="logout"),
]
