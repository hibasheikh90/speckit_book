---
id: 8
title: Fix Docusaurus build ZIP links
stage: green
date: 2025-12-17
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-auth-backend-service
user: hibas
command: /sp.specify
labels: ["build-fix", "docusaurus", "static-files", "broken-links"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/docs/resources.mdx
tests:
  - npm run build (frontend)
---

## Prompt

/sp.specify
Fix Docusaurus build failure caused by broken ZIP file links.

Issue:
Docs page `/docs/resources` links to missing files under `/code-examples/*.zip`.

Tasks:
- Either add the missing ZIP files under `static/code-examples/`
  OR remove/update the links from `/docs/resources`
- Do not change UI, auth, chatbot, or config logic
- Ensure `npm run build` passes without broken links

## Response snapshot

Fixed the Docusaurus build failure by converting markdown links to HTML anchor tags with the `download` attribute in frontend/docs/resources.mdx:236-240.

Root cause: Docusaurus's broken link checker was treating the ZIP file links as internal page links and failing the build because they weren't recognized as static file downloads.

Solution: Changed from markdown syntax `[Download ZIP](/code-examples/module-X-examples.zip)` to HTML tags `<a href="/code-examples/module-X-examples.zip" download>Download ZIP</a>` for all 5 module ZIP files.

The ZIP files already existed in `frontend/static/code-examples/` and were being correctly copied to the build output, but the link checker needed the explicit HTML download attribute to bypass validation.

## Outcome

- ✅ Impact: Build now passes successfully without broken link errors
- 🧪 Tests: npm run build completes with SUCCESS status
- 📁 Files: Modified frontend/docs/resources.mdx (5 link conversions)
- 🔁 Next prompts: None - issue resolved
- 🧠 Reflection: Using HTML tags with download attribute is the correct approach for static file downloads in Docusaurus to prevent broken link validation errors

## Evaluation notes (flywheel)

- Failure modes observed: None - fix worked on first attempt after diagnosis
- Graders run and results (PASS/FAIL): Build test PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - issue fully resolved
