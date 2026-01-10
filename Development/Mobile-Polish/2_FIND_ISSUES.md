# Mobile Polish Discovery - Find Specific Issues

## Context

- **Playbook:** Mobile Polish
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Using the assessment from the analysis phase, identify specific mobile polish issues that need fixing. This document bridges high-level findings to actionable improvements.

## Instructions

1. **Read the assessment** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ASSESSMENT.md`
2. **Search for mobile anti-patterns** - Components that break on mobile
3. **Identify missing optimizations** - Lazy loading, responsive images, touch targets
4. **Find navigation issues** - Desktop-only menus, overflow problems
5. **Output findings** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md`

## Discovery Checklist

- [ ] **Find mobile issues (or skip if comprehensive)**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ASSESSMENT.md`. If the assessment shows the site is fully mobile-optimized (responsive navigation, proper viewport, lazy loading, appropriate touch targets, no critical issues), mark this task complete without creating an issues file. Otherwise, search for specific components and code that need mobile optimization. Document each issue with file path, problem description, and suggested fix. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md`.

## What to Look For

### Viewport & Meta Tags

Search for these patterns:

```bash
# Missing viewport tag
grep -r "viewport" --include="*.html" --include="*.tsx" --include="*.jsx"

# Check _document.tsx in Next.js
# Check index.html in Vite/CRA
# Check layout.tsx in Next.js App Router
```

**Issue indicators:**

- No viewport meta tag
- Wrong viewport values (user-scalable=no without good reason)
- Missing initial-scale=1

### Responsive Navigation

Search for navigation components:

```bash
# Find header/nav components
find . -name "*header*" -o -name "*nav*" -o -name "*menu*" | grep -E "\.(tsx|jsx|ts|js)$"
```

**Issue indicators:**

- Desktop-only horizontal menu links on mobile
- No hamburger menu/drawer implementation
- Menu items overflow on small screens
- No mobile menu state management

### Non-Responsive Components

Common patterns to search:

```bash
# Fixed widths (potential mobile issues)
grep -r "width: [0-9]" --include="*.css" --include="*.scss" --include="*.tsx"
grep -r "w-\[" --include="*.tsx" --include="*.jsx"  # Tailwind arbitrary values

# Absolute positioning issues
grep -r "position: absolute" --include="*.css" --include="*.scss"

# Fixed containers
grep -r "container" --include="*.tsx" --include="*.jsx"
```

### Touch Target Issues

**Minimum size:** 44×44px (Apple) or 48×48px (Android)

Search for small interactive elements:

```bash
# Small buttons
grep -r "text-xs" --include="*.tsx" --include="*.jsx"  # Tailwind small text
grep -r "p-1\|px-1\|py-1" --include="*.tsx"  # Small padding

# Icon-only buttons
grep -r "<button.*<.*Icon" --include="*.tsx" --include="*.jsx"
```

**Issue indicators:**

- Buttons smaller than 44px
- Links with insufficient spacing
- Icon buttons without adequate tap area
- Dense navigation items

### Image Optimization

Search for unoptimized images:

```bash
# Regular img tags (should use Next.js Image or lazy loading)
grep -r "<img" --include="*.tsx" --include="*.jsx"

# Missing lazy loading
grep -r 'src="' --include="*.tsx" | grep -v "loading="
```

**Issue indicators:**

- Using `<img>` instead of `<Image>` in Next.js
- No `loading="lazy"` attribute
- No `srcset` for responsive images
- Large images without optimization
- Missing width/height attributes (CLS issues)

### Forms

Search for mobile-unfriendly forms:

```bash
# Form inputs
grep -r "<input" --include="*.tsx" --include="*.jsx"
grep -r "<select" --include="*.tsx" --include="*.jsx"
grep -r "<textarea" --include="*.tsx" --include="*.jsx"
```

**Issue indicators:**

- Small input fields (< 44px height)
- Missing mobile-friendly input types (tel, email, url)
- No autocomplete attributes
- Labels not properly associated with inputs
- Tiny checkboxes/radio buttons

### Data Tables

Search for tables:

```bash
grep -r "<table" --include="*.tsx" --include="*.jsx"
```

**Issue indicators:**

- No horizontal scroll for wide tables
- No mobile-specific table view
- Tiny text in table cells
- Too many columns on mobile

### Performance Issues

**Unoptimized bundles:**

```bash
# Large imports (potential code splitting candidates)
grep -r "import.*from 'react'" --include="*.tsx" --include="*.jsx"

# Check for lazy loading
grep -r "React.lazy\|lazy(" --include="*.tsx" --include="*.jsx"
```

**Issue indicators:**

- No route-based code splitting
- No component lazy loading
- Heavy libraries imported at top level
- No dynamic imports for large components

### CSS Media Queries

Check responsive design approach:

```bash
# Find media queries
grep -r "@media" --include="*.css" --include="*.scss" --include="*.tsx"

# Check Tailwind responsive classes
grep -r "sm:\|md:\|lg:\|xl:" --include="*.tsx" --include="*.jsx"
```

**Issue indicators:**

- Desktop-first approach (max-width queries)
- Hardcoded breakpoints (should use Tailwind or design system)
- Inconsistent breakpoint usage
- Missing mobile styles

## Output Format

Create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md` with:

```markdown
# Mobile Issues - Loop {{LOOP_NUMBER}}

## Summary
- **Total Issues Found:** [count]
- **By Category:** [X] Navigation, [Y] Images, [Z] Touch Targets, [W] Forms, [V] Performance
- **By Priority:** [X] Critical, [Y] High, [Z] Medium, [W] Low

## Issue List

### ISSUE-001: Missing Viewport Meta Tag
- **Category:** Core Mobile Support
- **Priority:** CRITICAL
- **File:** `[app/layout.tsx or public/index.html]`
- **Current State:** No viewport meta tag found
- **Impact:** Site not mobile-responsive, zoomed out on mobile devices
- **Fix Required:** Add viewport meta tag to document head
- **Code Example:**
  ```tsx
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  ```

### ISSUE-002: Desktop-Only Navigation Menu

- **Category:** Navigation
- **Priority:** CRITICAL
- **File:** `[components/Header.tsx:15-45]`
- **Current State:** Horizontal menu links overflow on mobile
- **Impact:** Navigation unusable on screens < 768px
- **Fix Required:** Implement responsive hamburger menu for mobile
- **Approach:**
  1. Add mobile menu state (useState)
  2. Create hamburger icon button
  3. Implement mobile drawer/menu
  4. Add breakpoint to toggle desktop/mobile nav

### ISSUE-003: Unoptimized Hero Image

- **Category:** Images / Performance
- **Priority:** HIGH
- **File:** `[components/Hero.tsx:12]`
- **Current State:** Using regular `<img>` tag, 2.5MB PNG
- **Impact:** Slow page load on mobile networks, poor LCP score
- **Fix Required:**
  1. Convert to Next.js `<Image>` component (if using Next.js)
  2. Add lazy loading for below-fold images
  3. Provide multiple sizes with srcset
  4. Convert to WebP/AVIF format
- **Code Example:**

  ```tsx
  <Image
    src="/hero.jpg"
    alt="Hero image"
    width={1200}
    height={600}
    priority  // For above-fold images
    sizes="(max-width: 768px) 100vw, 1200px"
  />
  ```

### ISSUE-004: Small Touch Targets on CTA Buttons

- **Category:** Touch Targets / Accessibility
- **Priority:** HIGH
- **File:** `[components/CallToAction.tsx:8-12]`
- **Current State:** Buttons are 36×36px on mobile
- **Impact:** Difficult to tap, poor mobile UX, accessibility issue
- **Fix Required:** Increase to minimum 44×44px
- **Current Code:**

  ```tsx
  <button className="px-2 py-1 text-sm">
  ```

- **Fixed Code:**

  ```tsx
  <button className="px-4 py-3 text-base min-h-[44px]">
  ```

### ISSUE-005: Form Inputs Missing Mobile Input Types

- **Category:** Forms / UX
- **Priority:** MEDIUM
- **File:** `[components/ContactForm.tsx:22-35]`
- **Current State:** Email and phone inputs using type="text"
- **Impact:** Mobile keyboard doesn't show email/phone layout
- **Fix Required:** Use appropriate input types
- **Code Example:**

  ```tsx
  <input type="email" />  // Shows @ key
  <input type="tel" />    // Shows number pad
  <input type="url" />    // Shows .com key
  ```

### ISSUE-006: Data Table Horizontal Overflow

- **Category:** Tables / Layout
- **Priority:** MEDIUM
- **File:** `[components/PricingTable.tsx:15-60]`
- **Current State:** 6-column table breaks layout on mobile
- **Impact:** Content not accessible, horizontal scroll issues
- **Fix Required:** Implement responsive table pattern
- **Approaches:**
  1. Horizontal scroll container (simple)
  2. Stacked layout on mobile (better UX)
  3. Hide less important columns on mobile

### ISSUE-007: No Code Splitting for Routes

- **Category:** Performance
- **Priority:** MEDIUM
- **File:** `[app/page.tsx, various routes]`
- **Current State:** All routes loaded upfront
- **Impact:** Large initial bundle, slow FCP on mobile
- **Fix Required:** Implement route-based code splitting
- **Approach:** Use Next.js app router or React.lazy()

### ISSUE-008: Missing Lazy Loading on Gallery Images

- **Category:** Images / Performance
- **Priority:** MEDIUM
- **File:** `[components/Gallery.tsx:20-45]`
- **Current State:** 20+ images load immediately
- **Impact:** Slow page load, wasted bandwidth
- **Fix Required:** Add loading="lazy" or use Intersection Observer
- **Code Example:**

  ```tsx
  <img loading="lazy" src={...} />
  ```

### ISSUE-009: Desktop-First Media Queries

- **Category:** CSS / Architecture
- **Priority:** LOW
- **File:** `[styles/globals.css]`
- **Current State:** Using max-width media queries
- **Impact:** Mobile styles as overrides, larger CSS
- **Fix Required:** Refactor to mobile-first (min-width)
- **Note:** If using Tailwind, this is already mobile-first

### ISSUE-010: Modal Not Full-Screen on Mobile

- **Category:** UI Components
- **Priority:** MEDIUM
- **File:** `[components/Modal.tsx:15]`
- **Current State:** Fixed 600px width modal on all screens
- **Impact:** Modal too small on mobile, poor UX
- **Fix Required:** Make modal full-screen on mobile
- **Code Example:**

  ```tsx
  className="w-full max-w-2xl md:w-auto"
  ```

---

## Issues by Category

### Navigation (2 issues)

- ISSUE-002: Desktop-Only Navigation Menu [CRITICAL]
- ...

### Images / Performance (3 issues)

- ISSUE-003: Unoptimized Hero Image [HIGH]
- ISSUE-007: No Code Splitting [MEDIUM]
- ISSUE-008: Missing Lazy Loading [MEDIUM]

### Touch Targets (1 issue)

- ISSUE-004: Small CTA Buttons [HIGH]

### Forms (1 issue)

- ISSUE-005: Missing Mobile Input Types [MEDIUM]

### Layout (2 issues)

- ISSUE-006: Table Overflow [MEDIUM]
- ISSUE-010: Modal Size [MEDIUM]

### Architecture (1 issue)

- ISSUE-009: Desktop-First CSS [LOW]

## Issues by File

Quick reference of which files have the most issues:

| File | Issue Count | Categories |
|------|-------------|------------|
| `components/Header.tsx` | 1 | Navigation |
| `components/Hero.tsx` | 1 | Images |
| `components/ContactForm.tsx` | 1 | Forms |

## Dependencies Needed

New packages or tools that may be needed:

- **None** - If using Next.js (already has Image optimization)
- **react-lazy-load-image-component** - If not using Next.js and need lazy loading
- **clsx** or **classnames** - For conditional class management in mobile menus
- **@headlessui/react** - For accessible mobile menu/drawer components
- **framer-motion** - For mobile menu animations (optional)

## Performance Impact

Estimated impact of fixing these issues:

- **Largest Contentful Paint (LCP):** -40% (image optimization)
- **First Contentful Paint (FCP):** -25% (code splitting)
- **Cumulative Layout Shift (CLS):** -60% (image dimensions)
- **Total Bundle Size:** -30% (lazy loading, code splitting)

```

## Guidelines

- **Be specific**: Include exact file paths and line numbers
- **Explain impact**: Why does this matter for mobile users?
- **Suggest solutions**: Provide code examples when possible
- **Categorize**: Group related issues together
- **Prioritize**: CRITICAL > HIGH > MEDIUM > LOW
- **Link to standards**: Reference WCAG, Core Web Vitals when relevant

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Issues documented:**
1. You've examined the codebase for mobile anti-patterns
2. You've documented specific issues with file paths and line numbers
3. You've created `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md`

**Option B - Already mobile-optimized:**
1. The assessment shows comprehensive mobile optimization
2. No critical mobile issues found
3. Mark task complete without creating issues file
