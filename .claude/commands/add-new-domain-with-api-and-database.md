---
name: add-new-domain-with-api-and-database
description: Workflow command scaffold for add-new-domain-with-api-and-database in DevOps-prj500.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-new-domain-with-api-and-database

Use this workflow when working on **add-new-domain-with-api-and-database** in `DevOps-prj500`.

## Goal

Adds a new business/domain feature with full-stack implementation: database schema, migration, seed data, API module/controller/service, tests, and i18n messages.

## Common Files

- `apps/api/prisma/schema.prisma`
- `apps/api/prisma/migrations/*/migration.sql`
- `apps/api/prisma/seed.ts`
- `apps/api/prisma/seed/*.ts`
- `apps/api/src/{domain}/*.ts`
- `apps/api/src/{domain}/*.spec.ts`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit apps/api/prisma/schema.prisma to add new models/tables.
- Create a migration in apps/api/prisma/migrations/ with a timestamped folder and migration.sql.
- Update or add seed data in apps/api/prisma/seed.ts or a new seed/*.ts file.
- Implement new module/controller/service in apps/api/src/{domain}/ (e.g., {domain}.module.ts, {domain}.controller.ts, {domain}.service.ts).
- Add unit/integration tests in apps/api/src/{domain}/*.spec.ts.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.