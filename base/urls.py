from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from budget_manager_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    # apps
    path("api/", include("api.urls")),
    path("users/", include("users.urls")),
    path("", include("incomes.urls")),
    path("", include("expenses.urls")),
    path("", include("helper_models.urls")),
    path("", include("budget_manager_app.urls")),
    path("", include("saving_goals.urls")),
    path("", include("file_parsers.urls")),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
#     urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
