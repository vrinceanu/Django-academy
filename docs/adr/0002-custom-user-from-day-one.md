# ADR 0002: Custom user model in the first migration

Date: 2026-11-01. Status: accepted.

## Decision

`accounts.User` exists from M0, before any other app migrates: UUID primary key,
the Network email as the login, no username, unusable password by default (people
sign in with Google from M1).

## Why

Django fixes `AUTH_USER_MODEL` at the first `migrate`. Switching later means
rewriting every migration that references the user. M1 extends the model (roles,
school, MFA for staff) without changing its identity.
