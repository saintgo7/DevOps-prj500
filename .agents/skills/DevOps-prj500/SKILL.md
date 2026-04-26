```markdown
# DevOps-prj500 Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill teaches you how to contribute to the `DevOps-prj500` TypeScript codebase, which is organized for full-stack development without a specific frontend framework. You'll learn the project's coding conventions, how to add new business domains with database and API support, expand internationalization (i18n), document architectural decisions, implement equity and safety guardrails, and create content approval workflows. The guide includes step-by-step instructions and code examples for each workflow, as well as the commands to streamline common tasks.

---

## Coding Conventions

### File Naming

- Use **camelCase** for file and directory names.
  - Example: `userProfile.ts`, `contentApprovalWorkflow.ts`

### Imports

- Use **relative imports** for internal modules.
  ```typescript
  import { getUser } from './userService';
  ```

### Exports

- Prefer **named exports**.
  ```typescript
  // Good
  export function approveContent() { ... }
  export const APPROVAL_PENDING = 'pending';

  // Avoid default exports
  // export default function() { ... }
  ```

---

## Workflows

### Add New Domain with API and Database

**Trigger:** When introducing a new business domain (e.g., columns, research, funding) with backend and API support.  
**Command:** `/new-domain`

1. **Edit Prisma Schema**
   - Add new models/tables in `apps/api/prisma/schema.prisma`.
   ```prisma
   model Research {
     id        String   @id @default(uuid())
     title     String
     createdAt DateTime @default(now())
     // ...other fields
   }
   ```
2. **Create a Migration**
   - Run Prisma migration to generate a new folder in `apps/api/prisma/migrations/`.
   ```bash
   npx prisma migrate dev --name add-research
   ```
3. **Seed Data**
   - Update `apps/api/prisma/seed.ts` or add a new file in `apps/api/prisma/seed/`.
   ```typescript
   // apps/api/prisma/seed/researchSeed.ts
   export async function seedResearch(prisma) {
     await prisma.research.create({ data: { title: 'Sample Research' } });
   }
   ```
4. **Implement API Module/Controller/Service**
   - Create files in `apps/api/src/research/`:
     - `research.module.ts`
     - `research.controller.ts`
     - `research.service.ts`
   ```typescript
   // research.controller.ts
   import { Controller, Get } from '@nestjs/common';
   import { ResearchService } from './research.service';

   @Controller('research')
   export class ResearchController {
     constructor(private readonly service: ResearchService) {}

     @Get()
     getAll() {
       return this.service.findAll();
     }
   }
   ```
5. **Add Tests**
   - Add unit/integration tests in `apps/api/src/research/research.service.spec.ts`.
   ```typescript
   import { describe, it, expect } from 'vitest';
   import { ResearchService } from './research.service';

   describe('ResearchService', () => {
     it('should return all research items', async () => {
       // test logic
     });
   });
   ```
6. **Update i18n Messages**
   - Add or update `apps/web/messages/{locale}.json`.
   ```json
   {
     "research.title": "Research",
     "research.description": "Research projects and findings"
   }
   ```
7. **Document in ADR**
   - Write an ADR in `docs/adr/xxxx-research.md` describing the design and decisions.

---

### Expand i18n Locales and Messages

**Trigger:** When adding support for more languages or new message namespaces.  
**Command:** `/add-locale`

1. **Add/Update Message Catalogs**
   - Edit `apps/web/messages/{locale}.json` for each supported locale.
2. **Update Locale Negotiation Logic**
   - Modify `apps/web/src/i18n/routing.ts` or `apps/api/src/i18n/locale.middleware.ts` as needed.
   ```typescript
   // Example: apps/web/src/i18n/routing.ts
   export function negotiateLocale(acceptLanguage: string) { ... }
   ```
3. **Add Message Namespaces**
   - Ensure new features have corresponding keys in each locale file.
4. **Translate or Stub Terms**
   - Provide translations or placeholders for all technical and plain-language terms.
5. **Update Tests**
   - Update or add tests for locale negotiation in `apps/api/src/i18n/locale.middleware.spec.ts`.

---

### Add ADR for Major Feature or Policy

**Trigger:** When documenting a significant architectural or policy decision.  
**Command:** `/new-adr`

1. **Write a New ADR**
   - Create a markdown file in `docs/adr/` with a sequential number and descriptive name.
   ```markdown
   # ADR 0005: Introduce Research Domain

   ## Context
   ...

   ## Decision
   ...
   ```
2. **Describe Context, Decision, Consequences, Rationale**
   - Use clear sections in the ADR.
3. **Link the ADR**
   - Reference it in `docs/README.md` or other relevant docs.
4. **Reference in Commits/PRs**
   - Mention the ADR number in related commit messages and pull requests.

---

### Full-Stack Feature with Equity Guardrails

**Trigger:** When implementing a new feature that must comply with equity and safety principles.  
**Command:** `/new-feature-guardrails`

1. **Design Models and Migrations**
   - Add models and constraints in `schema.prisma`.
2. **Implement RLS and Guardrails**
   - Enforce row-level security and equity/safety constraints in migrations and service logic.
   ```prisma
   // Example: Add a 'visibility' field for RLS
   model Content {
     id         String
     visibility String // e.g., 'public', 'private', 'restricted'
     // ...
   }
   ```
   ```typescript
   // In service
   if (user.role !== 'admin' && content.visibility !== 'public') {
     throw new Error('Access denied');
   }
   ```
3. **Update API Endpoints**
   - Add or modify controller/service files.
4. **Update i18n Messages**
   - Add plain-language and safety warning messages in all locales.
5. **Add/Update Tests**
   - Test for guardrails (e.g., noncommercial notices, harmful content guards).
6. **Document in ADR**
   - Write an ADR describing the workflow and guardrails.

---

### Add or Enhance Content Approval Workflow

**Trigger:** When ensuring content is reviewed and approved by humans before publication.  
**Command:** `/add-approval-workflow`

1. **Update Approval Models**
   - Add/modify approval-related models in `schema.prisma` and run migration.
2. **Implement Approval Logic**
   - Add approval token/signature logic (e.g., HMAC, expiry).
   ```typescript
   import crypto from 'crypto';
   function generateApprovalToken(contentId: string) {
     return crypto.createHmac('sha256', process.env.SECRET)
       .update(contentId + Date.now())
       .digest('hex');
   }
   ```
3. **Controller/Service Logic**
   - Implement state transitions for approval in controller/service files.
4. **Audit Logging**
   - Log all approval/rejection actions for traceability.
5. **Add/Update Tests**
   - Test approval flow, token security, and edge cases.
6. **Update i18n Messages**
   - Add approval state messages in all locales.
7. **Document in ADR**
   - Describe the workflow in an ADR.

---

## Testing Patterns

- **Framework:** [vitest](https://vitest.dev/)
- **Test File Pattern:** `*.spec.ts`
- **Placement:** Tests are placed alongside implementation files in the same directory.
- **Example:**
  ```typescript
  // apps/api/src/research/research.service.spec.ts
  import { describe, it, expect } from 'vitest';
  import { ResearchService } from './research.service';

  describe('ResearchService', () => {
    it('should fetch research items', async () => {
      // test logic
    });
  });
  ```

---

## Commands

| Command                   | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| /new-domain               | Add a new business/domain feature with API and database support          |
| /add-locale               | Add or expand i18n locales and message catalogs                         |
| /new-adr                  | Document a major architectural or policy decision as an ADR             |
| /new-feature-guardrails   | Implement a full-stack feature with equity and safety guardrails        |
| /add-approval-workflow    | Add or enhance a human-in-the-loop content approval workflow            |
```
