# Quickstart: Fix Docusaurus Broken Links

**Feature**: 001-fix-docusaurus-links
**Date**: 2025-12-18
**Audience**: Developers maintaining the documentation

## Overview

This guide provides a step-by-step workflow for identifying and fixing broken links in the Docusaurus documentation. Follow this procedure whenever the build fails due to broken link errors or as preventive maintenance.

## Prerequisites

- Node.js 20+ installed
- npm package manager available
- Git for version control
- Access to the repository with write permissions
- Working directory at repository root

## Quick Reference

### Build Commands
```bash
# Navigate to frontend directory
cd frontend

# Run production build (detects broken links)
npm run build

# Start development server (live reload)
npm run start

# Serve production build locally
npm run serve
```

### Expected Build Success Output
```
[INFO] [en] Creating an optimized production build...
[webpackbar] ✔ Server: Compiled successfully in X.XXm
[webpackbar] ✔ Client: Compiled successfully in X.XXm
[SUCCESS] Generated static files in "build".
```

### Expected Build Failure Output (Broken Links)
```
[ERROR] Broken link on source page path = /docs/example.md:
-> linking to /docs/nonexistent (resolved as: /path/to/docs/nonexistent.md)

Error: Broken links found!
```

## Step-by-Step Fix Workflow

### Step 1: Identify Broken Links

**Run the build to detect broken links:**

```bash
# From repository root
cd frontend

# Run build and capture output
npm run build 2>&1 | tee build-errors.log
```

**Analyze the output:**
- Exit code 0 = No broken links ✅
- Exit code 1 = Broken links found ❌

**If broken links exist, extract details:**
- Source file path (e.g., `/docs/module-1-ros2/week-1/chapter-1-intro.mdx`)
- Target URL (e.g., `/docs/missing-page`)
- Error message context

**Example error parsing:**
```
[ERROR] Broken link on source page path = /docs/module-1-ros2/week-1/chapter-1-intro.mdx:
-> linking to /docs/setup-guide (resolved as: frontend/docs/setup-guide.md)
```

Extracted info:
- File: `frontend/docs/module-1-ros2/week-1/chapter-1-intro.mdx`
- Broken URL: `/docs/setup-guide`
- Issue: Target file doesn't exist

### Step 2: Locate Link in Source File

**Open the source file:**
```bash
# Use your preferred editor
code frontend/docs/module-1-ros2/week-1/chapter-1-intro.mdx

# Or search for the link pattern
grep -n "/docs/setup-guide" frontend/docs/module-1-ros2/week-1/chapter-1-intro.mdx
```

**Find the broken link markup:**
```markdown
# Before (broken)
Check the [Setup Guide](/docs/setup-guide) for installation instructions.
```

**Identify the link components:**
- Link text: `Setup Guide`
- Target URL: `/docs/setup-guide`
- Full markup: `[Setup Guide](/docs/setup-guide)`

### Step 3: Apply the Fix

**Fix Strategy: Remove link markup, preserve text**

```markdown
# Before (broken link)
Check the [Setup Guide](/docs/setup-guide) for installation instructions.

# After (text preserved)
Check the Setup Guide for installation instructions.
```

**Pattern Replacement:**
- Find: `[Setup Guide](/docs/setup-guide)`
- Replace with: `Setup Guide`

**Additional Examples:**

```markdown
# Example 1: Link in sentence
Before: Download the [code samples](/code-examples/demo.zip) to get started.
After:  Download the code samples to get started.

# Example 2: Link in list
Before: - [Prerequisites](/docs/missing-prereqs)
After:  - Prerequisites

# Example 3: Link in header (keep header level)
Before: ## [Chapter Overview](/docs/nonexistent)
After:  ## Chapter Overview

# Example 4: Multiple links to same target
Before: See [intro](/docs/missing) and [overview](/docs/missing) pages.
After:  See intro and overview pages.
```

**What NOT to do:**
- ❌ Don't delete the entire sentence
- ❌ Don't add comments like `<!-- broken link -->`
- ❌ Don't replace with different text
- ❌ Don't create placeholder files
- ❌ Don't modify surrounding content

**Save the file after making changes.**

### Step 4: Validate the Fix

**Re-run the build:**
```bash
npm run build
```

**Check for success:**
```bash
echo $?  # Should output: 0
```

**Review the changes:**
```bash
# From repository root
git diff frontend/docs/

# Should show ONLY link markup removals, no other changes
```

**Validate with diff review:**
```diff
- Check the [Setup Guide](/docs/setup-guide) for installation instructions.
+ Check the Setup Guide for installation instructions.
```

### Step 5: Verify Content Integrity

**Checklist before committing:**

- [ ] Build exits with code 0 (success)
- [ ] No broken link errors in build output
- [ ] `git diff` shows only link markup changes (no content/structure changes)
- [ ] Text content is preserved (readable sentences)
- [ ] No changes to config files (`docusaurus.config.ts`, `sidebars.ts`)
- [ ] No changes to UI components (`frontend/src/`)
- [ ] No changes outside `frontend/docs/` directory
- [ ] All fixed files are in `frontend/docs/` only

**Validation commands:**
```bash
# Count changed files
git status --short | grep "^ M" | wc -l

# List changed files (should be in frontend/docs/ only)
git status --short

# Ensure no config changes
git diff frontend/docusaurus.config.ts  # Should be empty
git diff frontend/sidebars.ts  # Should be empty
```

### Step 6: Commit the Changes

**Stage only the modified markdown files:**
```bash
# From repository root
git add frontend/docs/

# Review staged changes
git status
```

**Commit with descriptive message:**
```bash
git commit -m "fix: remove broken links from documentation

- Removed broken link to /docs/setup-guide in chapter-1-intro.mdx
- Preserved all text content
- Build now passes with exit code 0

Fixes #<issue-number> (if applicable)"
```

**Push to feature branch:**
```bash
git push origin 001-fix-docusaurus-links
```

## Handling Multiple Broken Links

**If the build shows multiple broken links:**

```
[ERROR] Broken link on source page path = /docs/intro.mdx:
-> linking to /docs/missing-1

[ERROR] Broken link on source page path = /docs/faq.mdx:
-> linking to /docs/missing-2

[ERROR] Broken link on source page path = /docs/faq.mdx:
-> linking to /code-examples/demo.zip
```

**Create a checklist:**
```markdown
## Broken Links to Fix

- [ ] /docs/intro.mdx → /docs/missing-1
- [ ] /docs/faq.mdx → /docs/missing-2
- [ ] /docs/faq.mdx → /code-examples/demo.zip
```

**Fix one at a time:**
1. Fix the first link
2. Save the file
3. Re-run build to see remaining errors
4. Repeat until build passes

**Alternatively, fix all at once:**
1. Fix all links in the list
2. Save all files
3. Run build once to validate all fixes

**Commit strategy:**
- **Single commit**: If all fixes are related and simple
- **Multiple commits**: If fixes are in different modules or complex

## Edge Cases

### Case 1: Link to Non-Existent Code Example

```markdown
Before: Download [ROS 2 examples](/code-examples/ros2-basics.zip)
After:  Download ROS 2 examples
```

**Note**: Do NOT create the .zip file (per spec constraint FR-006).

### Case 2: Multiple Links in Same Sentence

```markdown
Before: See [intro](/docs/missing-1) and [guide](/docs/missing-2) for details.
After:  See intro and guide for details.
```

### Case 3: Link in Navigation (Next/Previous)

**If a "Next" or "Previous" link is broken:**

```markdown
Before: Next: [Advanced Topics](/docs/nonexistent-advanced)
After:  Next: Advanced Topics
```

**Then verify navigation still makes sense** by reading the text.

### Case 4: Empty Link Text

```markdown
Before: See [](/docs/missing) for more info.

# This is likely an error in the original markdown
# Option 1: Remove the entire link reference
After:  See the documentation for more info.

# Option 2: Use context to infer text
After:  See this page for more info.
```

**Use judgment based on surrounding context.**

## Testing Checklist

After fixing broken links, validate against all success criteria:

- [ ] **SC-001**: Build completes in <10 minutes ⏱️
  - Check: Review build time in output
  - Current baseline: ~5-7 minutes ✅

- [ ] **SC-002**: Zero broken link errors ❌
  - Check: Build output contains no `[ERROR] Broken link` messages
  - Validation: Exit code is 0

- [ ] **SC-003**: 100% of internal links valid ✅
  - Check: No `/docs/*` link errors in build
  - Validation: Build success

- [ ] **SC-004**: Code example links removed/corrected 📦
  - Check: No `/code-examples/*.zip` link errors
  - Validation: `grep -r "/code-examples/" frontend/docs/` returns no broken links

- [ ] **SC-005**: Content semantically unchanged 📝
  - Check: `git diff` shows only link markup removal
  - Validation: Read changed lines to ensure text makes sense

- [ ] **SC-006**: Only /docs files modified 📁
  - Check: `git status` shows changes only in `frontend/docs/`
  - Validation: No changes to config, UI, backend, or other directories

## Troubleshooting

### Problem: Build still fails after fix

**Diagnosis:**
```bash
# Re-run build with verbose output
npm run build -- --verbose

# Check for other errors (not link-related)
npm run build 2>&1 | grep -i error
```

**Solutions:**
- Verify you saved the file after editing
- Check for typos in the fix (e.g., extra spaces)
- Ensure you removed the entire `[text](url)` pattern, not just part of it
- Clear build cache: `npm run clear && npm run build`

### Problem: Git diff shows unexpected changes

**Diagnosis:**
```bash
# See detailed diff
git diff frontend/docs/ > changes.diff
cat changes.diff
```

**Solutions:**
- If config files changed: Revert them (`git checkout -- frontend/docusaurus.config.ts`)
- If content changed: Review and revert unintended edits
- If line endings changed: Configure git to handle CRLF/LF properly

### Problem: Build passes but links still appear broken in browser

**Diagnosis:**
```bash
# Test the production build locally
npm run serve
# Visit http://localhost:3000 and click links
```

**Solutions:**
- Clear browser cache (Ctrl+Shift+R)
- Restart the serve command
- Check if the link was supposed to be external (out of scope)

## Quick Commands Summary

```bash
# 1. Detect broken links
cd frontend && npm run build 2>&1 | tee ../build-errors.log

# 2. Search for a broken link in docs
grep -rn "/docs/missing-page" frontend/docs/

# 3. Fix the link (manual edit in editor)
# Replace [text](/docs/missing-page) → text

# 4. Validate fix
npm run build

# 5. Review changes
git diff frontend/docs/

# 6. Commit
git add frontend/docs/
git commit -m "fix: remove broken link to /docs/missing-page"
git push origin 001-fix-docusaurus-links
```

## Next Steps

After successfully fixing broken links:

1. **Create Pull Request**: Submit PR to merge feature branch into main
2. **Request Review**: Have team member review the changes
3. **Monitor CI/CD**: Ensure automated builds pass
4. **Deploy**: Merge to main triggers deployment to production
5. **Verify Production**: Check that live site has no broken links

## Preventive Measures

To avoid future broken links:

1. **Enable strict checking locally**: Keep `onBrokenLinks: 'throw'` in `docusaurus.config.ts`
2. **Test before committing**: Run `npm run build` before pushing
3. **Use relative paths**: Prefer `./file.md` over `/docs/path/file` when possible
4. **Verify targets exist**: Check file system before adding links
5. **Review documentation changes**: Ensure link targets aren't deleted without updating references

## Support

If you encounter issues not covered in this guide:

1. Check the spec: `specs/001-fix-docusaurus-links/spec.md`
2. Review the plan: `specs/001-fix-docusaurus-links/plan.md`
3. See research: `specs/001-fix-docusaurus-links/research.md`
4. Consult the team or open an issue

---

**Last Updated**: 2025-12-18
**Maintained By**: Development Team
