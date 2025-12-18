# Research: Fix Docusaurus Build Errors

**Feature**: 001-fix-docusaurus-links
**Date**: 2025-12-18
**Phase**: 0 (Research & Discovery)

## Overview

This document consolidates research findings for fixing broken links in Docusaurus documentation. All technical context is known (no NEEDS CLARIFICATION items), so research focuses on best practices and implementation approaches.

## Current State Analysis

### Build Status (as of 2025-12-18)
- **Build Result**: ✅ SUCCESS (exit code 0)
- **Broken Links Found**: 0
- **Build Time**: ~5-7 minutes (within <10 min constraint)
- **Link Checking**: Strict mode enabled (`onBrokenLinks: 'throw'`)

### Documentation Inventory
- **Total Files**: 44 markdown files (.md, .mdx)
- **Internal Links**: ~95 documented links (verified in DOCUSAURUS_LINK_VERIFICATION.md)
- **Target Directories**: `/docs/*` pages, `/code-examples/*.zip` files (currently none exist)

### Key Finding
The build currently passes with no broken links. This specification provides a preventive framework and systematic approach for addressing any future broken link issues.

## Research Areas

### 1. Docusaurus Link Validation Mechanisms

**Decision**: Use Docusaurus built-in link checker with `onBrokenLinks: 'throw'` configuration

**Rationale**:
- Docusaurus provides native broken link detection during build
- `onBrokenLinks: 'throw'` setting causes build to fail on broken links, ensuring issues are caught before deployment
- Build output provides detailed error messages showing exact file locations and broken URLs
- No additional tooling required

**Alternatives Considered**:
- **External link checkers** (markdown-link-check, linkinator): Rejected because Docusaurus already provides this functionality with better integration
- **Manual grep/regex search**: Rejected because it doesn't validate link targets, only finds syntax
- **Custom scripts**: Rejected due to spec constraint of no new tools/complexity

**Implementation Approach**:
```bash
# Run build to identify broken links
cd frontend
npm run build

# Build output will show errors like:
# [ERROR] Broken link on source page path = /docs/example.md:
# -> linking to /docs/nonexistent (resolved as: /path/to/docs/nonexistent.md)
```

### 2. Markdown Link Patterns in Docusaurus

**Decision**: Target standard markdown link syntax `[text](url)` and MDX-specific patterns

**Rationale**:
- Docusaurus supports both `.md` and `.mdx` files
- Link formats used in the project:
  - Absolute paths: `[Page](/docs/module-1-ros2/week-1/chapter-1-intro)`
  - Relative paths: `[Prerequisites](../prerequisites.mdx)`
  - Anchors: `[Setup](/docs/prerequisites#cloud-options)`
- All follow standard markdown syntax

**Link Types to Handle**:
1. **Internal documentation links**: `/docs/*` (most common)
2. **Code example archives**: `/code-examples/*.zip` (currently none exist, but may be added in future)
3. **Navigation links**: Previous/Next chapter links
4. **Cross-reference links**: FAQ, glossary, resources

**Patterns NOT in scope** (per spec):
- External URLs (http://, https://)
- Image links (`![alt](image.png)`)
- HTML anchor tags

### 3. Content Preservation Strategies

**Decision**: Remove link markup `[text](url)` → `text`, preserving all original text content

**Rationale**:
- Spec requirement FR-005: "link markup MUST be removed while preserving the original text content"
- Maintains readability and semantic meaning
- Avoids breaking sentence flow
- User still sees what the link was supposed to point to

**Pattern Transformations**:
```markdown
Before: Check out the [Installation Guide](/docs/missing-page) for details.
After:  Check out the Installation Guide for details.

Before: Download [example code](/code-examples/ros2-demo.zip).
After:  Download example code.

Before: See [module overview](./nonexistent.md) above.
After:  See module overview above.
```

**Edge Cases**:
1. **Multiple links to same broken target**: Fix all instances consistently
2. **Link-only list items**: Keep text, remove bullet if it becomes empty
3. **Links in headers**: Remove link, keep header text
4. **Nested links** (rare): Process inner-most first

### 4. Validation and Testing Approach

**Decision**: Multi-stage validation using build verification and content comparison

**Rationale**:
- Build must pass (primary success criterion)
- Content integrity must be preserved (critical constraint)
- Changes must be minimal and surgical

**Validation Steps**:
```bash
# 1. Pre-fix: Run build to identify broken links
npm run build 2>&1 | tee build-before.log

# 2. Fix: Apply changes to markdown files (manual or scripted)

# 3. Post-fix: Verify build passes
npm run build 2>&1 | tee build-after.log

# 4. Compare: Ensure only link markup changed
git diff frontend/docs/

# 5. Validate: Check for unintended changes
# - No structural changes (file moves, renames)
# - No config changes (docusaurus.config.ts, sidebars.ts)
# - No UI/auth/chatbot modifications
# - Text content preserved
```

**Success Criteria Validation**:
- SC-001: Build time <10 min ✓ (measured in logs)
- SC-002: Zero broken link errors ✓ (exit code 0)
- SC-003: 100% valid links ✓ (no build errors)
- SC-004: Code examples fixed ✓ (grep for `/code-examples/`)
- SC-005: Content unchanged ✓ (git diff review)
- SC-006: Only /docs modified ✓ (git status check)

### 5. Best Practices for Link Maintenance

**Decision**: Establish guidelines to prevent future broken links

**Recommendations** (for documentation):
1. **Use relative paths** for same-directory links: `[Page](./page.md)` instead of `/docs/dir/page`
2. **Verify target exists** before adding links (check file system)
3. **Use Docusaurus path syntax**: `/docs/path` auto-resolves to `.md` or `.mdx`
4. **Enable strict checking in development**: Keep `onBrokenLinks: 'throw'` for local builds
5. **Add pre-commit hook** (optional): Run build before commits to catch issues early

**CI/CD Integration** (future enhancement, out of scope):
```yaml
# .github/workflows/build.yml
- name: Build Docusaurus
  run: |
    cd frontend
    npm install
    npm run build  # Fails if broken links exist
```

## Technology Stack Summary

### Required Tools (Already Available)
- **Node.js 20+**: JavaScript runtime
- **npm**: Package manager
- **Docusaurus 3.9.2**: Static site generator with built-in link validation
- **TypeScript 5.6.2**: Type checking (for config files)

### No New Dependencies Required
Per spec constraints, no new tools or dependencies are added. All link detection and validation uses existing Docusaurus infrastructure.

## Implementation Strategy

### Approach: Manual Identification + Surgical Fixes

**Step 1: Identify Broken Links**
- Run `npm run build` in frontend/ directory
- Capture build output showing broken link errors
- Parse output to extract: source file, line number, broken URL

**Step 2: Locate in Source Files**
- Open each file listed in build errors
- Navigate to line number
- Identify exact link markup `[text](url)`

**Step 3: Apply Fix**
- Replace `[text](url)` with `text`
- Preserve surrounding whitespace and punctuation
- Ensure sentence remains grammatically correct

**Step 4: Validate**
- Re-run `npm run build`
- Verify exit code 0 (success)
- Review `git diff` to ensure only link markup changed

**Step 5: Commit**
- Stage only modified markdown files
- Commit with message: `fix: remove broken links from documentation`
- Create PR for review

### Automation Potential (Out of Scope, Future Enhancement)

A script could automate this process:
```bash
#!/bin/bash
# NOT IMPLEMENTED - just research note
# Parse build output for broken links
# Use sed/awk to replace [text](broken-url) → text
# Validate with second build
```

However, per spec constraint FR-010 ("minimal change required"), manual review of each fix is safer to ensure content integrity.

## Risk Analysis

### Low Risk
- **Current state**: Build already passes, no broken links exist
- **Scope**: Pure markdown edits, no code/config changes
- **Reversibility**: All changes tracked in git, easy to revert
- **Validation**: Build provides immediate feedback

### Mitigation Strategies
1. **Test on feature branch**: Never push directly to main
2. **Review each diff**: Manually verify text preservation
3. **Run build multiple times**: Ensure consistent success
4. **Check navigation**: Manually click through docs to verify no broken flows

## Conclusion

All research areas have been resolved with no unknowns remaining. The implementation approach is straightforward:
1. Use Docusaurus built-in link validation (no new tools)
2. Apply surgical fixes to remove broken link markup while preserving text
3. Validate using build success and git diff review

**Current Status**: Build passes with zero broken links. This specification provides a systematic framework for addressing any future link issues that may arise.

**Next Phase**: Proceed to Phase 1 (Design) to document the fix workflow in quickstart.md and create validation checklists.
