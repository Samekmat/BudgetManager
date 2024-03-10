from django.test import TestCase

from budget_manager_app.forms import BudgetForm, ChartForm, IncomeExpenseSelectForm
from expenses.factories import ExpenseFactory
from helper_models.factories import CurrencyFactory
from incomes.factories import IncomeFactory
from saving_goals.factories import SavingGoalFactory
from users.factories import UserFactory


class ChartFormTest(TestCase):
    def test_chart_form_valid(self):
        currency = CurrencyFactory()
        form_data = {"date_from": "2022-01-01", "date_to": "2022-12-31", "currency": currency.id}
        form = ChartForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_chart_form_invalid(self):
        form_data = {"date_from": "2022-01-01", "date_to": "2022-12-31"}  # Missing 'currency'
        form = ChartForm(data=form_data)
        self.assertFalse(form.is_valid())


class BudgetFormTest(TestCase):
    def test_budget_form_valid(self):
        user = UserFactory()
        currency = CurrencyFactory()
        income = IncomeFactory(user=user, currency=currency)
        expense = ExpenseFactory(user=user, currency=currency)
        goal = SavingGoalFactory(user=user, currency=currency)
        form_data = {
            "name": "My Budget",
            "currency": currency.id,
            "shared_with": [user.id],
            "incomes": [income.id],
            "expenses": [expense.id],
            "goals": [goal.id],
        }
        form = BudgetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_budget_form_invalid(self):
        form_data = {"name": "My Budget"}
        form = BudgetForm(data=form_data)
        self.assertFalse(form.is_valid())


class IncomeExpenseSelectFormTest(TestCase):
    def test_income_expense_select_form_valid(self):
        income = IncomeFactory()
        expense = ExpenseFactory()
        form_data = {"incomes": [income.id], "expenses": [expense.id]}
        form = IncomeExpenseSelectForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_income_expense_select_form_invalid(self):
        form_data = {"incomes": [999], "expenses": [888]}
        form = IncomeExpenseSelectForm(data=form_data)
        self.assertFalse(form.is_valid())
