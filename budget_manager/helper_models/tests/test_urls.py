from django.test import TestCase
from django.urls import resolve, reverse
from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    TagFactory,
)
from helper_models.views import (
    CategoryCreateView,
    CategoryListView,
    CategoryUpdateView,
    TagCreateView,
    TagListView,
    TagUpdateView,
)


class CategoryUrlsTestcase(TestCase):
    def setUp(self):
        self.category_income = CategoryIncomeFactory()
        self.category_expense = CategoryExpenseFactory()

        # Urls
        self.list_url = reverse("helper_models:categories")
        self.create_url = reverse("helper_models:category-create")
        self.cat_inc_update_url = reverse("helper_models:category-update", kwargs={"pk": self.category_income.id})
        self.cat_exp_update_url = reverse("helper_models:category-update", kwargs={"pk": self.category_expense.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, CategoryListView)
        self.assertEqual(resolve(self.create_url).func.view_class, CategoryCreateView)
        self.assertEqual(resolve(self.cat_inc_update_url).func.view_class, CategoryUpdateView)
        self.assertEqual(resolve(self.cat_exp_update_url).func.view_class, CategoryUpdateView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/categories/")
        self.assertEqual(self.create_url, "/categories/create/")
        self.assertEqual(self.cat_inc_update_url, f"/categories/{self.category_income.id}/update/")
        self.assertEqual(self.cat_exp_update_url, f"/categories/{self.category_expense.id}/update/")


class TagUrlsTestcase(TestCase):
    def setUp(self):
        self.tag = TagFactory()

        self.list_url = reverse("helper_models:tags")
        self.create_url = reverse("helper_models:tag-create")
        self.update_url = reverse("helper_models:tag-update", kwargs={"pk": self.tag.id})

    def test_urls_resolves(self):
        self.assertEqual(resolve(self.list_url).func.view_class, TagListView)
        self.assertEqual(resolve(self.create_url).func.view_class, TagCreateView)
        self.assertEqual(resolve(self.update_url).func.view_class, TagUpdateView)

    def test_urls_reverse(self):
        self.assertEqual(self.list_url, "/tags/")
        self.assertEqual(self.create_url, "/tags/create/")
        self.assertEqual(self.update_url, f"/tags/{self.tag.id}/update/")
