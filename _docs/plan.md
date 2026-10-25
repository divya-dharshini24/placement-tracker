# Placement Tracker - Specification

## Problem
Students applying for campus placements lose track of applications,
deadlines and statuses. This app gives each student one private place
to track them.

## Users
All students. Each student has their own account and sees only their own data.

## Application fields
Company, role, status (applied, test, interview, offer, rejected),
applied date, deadline date, deadline label (for example "Coding test"),
job posting link, notes, and a last-updated date that changes on every edit.

## Features
- Sign up, log in and log out
- Add, edit and delete applications
- Filter the list by status
- Dashboard: counts by status, upcoming deadlines (sorted by date), and
  applications with no update for more than 7 days

## Rules
- A deadline label needs a deadline date.
- One student can never see or change another student's applications.

## Later
- Status chart on the dashboard
- Search by company name