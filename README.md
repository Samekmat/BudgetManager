# Content of Project
* [General info](#general-info)
* [Technologies](#technologies--tools)
* [Setup](#setup)
* [Functionalities](#functionalities)
* [Application view](#application-view)

## General info
<details>
<summary>Click here to see general information about <b>BudgetManager Project</b>!</summary>
<b>BudgetManager</b> is a project dedicated to tracking and managing earnings and spending. With features like income and expense tracking, customizable budgets, goal settings, various options to upload your data, and generating charts to visualize that data.
</details>

## Technologies & Tools
<ul>
    <li>Python</li>
    <li>Django</li>
    <li>Plotly for charts</li>
    <li>Poetry</li>
    <li>PostgreSQL</li>
    <li>Docker | Docker Compose</li>
    <li>AWS(EB, S3, RDS)</li>
    <li>Tesseract engine with Pytesseract</li>
    <li>Pre-commit</li>
    <li>GitHub actions for CI</li>
    <li>HTML + Tailwind CSS with Flowbite components</li>
    <li>JavaScript</li>
</ul>

## Prerequisites
1) Python
2) Docker
3) Tesseract engine if running local


## Setup
 Get freecurrencyapi key from https://app.freecurrencyapi.com/login

### Local
1) Download and install tesseract engine from https://github.com/tesseract-ocr/tesseract

2) Clone repository from GitHub
```bash
git clone https://github.com/Samekmat/BudgetManager.git
```
3) Install dependencies
```bash
poetry install
```
4) Configure .env variables using base/.env.dist examples

5) Run server on localhost
```bash
python manage.py runserver
```


### Docker

1) Clone repository from GitHub
```bash
git clone https://github.com/Samekmat/BudgetManager.git
```

2) Configure .env variables using base/.env.dist examples

3) Build containers based on docker-compose.yml
```bash
docker compose -f .\.docker\docker-compsoe.yml up -d --build
```

## Functionalities
<details>
<summary>Click here to see all project functionalities</summary>

1. Custom user authentication:
<ul>
<li>
<h4>
To use Budget Manager app, it is required to have an account. There is custom register, login, logout and profile creation
using django signals.
</h4>
</li>
</ul>

2. Index view:
<ul>
<li>
<h4>
Index view is responsible for displaying currency exchange rates based on currencies existing in database.
It also show expense comparison by category, which is a status of the current month expenses compared percentage
to the previous expenses, it has 3 values(decreased, increased, unchanged).
At the end we have expense forecast which calculates average spending's for the next month.
</h4>
</li>
</ul>


3. Dashboard:
<ul>
<h4>Dashboard is serving two functionalities:</h4>
<li>Recent transactions:</li>
As name calls, it displays two newest expenses with two newest incomes.
<li>Expense and Income Charts:</li>
Here we need to specify date range and currency to select data for graph generation
(line chart, percentage charts and pie charts).
</ul>

4. Incomes and Expenses:
<ul>
<h4>Incomes and expenses have the same features which are:</h4>
<li>List with filter and pagination</li>
<li>Add new income/expense by form</li>
<li>Add new income/expense by image of a bill or invoice</li>
<li>Update</li>
<li>Delete</li>
<li>Export to csv</li>
<li>Export to pdf</li>
</ul>

5. Categories and Tags section:
<ul>
<h4>
<li>
Categories and Tags contains base crud for easy management and filter with pagination to easily find specific ones:
</li>
</h4>
</ul>

6. Saving goals:
<ul>
<li>
<h4>This section contains crud but also adding and subtracting amounts from the goals</h4>
</li>
</ul>

7. Budgets:
<ul>
<h4>Crud and features connected with budgets</h4>
<li>Crud</li>
<li>Share budget with another user</li>
<li>Specify budget currency</li>
<li>Select goals that will be connected with budget</li>
<li>Add incomes/expenses to a budget</li>
<li>Generate budget charts</li>

</ul>
</details>

## Application view

### Screenshots
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/2a3f8a5d-35fc-4e77-9d2e-90aa4e5a8c01" width="50%" height="50%" alt="Darkmode index"></img>
### Video showcase
