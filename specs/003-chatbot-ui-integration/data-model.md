# Data Model: UI Enhancement - Professional Robotics Theme

## Overview
This document describes the data structures and CSS variables that support the professional robotics theme UI enhancement. The theme uses Electric Cyan/Blue (#00FFFF) and Neon Green (#00FF00) accents with a dark background for a high-tech, engineering console aesthetic.

## CSS Variable Data Model

### 1. Color Variables

#### 1.1 Background Colors
```css
--ifm-color-primary-background: #0D1117;  /* Deep near-black */
--ifm-background-color: #0D1117;          /* Main background */
--ifm-background-surface-color: #161B22;  /* Card/content surfaces */
--ifm-background-tertiary: #21262D;        /* Lighter surfaces */
```

#### 1.2 Primary Accent Colors (Electric Cyan/Blue)
```css
--ifm-color-primary: #00FFFF;              /* Base electric cyan */
--ifm-color-primary-dark: #00E6E6;         /* Hover state */
--ifm-color-primary-darker: #00D9D9;       /* Active state */
--ifm-color-primary-darkest: #00B3B3;      /* Disabled state */
--ifm-color-primary-light: #1AFFFF;        /* Lighter state */
--ifm-color-primary-lighter: #33FFFF;      /* Lighter state */
--ifm-color-primary-lightest: #66FFFF;     /* Lightest state */
```

#### 1.3 Secondary Accent Colors (Neon Green/Lime)
```css
--ifm-color-secondary: #00FF00;            /* Base neon green */
--ifm-color-secondary-dark: #00E600;       /* Hover state */
--ifm-color-secondary-darker: #00D900;     /* Active state */
--ifm-color-secondary-darkest: #00B300;    /* Disabled state */
--ifm-color-secondary-light: #1AFF1A;      /* Lighter state */
--ifm-color-secondary-lighter: #33FF33;    /* Lighter state */
--ifm-color-secondary-lightest: #66FF66;   /* Lightest state */
```

#### 1.4 Text Colors
```css
--ifm-color-text: #F0F6FC;                 /* Primary text */
--ifm-color-text-secondary: #C9D1D9;       /* Secondary text */
--ifm-color-text-tertiary: #8B949E;        /* Muted text */
```

#### 1.5 Border and Code Colors
```css
--ifm-color-border: #30363D;               /* Component borders */
--ifm-toc-border-color: #30363D;           /* Table of contents borders */
--ifm-code-background: rgba(48, 54, 61, 0.5); /* Inline code bg */
--ifm-pre-background: #161B22;             /* Code block background */
```

#### 1.6 Shadow Colors
```css
--ifm-global-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);        /* Standard shadow */
--ifm-global-shadow-top: 0 -4px 12px rgba(0, 0, 0, 0.5);   /* Top shadow */
--ifm-global-shadow-bottom: 0 4px 12px rgba(0, 0, 0, 0.5); /* Bottom shadow */
```

### 2. Typography Variables

#### 2.1 Font Families
```css
--ifm-font-family-base: 'Inter', 'Roboto Mono', 'SF Mono', Monaco, Inconsolata, 'Fira Mono', 'Droid Sans Mono', monospace, system-ui, -apple-system, sans-serif;
--ifm-font-family-monospace: 'Roboto Mono', 'SF Mono', Monaco, Inconsolata, 'Fira Mono', 'Droid Sans Mono', monospace;
```

#### 2.2 Font Sizes
```css
--ifm-font-size-base: 16px;        /* Base font size */
--ifm-h1-font-size: 2.5rem;       /* 40px - Main page titles */
--ifm-h2-font-size: 2rem;         /* 32px - Section headings */
--ifm-h3-font-size: 1.75rem;      /* 28px - Subsection headings */
--ifm-h4-font-size: 1.5rem;       /* 24px - Minor headings */
--ifm-h5-font-size: 1.25rem;      /* 20px - Content headings */
--ifm-h6-font-size: 1rem;         /* 16px - Label headings */
```

#### 2.3 Font Weights
```css
--ifm-font-weight-light: 300;      /* Light text */
--ifm-font-weight-normal: 400;     /* Regular text */
--ifm-font-weight-semibold: 600;   /* Emphasized text */
--ifm-font-weight-bold: 700;       /* Strong emphasis */
```

### 3. Spacing Variables

#### 3.1 Spacing Scale
```css
--ifm-spacing-xs: 0.5rem;          /* 8px - Small spacing */
--ifm-spacing-sm: 0.75rem;         /* 12px - Small-medium spacing */
--ifm-spacing-md: 1rem;            /* 16px - Medium spacing */
--ifm-spacing-lg: 1.5rem;          /* 24px - Large spacing */
--ifm-spacing-xl: 2rem;            /* 32px - Extra large spacing */
--ifm-spacing-2xl: 3rem;           /* 48px - Double extra large */
```

#### 3.2 Border Radius
```css
--ifm-global-radius: 4px;          /* Standard border radius */
--ifm-button-border-radius: 6px;   /* Button border radius */
--ifm-card-border-radius: 8px;     /* Card border radius */
```

#### 3.3 Animation Timing
```css
--ifm-transition-fast: 0.15s;     /* Fast transitions */
--ifm-transition-normal: 0.3s;    /* Normal transitions */
--ifm-transition-slow: 0.5s;      /* Slow transitions */
```

## Component-Specific Data Models

### 1. Navigation Component
- Background: `--ifm-color-primary-background`
- Text: `--ifm-color-text`
- Hover: `--ifm-color-primary`
- Active: `--ifm-color-secondary`

### 2. Chat Widget Component
- Button Background: `--ifm-color-primary`
- Window Background: `--ifm-background-surface-color`
- Header Background: `--ifm-color-primary`
- Sent Messages: `--ifm-color-primary`
- Received Messages: `--ifm-color-border`

### 3. Code Block Component
- Background: `--ifm-pre-background`
- Text: `--ifm-color-text`
- Keywords: `--ifm-color-primary`
- Values: `--ifm-color-secondary`

## Accessibility Data Model

### 1. Contrast Ratios
- Text on background: Minimum 4.5:1 (AA compliance)
- Focus indicators: Minimum 3:1 contrast
- Interactive elements: Sufficient contrast for visibility

### 2. Focus States
- Primary: `--ifm-color-primary` with glow effect
- Secondary: `--ifm-color-secondary` with glow effect
- Outline: 2px solid with proper offset

## Responsive Design Variables

### 1. Breakpoints
```css
--ifm-container-width: 1140px;     /* Desktop container width */
--ifm-container-width-xl: 1320px;  /* Extra large container */
--ifm-paragraph-margin-bottom: 1rem; /* Paragraph spacing */
```

### 2. Mobile Adjustments
- Reduced spacing on smaller screens
- Adjusted font sizes for readability
- Touch-friendly interactive elements

## Validation Rules

### 1. Color Validation
- All color combinations must meet WCAG 2.1 AA standards
- No color-only information conveyance
- Sufficient contrast for readability

### 2. Typography Validation
- Font sizes appropriate for content hierarchy
- Line heights optimized for readability (1.4-1.6)
- Font weights used consistently for emphasis

### 3. Spacing Validation
- Consistent spacing between elements
- Proper visual hierarchy maintained
- Responsive spacing adjustments

This data model provides the foundation for consistent implementation of the professional robotics theme across all UI components while maintaining accessibility and usability standards.