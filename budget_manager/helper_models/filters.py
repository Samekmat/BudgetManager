import django_filters
from budget_manager_app.choices import CATEGORY_TYPES
from budget_manager_app.styles import CLASSES
from django import forms
from helper_models.models import Category, Tag


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": CLASSES}),
    )
    type = django_filters.ChoiceFilter(
        field_name="type",
        choices=CATEGORY_TYPES,
        widget=forms.Select(attrs={"class": CLASSES}),
    )

    class Meta:
        model = Category
        fields = ("name", "type")


class TagFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=forms.TextInput(attrs={"class": CLASSES}),
    )

    class Meta:
        model = Tag
        fields = ("name",)
