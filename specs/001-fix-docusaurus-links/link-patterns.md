# Link Pattern Examples: Docusaurus Broken Links

**Feature**: 001-fix-docusaurus-links
**Source**: research.md (Section 2 & 3)
**Purpose**: Reference guide for identifying and fixing broken link patterns

## Markdown Link Syntax

Docusaurus supports standard markdown link syntax in both `.md` and `.mdx` files.

### Basic Pattern

```markdown
[Link Text](target-url)
```

**Components**:
- `[Link Text]`: The visible text displayed to users
- `(target-url)`: The URL or path the link points to

## Link Types in Docusaurus

### 1. Absolute Paths (Internal Documentation)

**Pattern**: `/docs/path/to/page`

**Examples**:
```markdown
[Installation Guide](/docs/module-1-ros2/week-1/chapter-2-setup)
[Prerequisites](/docs/prerequisites)
[FAQ](/docs/faq)
```

**Docusaurus Resolution**:
- Automatically resolves to `.md` or `.mdx` file in `frontend/docs/`
- Example: `/docs/prerequisites` → `frontend/docs/prerequisites.mdx`

### 2. Relative Paths

**Pattern**: `./file.md` or `../directory/file.mdx`

**Examples**:
```markdown
[Next Chapter](./chapter-2-setup.mdx)
[Prerequisites](../prerequisites.mdx)
[Module Overview](../../module-1-ros2/module-1-assessment.mdx)
```

**Docusaurus Resolution**:
- Relative to current file location
- Must include file extension when using relative paths

### 3. Anchor Links

**Pattern**: `/docs/path#anchor-id` or `#local-anchor`

**Examples**:
```markdown
[Cloud Options](/docs/prerequisites#cloud-options)
[Setup Instructions](/docs/module-1-ros2/week-1/chapter-2-setup#installation)
[Jump to Section](#prerequisites)
```

**Docusaurus Resolution**:
- Navigates to specific section within a page
- Anchor IDs are auto-generated from headers or manually specified

### 4. Code Example Archives

**Pattern**: `/code-examples/filename.zip`

**Examples**:
```markdown
[ROS 2 Examples](/code-examples/ros2-basics.zip)
[Download Demo Code](/code-examples/module-1-demo.zip)
```

**Docusaurus Resolution**:
- Resolves to files in `frontend/static/code-examples/`
- Serves as downloadable static files

### 5. Navigation Links

**Pattern**: Previous/Next chapter references

**Examples**:
```markdown
**Previous**: [Chapter 1 - Introduction](./chapter-1-intro.mdx)
**Next**: [Chapter 3 - ROS Nodes](./chapter-3-nodes.mdx)
```

**Usage**: Common in chapter-based documentation for sequential navigation

### 6. Cross-Reference Links

**Pattern**: Links to glossary, FAQ, resources, etc.

**Examples**:
```markdown
See the [Glossary](/docs/glossary) for term definitions.
Refer to [FAQ](/docs/faq) for common questions.
Check [Resources](/docs/resources) for additional materials.
```

**Usage**: Linking between reference sections

## Broken Link Patterns

### What Makes a Link "Broken"

A link is broken when the target URL **does not resolve** to an existing file or page.

**Detection**: Docusaurus build with `onBrokenLinks: 'throw'` fails with error:

```
[ERROR] Broken link on source page path = /docs/example.md:
-> linking to /docs/nonexistent (resolved as: /path/to/docs/nonexistent.md)
```

### Common Broken Link Scenarios

#### Scenario 1: Missing Documentation Page

**Broken Pattern**:
```markdown
[Installation Guide](/docs/setup-guide)
```

**Why Broken**: File `frontend/docs/setup-guide.md` does not exist

**Build Error**:
```
[ERROR] Broken link on source page path = /docs/intro.mdx:
-> linking to /docs/setup-guide
```

#### Scenario 2: Missing Code Example

**Broken Pattern**:
```markdown
Download [ROS 2 examples](/code-examples/ros2-demo.zip)
```

**Why Broken**: File `frontend/static/code-examples/ros2-demo.zip` does not exist

**Build Error**:
```
[ERROR] Broken link on source page path = /docs/module-1-ros2/week-1/chapter-1-intro.mdx:
-> linking to /code-examples/ros2-demo.zip
```

#### Scenario 3: Incorrect File Extension

**Broken Pattern**:
```markdown
[Prerequisites](./prerequisites.md)
```

**Why Broken**: Actual file is `prerequisites.mdx`, not `.md`

**Build Error**:
```
[ERROR] Broken link on source page path = /docs/intro.mdx:
-> linking to ./prerequisites.md
```

#### Scenario 4: Wrong Path

**Broken Pattern**:
```markdown
[Chapter 2](/docs/ros2/chapter-2-setup)
```

**Why Broken**: Correct path is `/docs/module-1-ros2/week-1/chapter-2-setup`

**Build Error**:
```
[ERROR] Broken link on source page path = /docs/module-1-ros2/week-1/chapter-1-intro.mdx:
-> linking to /docs/ros2/chapter-2-setup
```

## Fix Patterns

### Standard Fix: Remove Link, Preserve Text

**Pattern Transformation**: `[text](broken-url)` → `text`

#### Example 1: Simple Sentence Link

**Before** (broken):
```markdown
Check out the [Installation Guide](/docs/missing-page) for details.
```

**After** (fixed):
```markdown
Check out the Installation Guide for details.
```

**Applied Rule**: Remove brackets `[]` and parentheses `()`, keep text

#### Example 2: Link in List

**Before** (broken):
```markdown
- [Prerequisites](/docs/nonexistent-prereqs)
- [Setup Guide](/docs/setup)
```

**After** (fixed):
```markdown
- Prerequisites
- Setup Guide
```

**Applied Rule**: Remove link markup, preserve list structure

#### Example 3: Link in Header

**Before** (broken):
```markdown
## [Getting Started](/docs/missing-intro)
```

**After** (fixed):
```markdown
## Getting Started
```

**Applied Rule**: Remove link, preserve header level and text

#### Example 4: Code Example Link

**Before** (broken):
```markdown
Download [example code](/code-examples/demo.zip) to get started.
```

**After** (fixed):
```markdown
Download example code to get started.
```

**Applied Rule**: Remove link, text flows naturally without it

#### Example 5: Multiple Links to Same Target

**Before** (broken):
```markdown
See the [intro guide](/docs/missing) and [overview](/docs/missing) pages.
```

**After** (fixed):
```markdown
See the intro guide and overview pages.
```

**Applied Rule**: Fix all instances consistently

## Edge Cases

### Edge Case 1: Empty Link Text

**Before** (broken):
```markdown
See [](/docs/missing-page) for more info.
```

**Fix Option A** (context-based):
```markdown
See the documentation for more info.
```

**Fix Option B** (infer from URL):
```markdown
See missing-page for more info.
```

**Recommendation**: Use context to determine appropriate text

### Edge Case 2: Link-Only Content

**Before** (broken):
```markdown
- [Broken Link](/docs/nonexistent)
```

**Fix** (preserve meaningful text):
```markdown
- Broken Link
```

**Alternative** (if no context):
```markdown
- (Link removed - target page does not exist)
```

### Edge Case 3: Nested Formatting

**Before** (broken):
```markdown
**Important**: See [**bold link**](/docs/missing) for details.
```

**After** (fixed):
```markdown
**Important**: See **bold link** for details.
```

**Applied Rule**: Preserve all formatting, remove only link markup

### Edge Case 4: Link in Code Block

**Before**:
```markdown
\`\`\`markdown
[Example Link](/docs/example)
\`\`\`
```

**Status**: **NOT BROKEN** - Links inside code blocks are not rendered as clickable links

**Action**: No fix needed for links in code blocks

## Patterns NOT in Scope

The following link types are **NOT** targeted for fixes:

### External URLs

```markdown
[GitHub](https://github.com)
[npm](https://www.npmjs.com)
```

**Reason**: External links handled separately, not part of internal docs

### Image Links

```markdown
![Alt Text](./image.png)
```

**Reason**: Image syntax different from text links, different validation

### HTML Anchor Tags

```html
<a href="/docs/page">Link</a>
```

**Reason**: HTML links require different handling, should use markdown

## Validation Patterns

### How to Verify a Fix

**Step 1**: Identify the pattern
```markdown
[text](url)
```

**Step 2**: Apply transformation
```markdown
text
```

**Step 3**: Check grammar
- Sentence should still read naturally
- No orphaned punctuation
- Proper spacing maintained

**Step 4**: Verify in git diff
```diff
- Check the [Setup Guide](/docs/missing-setup) for installation.
+ Check the Setup Guide for installation.
```

**Expected**: Only link markup removed, text preserved

## Regular Expression Patterns (Reference Only)

**Note**: Manual fixes preferred per spec, but regex provided for reference

### Match Markdown Link

```regex
\[([^\]]+)\]\(([^)]+)\)
```

**Groups**:
- `$1`: Link text
- `$2`: URL

### Extract Components

```bash
# Example: [Prerequisites](/docs/prereqs)
# Text: Prerequisites
# URL: /docs/prereqs
```

### Replace Pattern (for automation - NOT recommended per spec)

```bash
# Replace: \[([^\]]+)\]\([^)]+\)
# With: $1
```

**Warning**: Automation not recommended - manual review ensures content quality

## Best Practices

### Prevention

1. **Verify target exists** before creating link
2. **Use relative paths** for same-directory files
3. **Test build** before committing
4. **Double-check spelling** in URLs

### Fixing

1. **Read context** around broken link
2. **Preserve meaning** of original text
3. **Check grammar** after removal
4. **Verify build** passes after fix
5. **Review diff** before committing

### Validation

1. **Run build**: `npm run build` must pass
2. **Check exit code**: Must be 0
3. **Review changes**: `git diff` shows only link markup removed
4. **Read modified files**: Ensure text makes sense

---

**Last Updated**: 2025-12-18
**Version**: 1.0
**Based On**: specs/001-fix-docusaurus-links/research.md (Sections 2-3)
