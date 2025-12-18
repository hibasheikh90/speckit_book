---
id: 10
title: Disable Docusaurus broken link checks
stage: general
date: 2025-12-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-fix-docusaurus-links
user: hibas
command: none
labels: ["docusaurus", "configuration", "build"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/docusaurus.config.ts
tests:
  - none
---

## Prompt

Disable Docusaurus broken link checks.
Set onBrokenLinks and onBrokenAnchors to "ignore" so the build passes without errors.

## Response snapshot

Updated `frontend/docusaurus.config.ts`:
- Changed `onBrokenLinks` from `'throw'` to `'ignore'` (line 28)
- Added `onBrokenAnchors: 'ignore'` (line 29)

This allows the Docusaurus build to complete successfully without failing on broken internal links or anchor references.

## Outcome

- ✅ Impact: Build will no longer fail due to broken links or anchors
- 🧪 Tests: No tests modified
- 📁 Files: Modified frontend/docusaurus.config.ts
- 🔁 Next prompts: Test build to verify configuration works as expected
- 🧠 Reflection: Minimal viable change - only modified the two configuration options needed

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Verify build passes with new configuration
