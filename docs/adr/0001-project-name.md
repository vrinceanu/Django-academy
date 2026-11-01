# ADR 0001: The project is named `django`

Date: 2026-11-01. Status: accepted.

## Decision

The repository, folder (`LMS/django`), Docker Compose project and deployed services
are named `django`. This replaces the working name `chips-lms` used in the design doc.

## Consequence

No Python package inside the repo may be importable as `django`, because it would
shadow the Django framework. The settings package stays `config` and the apps stay
under `apps.*`. Container images are `django-api` and `django-web`.
