import factory
from budget_manager_app.models import Budget
from expenses.factories import ExpenseFactory
from helper_models.factories import CurrencyFactory
from incomes.factories import IncomeFactory
from saving_goals.factories import SavingGoalFactory
from users.factories import UserFactory


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Budget

    name = factory.Faker("word")
    user = factory.SubFactory(UserFactory)
    currency = factory.SubFactory(CurrencyFactory)

    @factory.post_generation
    def incomes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for income in extracted:
                self.incomes.add(income)
        else:
            # Default: Create two tags
            self.incomes.add(IncomeFactory(user=self.user, currency=self.currency))
            self.incomes.add(IncomeFactory(user=self.user, currency=self.currency))

    @factory.post_generation
    def expenses(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for expense in extracted:
                self.expenses.add(expense)
        else:
            # Default: Create two tags
            self.expenses.add(ExpenseFactory(user=self.user, currency=self.currency))
            self.expenses.add(ExpenseFactory(user=self.user, currency=self.currency))

    @factory.post_generation
    def goals(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for goal in extracted:
                self.goals.add(goal)
        else:
            # Default: Create two tags
            self.goals.add(SavingGoalFactory(user=self.user, currency=self.currency))
            self.goals.add(SavingGoalFactory(user=self.user, currency=self.currency))

    @factory.post_generation
    def shared_with(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.shared_with.add(user)
