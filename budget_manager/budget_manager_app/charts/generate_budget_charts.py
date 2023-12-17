import plotly.graph_objects as go
from django.db.models import Sum
from plotly.offline import plot


class ChartsGenerator:  # TODO ChartsBudgetsGenerator
    @staticmethod
    def generate_bar_chart(context):
        total_incomes = sum(item["total"] for item in context["incomes"])
        total_expenses = sum(item["total"] for item in context["expenses"])

        income_percentage = (total_incomes / (total_incomes + total_expenses)) * 100
        expense_percentage = (total_expenses / (total_incomes + total_expenses)) * 100

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Incomes"],
                y=[total_incomes],
                text=[f"{income_percentage:.2f}%"],
                name="Incomes",
            )
        )

        fig.add_trace(
            go.Bar(
                x=["Expenses"],
                y=[total_expenses],
                text=[f"{expense_percentage:.2f}%"],
                name="Expenses",
            )
        )

        fig.update_layout(
            title="Total Incomes vs Total Expenses",
            xaxis_title="",
            yaxis_title="Amount",
            barmode="group",
        )

        return plot(fig, output_type="div")

    @staticmethod
    def generate_pie_chart(context):
        labels = ["Incomes", "Expenses"]
        values = [
            sum(item["total"] for item in context["incomes"]),
            sum(item["total"] for item in context["expenses"]),
        ]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, title="Incomes/Expenses")])

        return plot(fig, output_type="div")

    @staticmethod
    def generate_budget_chart(context):
        total_balance = context["total_balance"]

        fig = go.Figure(
            go.Indicator(
                mode="number+delta",
                value=total_balance,
                title="Total Balance",
                number={"prefix": context["budget"].currency.symbol},
            )
        )

        return plot(fig, output_type="div")

    @staticmethod
    def generate_income_category_pie_chart(context):
        labels = [item["category__name"] for item in context["income_categories"]]
        values = [item["total"] for item in context["income_categories"]]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title="Income Categories")

        return plot(fig, output_type="div")

    @staticmethod
    def generate_expense_category_pie_chart(context):
        labels = [item["category__name"] for item in context["expense_categories"]]
        values = [item["total"] for item in context["expense_categories"]]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title="Expense Categories")

        return plot(fig, output_type="div")

    @staticmethod
    def generate_line_chart(context):
        income_data = context["budget"].incomes.values("date").annotate(total=Sum("amount")).order_by("date")
        income_dates = [item["date"] for item in income_data]
        income_totals = [item["total"] for item in income_data]

        expense_data = context["budget"].expenses.values("date").annotate(total=Sum("amount")).order_by("date")
        expense_dates = [item["date"] for item in expense_data]
        expense_totals = [-item["total"] for item in expense_data]

        all_dates = sorted(set(income_dates + expense_dates))

        daily_differences = []
        for date in all_dates:
            income = income_totals[income_dates.index(date)] if date in income_dates else 0
            expense = expense_totals[expense_dates.index(date)] if date in expense_dates else 0
            daily_differences.append(income + expense)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=income_dates, y=income_totals, mode="lines+markers", name="Income"))
        fig.add_trace(go.Scatter(x=expense_dates, y=expense_totals, mode="lines+markers", name="Expenses"))
        fig.add_trace(
            go.Scatter(
                x=all_dates,
                y=daily_differences,
                mode="lines+markers",
                name="Difference",
            )
        )

        fig.update_layout(
            title="Budget Overview",
            xaxis_title="Date",
            yaxis_title="Amount",
        )

        chart_div = plot(fig, output_type="div", include_plotlyjs=False)

        return chart_div
