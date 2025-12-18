# Tasks: Fix Docusaurus Build Errors

**Input**: Design documents from `/specs/001-fix-docusaurus-links/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, quickstart.md ✅

**Tests**: No test tasks included - tests not requested in feature specification. Validation uses Docusaurus build verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Note that US1 and US3 (both P1) must be completed together as they represent the core fix workflow.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a documentation maintenance project:
- **Documentation files**: `frontend/docs/` (TARGET for all fixes)
- **Build validation**: `frontend/` directory for npm commands
- **Planning artifacts**: `specs/001-fix-docusaurus-links/`
- No code changes - purely markdown file edits

---

## Phase 1: Setup (Validation Infrastructure)

**Purpose**: Verify build environment and establish baseline

- [x] T001 Verify Node.js 20+ and npm are installed and accessible
- [x] T002 Verify Docusaurus dependencies installed in frontend/package.json
- [x] T003 Run baseline build to establish current state in frontend/ directory
- [x] T004 Capture baseline build output to specs/001-fix-docusaurus-links/build-baseline.log
- [x] T005 Verify strict link checking enabled (`onBrokenLinks: 'throw'`) in frontend/docusaurus.config.ts

**Checkpoint**: Environment validated, baseline established (current: 0 broken links, build passes)

---

## Phase 2: Foundational (Link Detection Framework)

**Purpose**: Core infrastructure for identifying broken links

**⚠️ CRITICAL**: This phase establishes the detection mechanism. If no broken links exist (current state), this serves as preventive documentation.

- [x] T006 Document current build status (exit code 0, no broken links) in specs/001-fix-docusaurus-links/current-state.md
- [x] T007 [P] Create validation checklist template based on quickstart.md in specs/001-fix-docusaurus-links/checklists/fix-validation.md
- [x] T008 [P] Document link pattern examples (from research.md) for future reference in specs/001-fix-docusaurus-links/link-patterns.md

**Checkpoint**: Foundation ready - if broken links are detected in future, fix workflow can begin

---

## Phase 3: User Story 1 - Build Success Without Link Errors (Priority: P1) 🎯 MVP

**Goal**: Ensure Docusaurus build completes successfully with exit code 0 and zero broken link errors

**Independent Test**: Run `npm run build` in frontend/ directory and verify:
- Exit code is 0
- No `[ERROR] Broken link` messages in output
- Build completes in <10 minutes

**Note**: Current state shows 0 broken links. Tasks below are for when/if broken links are detected in future.

### Link Detection for User Story 1

- [ ] T009 [US1] Run production build with strict checking in frontend/ directory using `npm run build`
- [ ] T010 [US1] Capture build output to specs/001-fix-docusaurus-links/build-errors.log
- [ ] T011 [US1] Parse build output to extract broken link errors (source file, target URL, line number)
- [ ] T012 [US1] Create broken links inventory in specs/001-fix-docusaurus-links/broken-links-list.md

### Link Fix Implementation for User Story 1

**Note**: Only execute if broken links detected in T009-T012. If build passes (current state), skip to checkpoint.

- [ ] T013 [US1] For each broken /docs/* link: locate source file in frontend/docs/
- [ ] T014 [US1] For each broken /code-examples/*.zip link: locate source file in frontend/docs/
- [ ] T015 [US1] Apply fix pattern: replace `[text](broken-url)` with `text` preserving all content
- [ ] T016 [US1] Save all modified markdown files in frontend/docs/ directory
- [ ] T017 [US1] Re-run build to verify all broken link errors resolved using `npm run build`
- [ ] T018 [US1] Verify build exit code is 0 (success)
- [ ] T019 [US1] Verify build output contains zero `[ERROR] Broken link` messages
- [ ] T020 [US1] Verify build time is <10 minutes (SC-001)

**Checkpoint**: At this point, build should pass with no broken link errors (US1 complete)

---

## Phase 4: User Story 3 - Preserved Content Integrity (Priority: P1)

**Goal**: Ensure all original content, structure, and functionality remain intact with only minimal changes to link markup

**Independent Test**: Compare documentation content before and after fixes using `git diff frontend/docs/` to verify:
- Only link markup removed (no content changes)
- No structural changes (files not moved/renamed)
- No config file modifications

**Note**: US3 must be validated immediately after US1 fixes. These are paired P1 priorities.

### Content Integrity Validation for User Story 3

- [ ] T021 [US3] Review git diff for frontend/docs/ directory to identify all changes
- [ ] T022 [US3] Verify ONLY link markup removed: pattern `[text](url)` → `text` (SC-005)
- [ ] T023 [US3] Verify no text content changes beyond link removal
- [ ] T024 [US3] Verify no file moves, renames, or deletions in frontend/docs/
- [ ] T025 [US3] Verify no changes to frontend/docusaurus.config.ts (unless explicitly needed for link validation)
- [ ] T026 [US3] Verify no changes to frontend/sidebars.ts
- [ ] T027 [US3] Verify no changes to frontend/src/ directory (UI components untouched)
- [ ] T028 [US3] Verify no changes to backend/ directory (auth/chatbot untouched)
- [ ] T029 [US3] Verify no changes outside frontend/docs/ except documentation artifacts (SC-006)
- [ ] T030 [US3] Read modified files to ensure sentences remain grammatically correct
- [ ] T031 [US3] Verify markdown syntax still valid (headers, lists, formatting preserved)

**Checkpoint**: All user stories 1 AND 3 should both work independently - build passes AND content integrity preserved

---

## Phase 5: User Story 2 - Clean Link References (Priority: P2)

**Goal**: Ensure documentation readers never encounter 404 errors when following links (preventive validation)

**Independent Test**: Navigate through documentation pages manually and click links to verify they resolve to valid pages

**Note**: This is preventive validation since current state has no broken links. Execute for quality assurance.

### Manual Navigation Validation for User Story 2

- [ ] T032 [P] [US2] Navigate to frontend/docs/intro.mdx in development mode (`npm run start`)
- [ ] T033 [P] [US2] Click all internal links in module-1-ros2/ documentation pages
- [ ] T034 [P] [US2] Click all internal links in module-2-simulation/ documentation pages
- [ ] T035 [P] [US2] Click all internal links in module-3-isaac/ documentation pages
- [ ] T036 [P] [US2] Click all internal links in module-4-vla/ documentation pages
- [ ] T037 [P] [US2] Click all internal links in module-5-capstone/ documentation pages
- [ ] T038 [P] [US2] Verify all links in faq.mdx, glossary.mdx, resources.mdx, prerequisites.mdx resolve
- [ ] T039 [US2] Verify no 404 errors encountered during navigation
- [ ] T040 [US2] Verify navigation flow remains logical (Next/Previous chapter links work)
- [ ] T041 [US2] Search for `/code-examples/` references using `grep -r "/code-examples/" frontend/docs/`
- [ ] T042 [US2] Verify any code example links point to existing files or have been removed

**Checkpoint**: All user stories (US1, US2, US3) should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates

- [ ] T043 [P] Update specs/001-fix-docusaurus-links/current-state.md with final build status
- [ ] T044 [P] Update specs/001-fix-docusaurus-links/broken-links-list.md with resolution details (if any fixes applied)
- [ ] T045 Run all success criteria validations from specs/001-fix-docusaurus-links/quickstart.md
- [ ] T046 Verify SC-001: Build completes in <10 minutes
- [ ] T047 Verify SC-002: Zero broken link errors in build output
- [ ] T048 Verify SC-003: 100% of internal /docs/* links resolve to valid pages
- [ ] T049 Verify SC-004: All /code-examples/*.zip links removed or corrected
- [ ] T050 Verify SC-005: Documentation content semantically unchanged
- [ ] T051 Verify SC-006: No files outside frontend/docs/ modified
- [ ] T052 Create git commit with message format from quickstart.md
- [ ] T053 Push to feature branch 001-fix-docusaurus-links
- [ ] T054 Verify remote build passes (if CI/CD configured)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion (T001-T005) - Documents current state
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion (T006-T008)
  - **Current State**: No broken links, so T013-T020 can be skipped
  - **Future State**: If broken links detected, execute T013-T020
- **User Story 3 (Phase 4)**: MUST execute immediately after US1 if fixes applied
  - **Current State**: Validates no unintended changes were made
  - **Dependency**: US3 (T021-T031) depends on US1 (T009-T020) completion
- **User Story 2 (Phase 5)**: Can start after Foundational (Phase 2) - Independent preventive validation
  - Can run in parallel with US1/US3 if desired (different validation approach)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: MUST follow User Story 1 immediately (paired P1 priorities for fix+validate)
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1/US3 (manual navigation test)

### Within Each User Story

**User Story 1 (Build Success)**:
- T009-T012: Detection phase (sequential - parse build output)
- T013-T014: Location phase (can run in parallel - different file searches)
- T015-T016: Fix application (sequential - modify files)
- T017-T020: Validation phase (sequential - verify build success)

**User Story 3 (Content Integrity)**:
- T021-T024: Diff review (sequential - examine changes)
- T025-T029: Config validation (can run in parallel - check different files)
- T030-T031: Content validation (sequential - read modified files)

**User Story 2 (Clean Links)**:
- T032-T038: Manual navigation (can run in parallel - different modules)
- T039-T042: Final verification (sequential - consolidate findings)

### Parallel Opportunities

**Phase 1 (Setup)**: Limited parallelism - sequential verification recommended
- T001-T005 should run sequentially to establish baseline

**Phase 2 (Foundational)**: High parallelism
- T006: Sequential (documents baseline)
- T007-T008: **Can run in parallel** (different documentation files)

**Phase 3 (User Story 1)**: Mixed parallelism
- T009-T012: Sequential (detection workflow)
- T013-T014: **Can run in parallel** (searching different link types)
- T015-T020: Sequential (fix and validate)

**Phase 4 (User Story 3)**: Mixed parallelism
- T021-T024: Sequential (diff review)
- T025-T029: **Can run in parallel** (checking different config files)
- T030-T031: Sequential (content review)

**Phase 5 (User Story 2)**: High parallelism
- T032-T038: **Can run in parallel** (navigating different modules simultaneously)
- T039-T042: Sequential (consolidation)

**Phase 6 (Polish)**: Mixed parallelism
- T043-T044: **Can run in parallel** (updating different documentation files)
- T045-T051: Sequential (success criteria validation)
- T052-T054: Sequential (git workflow)

---

## Parallel Example: User Story 1

```bash
# If broken links are detected, these searches can run in parallel:
Task T013: "Search for broken /docs/* links in frontend/docs/"
Task T014: "Search for broken /code-examples/*.zip links in frontend/docs/"

# Parallel execution:
grep -rn "/docs/missing-page" frontend/docs/ &
grep -rn "/code-examples/" frontend/docs/ &
wait
```

## Parallel Example: User Story 3

```bash
# Config file checks can run in parallel:
Task T025: "Verify no changes to frontend/docusaurus.config.ts"
Task T026: "Verify no changes to frontend/sidebars.ts"
Task T027: "Verify no changes to frontend/src/"
Task T028: "Verify no changes to backend/"

# Parallel execution:
git diff frontend/docusaurus.config.ts &
git diff frontend/sidebars.ts &
git diff frontend/src/ &
git diff backend/ &
wait
```

## Parallel Example: User Story 2

```bash
# Manual navigation tests can be distributed across team members:
Developer A: "Navigate module-1-ros2/ and module-2-simulation/"
Developer B: "Navigate module-3-isaac/ and module-4-vla/"
Developer C: "Navigate module-5-capstone/ and root pages"

# Or use automated link checker if desired (not required per spec):
# (This is optional - manual testing is the defined approach)
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 3 Only - Both P1)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T008)
3. Complete Phase 3: User Story 1 (T009-T020)
   - **Current state**: If no broken links, skip T013-T020
   - **Future state**: If broken links detected, execute full workflow
4. Complete Phase 4: User Story 3 (T021-T031) - **IMMEDIATELY after US1**
5. **STOP and VALIDATE**: Verify build passes AND content integrity preserved
6. Commit and push if validated

### Incremental Delivery

1. Complete Setup + Foundational → Detection framework ready
2. Add User Story 1 → Fix broken links (if any) → Validate build passes
3. Add User Story 3 → Validate content integrity → Deploy/Demo (MVP!)
4. Add User Story 2 → Manual navigation validation → Full quality assurance complete
5. Polish → Final documentation → Ready for production

### Current State Strategy (No Broken Links Detected)

Since the current build passes with 0 broken links:

1. **Phases 1-2**: Execute fully (T001-T008) to establish baseline and documentation
2. **Phase 3 (US1)**: Execute T009-T012 (detection) to confirm no broken links
   - Skip T013-T020 (fixes not needed)
   - Document in current-state.md
3. **Phase 4 (US3)**: Execute T021-T031 to validate clean git status
4. **Phase 5 (US2)**: Execute T032-T042 for preventive validation
5. **Phase 6**: Complete all success criteria validations
6. Result: Comprehensive documentation for future broken link issues

### Parallel Team Strategy

With multiple developers (if broken links exist):

1. **Team completes Setup + Foundational together** (T001-T008)
2. **One developer executes US1 detection** (T009-T012)
3. **Once broken links identified, parallelize fixes**:
   - Developer A: Fix /docs/* links in module-1 and module-2
   - Developer B: Fix /docs/* links in module-3 and module-4
   - Developer C: Fix /code-examples/* links and module-5
4. **All developers sync**: Re-run build together (T017-T020)
5. **One developer validates US3** (T021-T031)
6. **Team distributes US2 manual testing** (T032-T042)

---

## Notes

- **[P] tasks**: Different files or independent checks, no dependencies, safe to parallelize
- **[Story] label**: Maps task to specific user story for traceability and independent testing
- **Current state**: Build passes with 0 broken links - some tasks serve as preventive documentation
- **Future use**: If broken links appear, follow quickstart.md and execute relevant tasks
- **No tests**: Per spec, no automated tests requested - validation uses Docusaurus build + manual review
- **Minimal changes**: FR-010 requires minimal change per fix - manual review preferred over automation
- **Content preservation**: US3 is critical - must validate ONLY link markup changed
- Commit after completing each user story phase (T020, T031, T042, T054)
- Stop at any checkpoint to validate story independently
- Avoid: batch fixes without validation, config changes, content modifications beyond link removal

---

## Success Criteria Mapping

| Criterion | Validated By | Tasks |
|-----------|--------------|-------|
| SC-001: Build <10 min | Build time measurement | T003, T017, T046 |
| SC-002: Zero broken link errors | Build output check | T009, T018, T019, T047 |
| SC-003: 100% valid internal links | Build success + manual nav | T017, T032-T038, T048 |
| SC-004: Code examples removed/corrected | Grep search + build | T014, T041-T042, T049 |
| SC-005: Content unchanged | Git diff review | T022-T024, T030-T031, T050 |
| SC-006: Only /docs modified | Git status check | T025-T029, T051 |

---

## Task Count Summary

- **Total Tasks**: 54
- **Setup (Phase 1)**: 5 tasks
- **Foundational (Phase 2)**: 3 tasks
- **User Story 1 (P1)**: 12 tasks (detection: 4, fixes: 4, validation: 4)
- **User Story 3 (P1)**: 11 tasks (diff: 4, config: 5, content: 2)
- **User Story 2 (P2)**: 11 tasks (navigation: 7, verification: 4)
- **Polish (Phase 6)**: 12 tasks (documentation: 2, validation: 6, git: 4)

**Parallel Opportunities Identified**: 18 tasks marked [P]
- Phase 2: 2 parallel tasks (T007-T008)
- Phase 3: 2 parallel tasks (T013-T014)
- Phase 4: 5 parallel tasks (T025-T029)
- Phase 5: 7 parallel tasks (T032-T038)
- Phase 6: 2 parallel tasks (T043-T044)

**Suggested MVP Scope**: User Stories 1 + 3 (both P1) = 28 core tasks (Setup + Foundational + US1 + US3 + essential Polish)
