# Data Model: Fix Docusaurus Build Errors

**Feature**: 001-fix-docusaurus-links
**Date**: 2025-12-18
**Phase**: 1 (Design)

## Overview

This feature involves documentation maintenance with no persistent data storage, databases, or APIs. However, we can model the conceptual entities involved in identifying and fixing broken links.

## Conceptual Entities

### 1. Broken Link

**Description**: A markdown link reference where the target URL does not resolve to an existing page or file.

**Attributes**:
- `sourceFile` (string): Path to the markdown file containing the broken link
  - Example: `frontend/docs/module-1-ros2/week-1/chapter-1-intro.mdx`
- `lineNumber` (integer): Line number in the source file where the link appears
  - Example: `42`
- `linkText` (string): The display text of the link
  - Example: `"Installation Guide"`
- `targetUrl` (string): The URL that the link points to
  - Example: `/docs/missing-page`
- `linkMarkup` (string): The full markdown link syntax
  - Example: `[Installation Guide](/docs/missing-page)`
- `errorType` (enum): Type of broken link
  - Values: `MISSING_DOC_PAGE`, `MISSING_CODE_EXAMPLE`, `INVALID_ANCHOR`

**Validation Rules**:
- `sourceFile` must exist in `frontend/docs/` directory
- `lineNumber` must be positive integer within file bounds
- `linkMarkup` must match pattern `[text](url)`
- `targetUrl` must be a relative or absolute path (not external URL)

**Lifecycle**:
1. **Detected**: Identified during build process via Docusaurus error output
2. **Analyzed**: Source file and line number extracted from build logs
3. **Fixed**: Link markup removed, text preserved
4. **Validated**: Build re-run to confirm fix successful

### 2. Documentation Page

**Description**: A markdown file (.md or .mdx) in the documentation directory representing a chapter or section.

**Attributes**:
- `filePath` (string): Absolute path to the markdown file
  - Example: `C:\Users\...\frontend\docs\intro.mdx`
- `relativePath` (string): Path relative to docs directory
  - Example: `module-1-ros2/week-1/chapter-1-intro.mdx`
- `urlPath` (string): Docusaurus URL path for the page
  - Example: `/docs/module-1-ros2/week-1/chapter-1-intro`
- `fileType` (enum): File extension type
  - Values: `MD`, `MDX`
- `contentSize` (integer): File size in bytes
- `linkCount` (integer): Number of internal links in the file

**Validation Rules**:
- `filePath` must exist on file system
- `fileType` must be `.md` or `.mdx`
- `urlPath` must be resolvable by Docusaurus router

**Relationships**:
- One Documentation Page can contain zero or more Broken Links (one-to-many)
- Documentation Pages can link to other Documentation Pages (many-to-many)

### 3. Code Example Archive

**Description**: A .zip file in the static directory containing downloadable code samples (currently none exist).

**Attributes**:
- `fileName` (string): Name of the .zip file
  - Example: `ros2-demo.zip`
- `filePath` (string): Path relative to static directory
  - Example: `code-examples/ros2-demo.zip`
- `urlPath` (string): Public URL for download
  - Example: `/code-examples/ros2-demo.zip`
- `exists` (boolean): Whether the file physically exists

**Validation Rules**:
- `fileName` must end with `.zip`
- `filePath` must be within `frontend/static/` directory
- If `exists` is false and links reference it, those are broken links

**Relationships**:
- Zero or more Documentation Pages can link to a Code Example Archive (many-to-one)

### 4. Build Log

**Description**: Console output from the Docusaurus build process showing errors, warnings, and success messages.

**Attributes**:
- `timestamp` (datetime): When the build was run
- `exitCode` (integer): Process exit code (0 = success, non-zero = failure)
- `brokenLinkErrors` (array of strings): List of broken link error messages
- `buildTime` (integer): Build duration in seconds
- `outputPath` (string): Path to generated build artifacts
  - Example: `frontend/build/`

**Validation Rules**:
- `exitCode` must be 0 for successful build
- `brokenLinkErrors` must be empty array for passing build
- `buildTime` must be < 600 seconds (10 minutes per SC-001)

**Relationships**:
- One Build Log identifies zero or more Broken Links (one-to-many)

## State Transitions

### Broken Link Lifecycle

```
[Undetected]
    ↓ (build with onBrokenLinks: 'throw')
[Detected in Build Log]
    ↓ (parse error message)
[Located in Source File]
    ↓ (remove link markup, preserve text)
[Fixed]
    ↓ (re-run build)
[Validated] → ✅ Complete
```

### Build Status Flow

```
[Build Triggered]
    ↓
[Scanning Files]
    ↓
[Validating Links]
    ├─ (all links valid) → [Build Successful] → Exit Code 0
    └─ (broken links found) → [Build Failed] → Exit Code 1
                                    ↓
                              [Fix Applied]
                                    ↓
                              [Re-Validate] → Loop back to [Scanning Files]
```

## Non-Persisted Data

Since this is a documentation maintenance task, no data is persisted to databases. All information exists in:

1. **File System**: Markdown files in `frontend/docs/`
2. **Build Output**: Console logs and `frontend/build/` directory (gitignored)
3. **Version Control**: Git commits tracking changes to markdown files

## API Contracts

**N/A** - This feature has no API endpoints. All operations are file-based edits validated by the Docusaurus build process.

## Summary

While this feature doesn't involve traditional data models (no database schemas), the conceptual entities (Broken Link, Documentation Page, Code Example Archive, Build Log) provide structure for understanding the fix workflow. The key relationship is:

**Build Log** detects **Broken Links** → **Broken Links** exist in **Documentation Pages** → Fix removes link markup → **Build Log** validates success.

All state is transient, existing only during the build process and fix workflow. Permanent changes are stored as git commits to markdown files.
