from typing import Any, Dict, List, Union

import plotly.graph_objects as go
from django.db.models import Sum
from plotly.offline import plot

BG_COLOR = "#d1d5db"
PLOT_BGCOLOR = "#e5e7eb"


class ChartsBudgetsGenerator:
    @staticmethod
    def generate_bar_chart(context: Dict[str, Union[List[Dict[str, Any]], float]]) -> str:
        """Generate a bar chart comparing total incomes and total expenses.

        Args:
        - context (Dict): Dictionary containing incomes and expenses data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

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
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=PLOT_BGCOLOR,
        )

        return plot(fig, output_type="div")

    @staticmethod
    def generate_pie_chart(context: Dict[str, Union[List[Dict[str, Any]], float]]) -> str:
        """Generate a pie chart representing the distribution of incomes and expenses.

        Args:
        - context (Dict): Dictionary containing incomes and expenses data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

        labels = ["Incomes", "Expenses"]
        values = [
            sum(item["total"] for item in context["incomes"]),
            sum(item["total"] for item in context["expenses"]),
        ]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, title="Incomes/Expenses")])
        fig.update_layout(paper_bgcolor=BG_COLOR, plot_bgcolor=PLOT_BGCOLOR)

        return plot(fig, output_type="div")

    @staticmethod
    def generate_budget_chart(context: Dict[str, Any]) -> str:
        """Generate an indicator chart for the total budget balance.

        Args:
        - context (Dict): Dictionary containing total_balance and budget data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

        total_balance = context["total_balance"]

        fig = go.Figure(
            go.Indicator(
                mode="number+delta",
                value=total_balance,
                title="Total Balance",
                number={"suffix": f" {context['budget'].currency.symbol}"},
            )
        )

        fig.update_layout(paper_bgcolor=BG_COLOR, plot_bgcolor=PLOT_BGCOLOR)
        return plot(fig, output_type="div")

    @staticmethod
    def generate_income_category_pie_chart(context: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate a pie chart representing the distribution of incomes across
        categories.

        Args:
        - context (Dict): Dictionary containing income categories data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

        labels = [item["category__name"] for item in context["income_categories"]]
        values = [item["total"] for item in context["income_categories"]]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title="Income Categories", paper_bgcolor=BG_COLOR, plot_bgcolor=PLOT_BGCOLOR)

        return plot(fig, output_type="div")

    @staticmethod
    def generate_expense_category_pie_chart(context: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate a pie chart representing the distribution of expenses across
        categories.

        Args:
        - context (Dict): Dictionary containing expense categories data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

        labels = [item["category__name"] for item in context["expense_categories"]]
        values = [item["total"] for item in context["expense_categories"]]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        fig.update_layout(title="Expense Categories", paper_bgcolor=BG_COLOR, plot_bgcolor=PLOT_BGCOLOR)

        return plot(fig, output_type="div")

    @staticmethod
    def generate_line_chart(context: Dict[str, Any]) -> str:
        """Generate a line chart representing the budget overview.

        Args:
        - context (Dict): Dictionary containing budget overview data.

        Returns:
        - str: The generated chart as an HTML div string.
        """

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
            paper_bgcolor=BG_COLOR,
            plot_bgcolor=PLOT_BGCOLOR,
        )

        chart_div = plot(fig, output_type="div", include_plotlyjs=False)

        return chart_div
