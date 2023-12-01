from budget_manager.budget_manager_app.factories import SavingGoalFactory, CurrencyFactory


def test_new_saving_goal():
    factory = SavingGoalFactory()
    currency = CurrencyFactory()
    saving_goal = factory.create(name='new computer', currency=currency)
    assert saving_goal.name == 'new computer'
    assert saving_goal.currency is not None
