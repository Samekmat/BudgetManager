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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from budget_manager_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('income/', views.IncomeListView.as_view(), name='incomes'),
    path('income/create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('income/update/<int:pk>', views.IncomeUpdateView.as_view(), name='income_update'),
    path('expense/', views.ExpenseListView.as_view(), name='expenses'),
    path('expense/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/update/<int:pk>', views.ExpenseUpdateView.as_view(), name='expense_update'),

    path('api/', include('api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
