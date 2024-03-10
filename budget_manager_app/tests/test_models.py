from django.test import TestCase

from budget_manager_app.factories import BudgetFactory
from expenses.factories import ExpenseFactory
from helper_models.factories import CurrencyFactory
from incomes.factories import IncomeFactory
from saving_goals.factories import SavingGoalFactory
from users.factories import UserFactory


class BudgetModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.user3 = UserFactory()
        self.currency = CurrencyFactory()
        self.income1 = IncomeFactory()
        self.income2 = IncomeFactory()
        self.expense1 = ExpenseFactory()
        self.expense2 = ExpenseFactory()
        self.goal = SavingGoalFactory()

        self.budget = BudgetFactory(
            user=self.user,
            currency=self.currency,
            incomes=[self.income1, self.income2],
            expenses=[self.expense1, self.expense2],
            goals=[self.goal],
            shared_with=[self.user2, self.user3],
        )

    def test_calculate_balance(self):
        expected_balance = sum(income.amount for income in [self.income1, self.income2]) - sum(
            expense.amount for expense in [self.expense1, self.expense2]
        )

        actual_balance = self.budget.calculate_balance

        self.assertEqual(actual_balance, expected_balance)

    def test_calculate_balance_with_no_incomes_or_expenses(self):
        self.budget.incomes.set([])
        self.budget.expenses.set([])

        expected_balance = 0

        actual_balance = self.budget.calculate_balance

        self.assertEqual(actual_balance, expected_balance)

    def test_calculate_balance_with_shared_budget(self):
        shared_budget = BudgetFactory(
            user=self.user2,
            currency=self.currency,
            incomes=[IncomeFactory(), IncomeFactory()],
            expenses=[ExpenseFactory(), ExpenseFactory()],
            goals=[SavingGoalFactory()],
            shared_with=[self.user, self.user3],
        )

        expected_balance = sum(income.amount for income in shared_budget.incomes.all()) - sum(
            expense.amount for expense in shared_budget.expenses.all()
        )

        actual_balance = shared_budget.calculate_balance

        self.assertEqual(actual_balance, expected_balance)
