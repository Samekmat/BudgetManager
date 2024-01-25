"""URL configuration for budget_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from budget_manager_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    # apps
    path("api/", include("api.urls")),
    path("users/", include("users.urls")),
    path("", include("incomes.urls")),
    path("", include("expenses.urls")),
    path("", include("helper_models.urls")),
    path("", include("budget_manager_app.urls")),
    path("", include("saving_goals.urls")),
    path("", include("csv_files.urls")),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
