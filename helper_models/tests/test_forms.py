from django.test import TestCase

from helper_models.factories import (
    CategoryExpenseFactory,
    CategoryIncomeFactory,
    TagFactory,
)
from helper_models.forms import CategoryForm, TagForm


class CategoryFormTestCase(TestCase):
    def setUp(self):
        self.category_income = CategoryIncomeFactory()
        self.category_expense = CategoryExpenseFactory()

    def test_category_form_valid_data(self):
        category_income_data = {
            "name": self.category_income.name,
            "type": self.category_income.type,
            "description": self.category_income.description,
            "user": self.category_income.user,
        }
        category_expense_data = {
            "name": self.category_expense.name,
            "type": self.category_expense.type,
            "description": self.category_expense.description,
            "user": self.category_expense.user,
        }
        category_income_form = CategoryForm(data=category_income_data)
        category_expense_form = CategoryForm(data=category_expense_data)
        self.assertTrue(category_income_form.is_valid())
        self.assertTrue(category_expense_form.is_valid())

    def test_category_form_invalid_data(self):
        category_income_data_invalid = {
            "name": 0,
            "type": self.category_income.type,
            "builtin": self.category_income.builtin,
            "user": self.category_income.user,
        }
        category_expense_data_invalid = {
            "name": self.category_expense.name,
            "type": 10,
            "builtin": self.category_expense.builtin,
            "user": self.category_expense.user,
        }
        category_income_form = CategoryForm(data=category_income_data_invalid)
        category_expense_form = CategoryForm(data=category_expense_data_invalid)
        self.assertFalse(category_income_form.is_valid())
        self.assertFalse(category_expense_form.is_valid())

    def test_category_form_empty_data(self):
        category_income_data_empty = {
            "name": "",
            "type": "",
            "builtin": "",
            "user": "",
        }
        category_expense_data_empty = {
            "name": "",
            "type": "",
            "builtin": "",
            "user": "",
        }
        category_income_form = CategoryForm(data=category_income_data_empty)
        category_expense_form = CategoryForm(data=category_expense_data_empty)
        self.assertFalse(category_income_form.is_valid())
        self.assertFalse(category_expense_form.is_valid())


class TagFormTestCase(TestCase):
    def setUp(self):
        self.tag = TagFactory()

    def test_tag_form_valid_data(self):
        tag_data = {"name": self.tag.name, "user": self.tag.user}
        form = TagForm(data=tag_data)
        self.assertTrue(form.is_valid())

    def test_tag_form_invalid_data(self):
        tag_data_invalid = {"name": "a" * 33, "user": self.tag.user}  # max len is a 32
        form = TagForm(data=tag_data_invalid)
        self.assertFalse(form.is_valid())

    def test_tag_form_empty_data(self):
        tag_data_empty = {"name": "", "user": ""}
        form = TagForm(data=tag_data_empty)
        self.assertFalse(form.is_valid())
