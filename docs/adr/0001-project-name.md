# ADR 0001: The project is named `django-academy`

Date: 2026-11-01. Status: accepted (renamed from `django` the same day).

## Decision

The repository, folder (`LMS/django-academy`), Docker Compose project and deployed
services are named `django-academy`. This replaces the working name `chips-lms` used in
the design doc, and the short-lived name `django`, which was too generic.

Container images are `django-academy-api` and `django-academy-web`; on the staging
VM the stack lives in `/opt/django-academy`.

## Consequence

Python packages keep their design names: settings in `config`, apps under `apps.*`.
Nothing inside the repo is importable as `django`, so the framework is never shadowed.
