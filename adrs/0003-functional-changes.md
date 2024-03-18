# Title
Date: `2024-03-17`

## Status
Accepted

## Functionalities
> - User profile
> - Authentication
> - Expense tracking
> - Income management
> - CRUD for income and expenses
> - Scan receipt or invoice (ocr lib)
> - Built-in categories of expenses
> - CRUD for custom categories of expenses
> - Categories and payment_methods of expenses (must, need, want) | (cash, card)
> - Display recent payments/expenses
> - Create graph/chart of budget
> - Compare month/category in case of expenses have increased or decreased
> - Summary of chosen period (from-to)
> - Create saving goal
> - ~~Possibility to add regular payments into home budget~~
> - Export to csv/pdf
> - Currency selection with loading exchange rate
> - Joining someone to shared budget
> - Filter by category and time
> - ~~Bill reminder~~
> - Toast operations
> - * ~~Reading data from wallets(google)~~
> - * ~~Integrate with bank to count expenses and incomes~~
> - * ~~Automatically assign categories to transaction~~
> - * Expense forecasting
> - * ~~Expense approval in shared budget~~

## Context
> We provided updated functional requirements of functionalities.

## Decision
> - We cut off some low impact functionalities but also the ones that became the problem to handle because of accessibility to some services.

## Changes
1) ### Forgiven
> Reading data from google wallet, regular payments, bill reminder, auto assign categories, expense approval
2) ### Changed
> Integrate with bank > Load csv from the chosen bank

## Consequences
> - We decided to cut off some functionalities that are not as good as we thought at the beginning, but also gave up hard to get google wallet api key.
> - Secondly, changed approach from bank integration to just load the bank transactions using csv files.

## Keywords
- functionality change
- ideas for project
- requirements
- changes
