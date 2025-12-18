# Fix Validation Checklist: Docusaurus Broken Links

**Purpose**: Validate that broken link fixes are correct and complete before committing
**Feature**: 001-fix-docusaurus-links
**Source**: quickstart.md validation procedures

## Pre-Fix Validation

**Before applying any fixes, verify:**

- [ ] Build has been run to identify broken links (`npm run build`)
- [ ] Build output has been captured to `build-errors.log`
- [ ] Broken links inventory created in `broken-links-list.md`
- [ ] Each broken link documented with: source file, line number, target URL

## Fix Application Checklist

**For each broken link fix, ensure:**

- [ ] Source file located correctly in `frontend/docs/`
- [ ] Exact line number identified from build error
- [ ] Link markup pattern identified: `[text](url)`
- [ ] Fix pattern applied: `[text](url)` → `text`
- [ ] All original text content preserved
- [ ] Surrounding whitespace and punctuation maintained
- [ ] Sentence remains grammatically correct after fix
- [ ] Multiple instances of same broken link fixed consistently

## Build Validation

**After applying fixes, verify build success:**

- [ ] Build exits with code 0 (success)
- [ ] Build command: `npm run build` completes without errors
- [ ] No `[ERROR] Broken link` messages in build output
- [ ] Build time is <10 minutes (SC-001)
- [ ] Exit code verified: `echo $?` returns 0

## Content Integrity Validation

**Verify only link markup changed:**

- [ ] `git diff` shows only link markup changes (no content/structure changes)
- [ ] Text content is preserved (readable sentences)
- [ ] No changes to config files (`docusaurus.config.ts`, `sidebars.ts`)
- [ ] No changes to UI components (`frontend/src/`)
- [ ] No changes to backend code (`backend/`)
- [ ] No changes outside `frontend/docs/` directory
- [ ] All fixed files are in `frontend/docs/` only

## Git Status Validation

**Validation commands:**

```bash
# Count changed files
git status --short | grep "^ M" | wc -l

# List changed files (should be in frontend/docs/ only)
git status --short

# Ensure no config changes
git diff frontend/docusaurus.config.ts  # Should be empty
git diff frontend/sidebars.ts  # Should be empty

# Verify only docs changed
git diff --name-only | grep -v "^frontend/docs/"  # Should be empty
```

**Results:**

- [ ] Only `frontend/docs/*.md` or `frontend/docs/*.mdx` files modified
- [ ] No config file changes
- [ ] No UI component changes
- [ ] No backend changes

## Success Criteria Validation

**Verify all success criteria met:**

- [ ] **SC-001**: Build completes in <10 minutes
- [ ] **SC-002**: Zero broken link errors in build output
- [ ] **SC-003**: 100% of internal /docs/* links resolve to valid pages
- [ ] **SC-004**: All /code-examples/*.zip links removed or corrected
- [ ] **SC-005**: Documentation content remains semantically unchanged
- [ ] **SC-006**: No files outside /docs directory modified

## Edge Cases Handled

**Verify special cases are addressed:**

- [ ] Multiple links to same broken target - all fixed consistently
- [ ] Links in headers - link removed, header text preserved
- [ ] Links in list items - text preserved, bullet kept if meaningful
- [ ] Links in sentences - grammar remains correct after removal
- [ ] Empty link text - contextually appropriate text added or link fully removed

## Manual Review Checklist

**Before committing, manually review:**

- [ ] Read modified files to ensure text makes sense
- [ ] Check that no unintended whitespace changes occurred
- [ ] Verify markdown syntax is still valid (no broken lists, headers, etc.)
- [ ] Confirm navigation flow still works (Next/Previous links logical)
- [ ] Check that no broken links were missed

## Commit Preparation

**Ready to commit when:**

- [ ] All fixes applied and validated
- [ ] Build passes with exit code 0
- [ ] Git diff reviewed and approved
- [ ] Success criteria validated
- [ ] Edge cases handled
- [ ] Manual review complete

## Commit Checklist

**Before pushing:**

- [ ] Staged only `frontend/docs/` files: `git add frontend/docs/`
- [ ] Reviewed staged changes: `git status`
- [ ] Created descriptive commit message (see commit template below)
- [ ] Committed changes: `git commit -m "..."`
- [ ] Pushed to feature branch: `git push origin 001-fix-docusaurus-links`

## Commit Message Template

```bash
git commit -m "fix: remove broken links from documentation

- Removed broken link to /docs/[target] in [file]
- Preserved all text content
- Build now passes with exit code 0

Fixes #[issue-number] (if applicable)"
```

## Post-Commit Validation

**After pushing to remote:**

- [ ] Verify remote build passes (if CI/CD configured)
- [ ] Check that PR is created or updated
- [ ] Request code review
- [ ] Monitor CI/CD pipeline for any failures

## Rollback Procedure

**If fixes introduced issues:**

1. **Identify the problem**: Review build errors or failing tests
2. **Revert the commit**: `git revert HEAD` or `git reset --hard HEAD~1`
3. **Re-apply fixes**: Follow this checklist again more carefully
4. **Test thoroughly**: Ensure all validations pass before re-committing

## Notes

- **Minimal changes**: Only remove link markup, never modify surrounding content
- **Preserve semantics**: Ensure text remains meaningful after link removal
- **No automation**: Manual review preferred per spec constraint FR-010
- **Build is source of truth**: Always verify with `npm run build`
- **Git diff is critical**: Review every change before committing

---

**Last Updated**: 2025-12-18
**Template Version**: 1.0
**Based On**: specs/001-fix-docusaurus-links/quickstart.md
