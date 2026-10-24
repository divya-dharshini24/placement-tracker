# Placement Tracker

A web app where students track their job applications: company, role, status, deadlines and notes. Each student has their own account and sees only their own applications.

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

The 17 tests cover login protection, privacy between students, the dashboard logic, add, edit, delete, filtering and validation.

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