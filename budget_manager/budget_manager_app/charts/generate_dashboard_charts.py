import plotly.graph_objects as go
from django.db.models import Sum
from plotly.offline import plot


class ChartsDashboardGenerator:
    @staticmethod
    def generate_line_chart(form, expenses, incomes):
        if form.is_valid():
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            currency = form.cleaned_data.get("currency")

            expenses = ChartsDashboardGenerator.filter_data(expenses, date_from, date_to, currency)
            incomes = ChartsDashboardGenerator.filter_data(incomes, date_from, date_to, currency)

            expenses = expenses.values("date").annotate(total_amount=Sum("amount")).order_by("date")
            incomes = incomes.values("date").annotate(total_amount=Sum("amount")).order_by("date")

            if expenses.exists() or incomes.exists():
                expense_dates = list(expenses.values_list("date", flat=True))
                income_dates = list(incomes.values_list("date", flat=True))

                expense_amounts = list(expenses.values_list("total_amount", flat=True))
                income_amounts = list(incomes.values_list("total_amount", flat=True))

                # Convert expenses to negative values
                expense_amounts = [-amount for amount in expense_amounts]

                expense_trace = go.Scatter(
                    x=expense_dates,
                    y=expense_amounts,
                    mode="lines+markers",
                    name="Expenses",
                    line=dict(color="#FA7070"),
                )
                income_trace = go.Scatter(
                    x=income_dates,
                    y=income_amounts,
                    mode="lines+markers",
                    name="Incomes",
                    line=dict(color="#557C55"),
                )

                data = [expense_trace, income_trace]
                graph = go.Figure(data)

                title = "Income and Expense Line chart"
                graph.update_layout(title_text=title)

                line_chart = graph.to_html(full_html=False, default_height=500, default_width=700)
                return line_chart

    @staticmethod
    def generate_pie_chart(model, date_from, date_to, currency, title):
        filtered_data = model.objects.filter(currency=currency)

        if date_from and date_to:
            filtered_data = filtered_data.filter(date__range=(date_from, date_to))

        if filtered_data.exists():
            categories = filtered_data.values("category__name").annotate(total_amount=Sum("amount"))

            category_names = list(categories.values_list("category__name", flat=True))
            category_amounts = list(categories.values_list("total_amount", flat=True))

            data = go.Pie(labels=category_names, values=category_amounts)
            fig = go.Figure(data)
            fig.update_layout(title=title)

            return plot(fig, output_type="div")

    @staticmethod
    def generate_percentage_bar_chart(form, expenses, incomes):
        if form.is_valid():
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            currency = form.cleaned_data.get("currency")

            expenses = ChartsDashboardGenerator.filter_data(expenses, date_from, date_to, currency)
            incomes = ChartsDashboardGenerator.filter_data(incomes, date_from, date_to, currency)

            total_expenses = expenses.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
            total_incomes = incomes.aggregate(total_amount=Sum("amount"))["total_amount"] or 0
            total = total_expenses + total_incomes

            if total > 0:
                expense_percentage = (total_expenses / total) * 100
                income_percentage = (total_incomes / total) * 100

                # Creating the bar chart
                labels = ["Expenses", "Incomes"]
                values = [expense_percentage, income_percentage]

                data = go.Bar(
                    x=labels,
                    y=values,
                    text=values,
                    textposition="auto",
                    marker=dict(color=["#FA7070", "#557C55"]),
                )

                fig = go.Figure(data)
                fig.update_traces(texttemplate="%{text:.2s}%", textfont_size=14)

                title = "Percentage of Incomes and Expenses"
                fig.update_layout(
                    title=title,
                    xaxis=dict(title="Category"),
                    yaxis=dict(title="Percentage"),
                )

                return plot(fig, output_type="div")

    @staticmethod
    def filter_data(data, date_from, date_to, currency):
        filters = {}
        if date_from:
            filters["date__gte"] = date_from
        if date_to:
            filters["date__lte"] = date_to
        if currency:
            filters["currency"] = currency

        if filters:
            data = data.filter(**filters)
        return data
