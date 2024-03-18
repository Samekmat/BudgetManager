# Content of Project
* [General info](#general-info)
* [Technologies](#technologies--tools)
* [Setup](#setup)
* [Functionalities](#functionalities)
* [Application view](#application-view)
* [Video showcase](#video-showcase)

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
<h4>
To use Budget Manager app, it is required to have an account. There is custom register, login, logout and profile creation
using django signals.
</h4>
</ul>

2. Index view:
<ul>
<h4>
Index view is responsible for displaying currency exchange rates based on currencies existing in database.
It also show expense comparison by category, which is a status of the current month expenses compared percentage
to the previous expenses, it has 3 values(decreased, increased, unchanged).
At the end we have expense forecast which calculates average spending's for the next month.
</h4>
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
Categories and Tags contains base crud for easy management and filter with pagination to easily find specific ones:
</h4>
</ul>

6. Saving goals:
<ul>
<h4>This section contains crud but also adding and subtracting amounts from the goals</h4>
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

## Additional resources
<ul>
<li>Fixtures to preload initial data -> categories, currencies and tags: helper_models/fixtures</li>

```commandline
python manage.py loaddata 'fixture'
```

<li>Sample bills and CSV's  - > resources</li>
</ul>


## Application view

### Screenshots

<details>
<summary>Show Screens</summary>

<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/2a3f8a5d-35fc-4e77-9d2e-90aa4e5a8c01" width="45%" alt="Darkmode index img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/e3b12fb9-6585-4f33-9f6c-09dd3e6fa44b" width="45%" alt="Expenses img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/e308944f-ec19-45a6-87fc-0511529e1888" width="45%" alt="Income add img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/260dcf54-ff57-4e8c-b4dd-ebfed43584b7" width="45%" alt="OCR view img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/da5a2638-88f1-4aa9-b59d-44c3d6d10d07" width="45%" alt="Login img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/7c363a69-9382-48b6-840b-e884e8435427" width="45%" alt="Register img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/10f35fcb-35d7-4314-870a-b46e2f761a49" width="45%" alt="Categories img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/9a2e257a-1b9a-4617-a408-bec56661b739" width="45%" alt="Saving goal view img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/7d110b6b-bacf-425b-9c65-b3b5e78e47df" width="45%" alt="Dashboard img"></img>
<img src="https://github.com/Samekmat/BudgetManager/assets/32867793/83b57bc2-7dd6-45c8-bc73-566716c0df20" width="45%" alt="Budget view charts img"></img>
</details>

### Video showcase
[<img src="https://cdn.loom.com/sessions/thumbnails/0cb822939e2c432190c217c0ee6a301b-with-play.gif" width="50%">](https://www.loom.com/embed/0cb822939e2c432190c217c0ee6a301b?sid=fab91a0c-88b8-4502-af7c-d5d6d37136fe)
