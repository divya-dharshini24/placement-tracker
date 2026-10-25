# Placement Tracker

A Django app where each student tracks their own job applications.
Students sign up, add applications, and see a dashboard of their progress.

## Commands

- `pip install -r requirements.txt` - install dependencies
- `python manage.py migrate` - create the database
- `python manage.py runserver` - run the app
- `python manage.py test` - run all tests

## Rules

- A student may only see, edit or delete their own applications.
- Do not add dependencies without asking.
- Every change keeps `python manage.py test` passing.

## Documents

- `_docs/plan.md` - product specification
- `_docs/process.md` - how work is organized
- `_docs/team/pm.md` - the product manager role
- `_docs/team/software-engineer.md` - the engineer role
- `_docs/team/qa-engineer.md` - the QA role