# Placement Tracker

A web app where students track their job applications: company, role, status, deadlines and notes. Each student has their own account and sees only their own applications.

## Problem

Students applying for campus placements lose track of applications, deadlines and statuses across many companies. This app gives each student one private place to see where every application stands and what needs attention next.

## Features

- Sign up, log in and log out (Django's built-in authentication)
- Add, edit and delete applications
- Filter applications by status
- Dashboard with:
  - counts by status (applied, test, interview, offer, rejected)
  - upcoming deadlines, soonest first
  - applications with no update for more than 7 days
- Each application stores: company, role, status, applied date, deadline date and label, job posting link, notes, and a last-updated time that changes on every edit

## Tech stack

- Python 3.9 and Django 4.2
- SQLite database by default, Postgres when run with Docker
- Django templates with Bootstrap for the pages

I used Django templates instead of a separate React frontend. This keeps it as one project with one command to run, while the frontend (templates and forms), backend (views) and database (models) are all connected.

## How to run

```bash
git clone https://github.com/divya-dharshini24/placement-tracker.git
cd placement-tracker
python -m venv venv
venv\Scripts\activate        # Windows (on Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/, click **Sign up**, create an account and add your first application.

To use the admin site, run `python manage.py createsuperuser` and open http://127.0.0.1:8000/admin/.

## How to run the tests

```bash
python manage.py test
```

The 17 tests cover login protection, privacy between students, the dashboard logic (counts by status, upcoming deadlines, the 7-day rule), add, edit, delete, filtering and validation. They use Django's test client against the real views and database.

## Run with Docker

The app can also run in Docker, with Postgres as the database. One command starts both the app and the database, so there is no need to install Python packages or a database on your computer.

**What you need:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and **running**.

**Start everything:**

```bash
docker compose up --build
```

The first run takes a few minutes while Docker builds the image. The database migrations are applied automatically when the app starts.

**Open the app** at http://127.0.0.1:8001/, then click **Sign up**, create an account and add your first application. (The app listens on port 8001 on your computer because port 8000 was blocked on mine. You can change it in `docker-compose.yml`.)

**Run the tests inside the container** (in a second terminal, while or after the app runs):

```bash
docker compose run --rm web python manage.py test
```

All 17 tests run against the Postgres database.

**Stop it:**

```bash
docker compose down
```

This stops the containers and keeps your data. To stop **and delete the database data**, use:

```bash
docker compose down -v
```

**Note:** the database user and password in `docker-compose.yml` are for local development only. Never reuse them for a real deployment.

## Project documents

- `AGENTS.md`: project overview, commands and rules for coding assistants
- `_docs/plan.md`: the product specification
- `_docs/process.md`: how work is organized
- `_docs/team/`: the PM, engineer and QA role descriptions
- Tasks and acceptance criteria are tracked in the repository's GitHub Issues

I built this project with an AI assistant guiding me step by step; I ran, tested and committed every change myself.

## Project structure

- `applications/models.py`: the Application model
- `applications/views.py`: dashboard, list, add, edit, delete and sign-up views
- `applications/forms.py`: the application form
- `applications/tests.py`: automated tests
- `applications/templates/`: page templates
- `jobtracker/`: project settings and URLs

## Future improvements

- Status chart on the dashboard
- Search by company name