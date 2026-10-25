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
- SQLite database
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

The 17 tests include:

- **Unit tests:** the dashboard logic (counts by status, upcoming deadlines, the 7-day rule) and form validation
- **Integration tests:** login protection, privacy between students, and add, edit, delete and filter, using Django's test client against the real views and database

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