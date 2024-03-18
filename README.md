# Content of Project
* [General info](#general-info)
* [Technologies](#technologies--tools)
* [Setup](#setup)
* [More detailed information about modules](#more-detailed-information-about-modules)
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
1) Docker

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
