# Mobile Polish Implementation - Apply the Fixes

## Context

- **Playbook:** Mobile Polish
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Implement mobile polish improvements for `PENDING` items from the evaluation phase. Apply fixes that make the React website mobile-friendly, following best practices for the detected tech stack.

## Instructions

1. **Read the plan** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`
2. **Find ONE `PENDING` item** (not `IMPLEMENTED`, `FUTURE`, or `PENDING - MANUAL REVIEW`)
3. **Implement the fix** following the tech stack's conventions
4. **Test the change** on mobile viewport (DevTools or real device)
5. **Update status** to `IMPLEMENTED` in the plan file
6. **Log changes** to `{{AUTORUN_FOLDER}}/MOBILE_LOG_{{AGENT_NAME}}_{{DATE}}.md`

## Implementation Checklist

- [ ] **Implement mobile fix (or skip if none)**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`. If the file doesn't exist OR contains no items with status exactly `PENDING`, mark this task complete without changes. Otherwise, implement exactly ONE `PENDING` item with EASY or MEDIUM effort. Follow framework conventions (Next.js, Tailwind, etc.). Test on mobile viewport. Update status to `IMPLEMENTED` in the plan. Log to `{{AUTORUN_FOLDER}}/MOBILE_LOG_{{AGENT_NAME}}_{{DATE}}.md`. Only implement ONE fix per task execution.

## Implementation Guidelines

### Before Implementing

1. **Read the component** - Understand current implementation
2. **Check tech stack** - Use framework-specific patterns (Next.js Image, Tailwind classes)
3. **Review the fix strategy** - Follow the plan's implementation steps
4. **Consider impact** - Don't break existing functionality

### Implementation Patterns by Fix Type

#### 1. Viewport Meta Tag

**Location:** Find the document head

- Next.js App Router: `app/layout.tsx`
- Next.js Pages Router: `pages/_document.tsx`
- CRA/Vite: `public/index.html` or `index.html`

**Implementation:**

```tsx
// Next.js App Router (app/layout.tsx)
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>{children}</body>
    </html>
  )
}

// Next.js Pages Router (pages/_document.tsx)
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}

// CRA/Vite (public/index.html)
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
```

#### 2. Responsive Hamburger Menu

**Pattern:** Mobile-first navigation with hamburger menu

```tsx
// components/Header.tsx
'use client' // If Next.js App Router

import { useState } from 'react'
import Link from 'next/link' // or react-router Link
import { Menu, X } from 'lucide-react' // or any icon library

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const links = [
    { href: '/', label: 'Home' },
    { href: '/about', label: 'About' },
    { href: '/services', label: 'Services' },
    { href: '/contact', label: 'Contact' },
  ]

  return (
    <header className="bg-white border-b">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        {/* Logo */}
        <Link href="/" className="text-xl font-bold">
          Logo
        </Link>

        {/* Desktop Navigation - hidden on mobile */}
        <nav className="hidden md:flex gap-6">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="hover:text-blue-600 transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* Mobile Hamburger Button - hidden on desktop */}
        <button
          onClick={() => setMobileMenuOpen(true)}
          className="md:hidden p-2"
          aria-label="Open menu"
          aria-expanded={mobileMenuOpen}
        >
          <Menu className="w-6 h-6" />
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
            onClick={() => setMobileMenuOpen(false)}
            aria-hidden="true"
          />

          {/* Menu Panel */}
          <div className="fixed inset-y-0 right-0 w-64 max-w-full bg-white z-50 p-6 md:hidden">
            {/* Close Button */}
            <button
              onClick={() => setMobileMenuOpen(false)}
              className="absolute top-4 right-4 p-2"
              aria-label="Close menu"
            >
              <X className="w-6 h-6" />
            </button>

            {/* Menu Links */}
            <nav className="flex flex-col gap-4 mt-12">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-lg hover:text-blue-600 transition-colors py-2"
                >
                  {link.label}
                </Link>
              ))}
            </nav>
          </div>
        </>
      )}
    </header>
  )
}
```

**With Animation (optional - using Tailwind):**

```tsx
{/* Animated backdrop */}
<div
  className={`fixed inset-0 bg-black/50 z-40 md:hidden transition-opacity ${
    mobileMenuOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
  }`}
  onClick={() => setMobileMenuOpen(false)}
/>

{/* Animated panel */}
<div
  className={`fixed inset-y-0 right-0 w-64 bg-white z-50 p-6 md:hidden transform transition-transform ${
    mobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
  }`}
>
  {/* content */}
</div>
```

#### 3. Image Optimization

**Next.js Image Component:**

```tsx
// Before
<img src="/hero.jpg" alt="Hero" />

// After
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // For above-fold images
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 1200px"
  className="w-full h-auto"
/>

// For below-fold images, omit priority to enable lazy loading
<Image
  src="/gallery-1.jpg"
  alt="Gallery image"
  width={800}
  height={600}
  sizes="(max-width: 768px) 100vw, 800px"
/>
```

**Regular HTML with Lazy Loading:**

```tsx
// For projects not using Next.js
<img
  src="/image.jpg"
  alt="Description"
  loading="lazy"
  width="800"
  height="600"
  className="w-full h-auto"
/>

// Responsive images with srcset
<img
  src="/image-800.jpg"
  srcSet="/image-400.jpg 400w, /image-800.jpg 800w, /image-1200.jpg 1200w"
  sizes="(max-width: 768px) 100vw, 800px"
  alt="Description"
  loading="lazy"
  width="800"
  height="600"
/>
```

#### 4. Touch Target Sizes

**Minimum 44×44px for all interactive elements:**

```tsx
// Before - too small
<button className="px-2 py-1 text-sm">
  Click Me
</button>

// After - minimum touch target
<button className="px-4 py-3 text-base min-h-[44px]">
  Click Me
</button>

// Icon buttons
<button
  className="p-3 min-h-[44px] min-w-[44px] flex items-center justify-center"
  aria-label="Search"
>
  <SearchIcon className="w-5 h-5" />
</button>

// Links
<Link
  href="/page"
  className="inline-block py-3 px-4 min-h-[44px] hover:bg-gray-100"
>
  Link Text
</Link>
```

#### 5. Mobile-Friendly Form Inputs

**Use appropriate input types and attributes:**

```tsx
<form>
  {/* Email - shows @ keyboard key */}
  <input
    type="email"
    name="email"
    autoComplete="email"
    required
    className="w-full px-4 py-3 border rounded-lg min-h-[44px]"
  />

  {/* Phone - shows number pad */}
  <input
    type="tel"
    name="phone"
    autoComplete="tel"
    className="w-full px-4 py-3 border rounded-lg min-h-[44px]"
  />

  {/* URL - shows .com key */}
  <input
    type="url"
    name="website"
    autoComplete="url"
    className="w-full px-4 py-3 border rounded-lg min-h-[44px]"
  />

  {/* Numeric input */}
  <input
    type="text"
    inputMode="numeric"
    pattern="[0-9]*"
    name="zip"
    autoComplete="postal-code"
    className="w-full px-4 py-3 border rounded-lg min-h-[44px]"
  />

  {/* Date - shows date picker */}
  <input
    type="date"
    name="birthdate"
    autoComplete="bday"
    className="w-full px-4 py-3 border rounded-lg min-h-[44px]"
  />
</form>
```

#### 6. Responsive Tables

**Horizontal scroll container:**

```tsx
// components/PricingTable.tsx
<div className="overflow-x-auto">
  <table className="min-w-full divide-y divide-gray-200">
    <thead>
      <tr>
        <th className="px-6 py-3 text-left">Feature</th>
        <th className="px-6 py-3 text-left">Basic</th>
        <th className="px-6 py-3 text-left">Pro</th>
        <th className="px-6 py-3 text-left">Enterprise</th>
      </tr>
    </thead>
    <tbody>
      {/* table rows */}
    </tbody>
  </table>
</div>

// Optional: Add scroll indicator
<div className="relative">
  <div className="overflow-x-auto">
    <table className="min-w-full">
      {/* content */}
    </table>
  </div>
  <div className="md:hidden text-center text-sm text-gray-500 mt-2">
    ← Scroll to see more →
  </div>
</div>
```

Alternative: Stacked layout on mobile

```tsx
{/* Desktop: table, Mobile: stacked cards */}
<div className="hidden md:block">
  <table>{/* regular table */}</table>
</div>

<div className="md:hidden space-y-4">
  {data.map((row) => (
    <div key={row.id} className="border rounded-lg p-4">
      <div className="font-bold">{row.name}</div>
      <div className="text-sm text-gray-600">{row.price}</div>
      {/* other fields */}
    </div>
  ))}
</div>
```

#### 7. Lazy Loading Images

```tsx
// Gallery component with lazy loading
export function Gallery({ images }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {images.map((image, index) => (
        <img
          key={image.id}
          src={image.src}
          alt={image.alt}
          width={image.width}
          height={image.height}
          loading={index < 3 ? 'eager' : 'lazy'} // First 3 eager, rest lazy
          className="w-full h-auto rounded-lg"
        />
      ))}
    </div>
  )
}
```

### Testing Checklist

After implementing, verify:

- [ ] **Mobile viewport test** - Use Chrome DevTools responsive mode (375px, 768px, 1024px)
- [ ] **Touch target sizes** - All buttons/links are tappable
- [ ] **Navigation works** - Menu opens/closes on mobile
- [ ] **Images load** - Lazy loading works, no layout shift
- [ ] **Forms usable** - Correct keyboards appear on mobile
- [ ] **No horizontal scroll** - Content fits viewport
- [ ] **Accessibility** - Screen reader can navigate
- [ ] **Visual regression** - Desktop layout not broken

## Update Plan Status

After implementing, update `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`:

```markdown
### FIX-001: Add Viewport Meta Tag
- **Status:** `IMPLEMENTED`  ← Changed from PENDING
- **Implemented In:** Loop {{LOOP_NUMBER}}
- **File Modified:** `app/layout.tsx`
- **Changes Made:**
  - Added viewport meta tag to document head
  - Verified on mobile DevTools (375px, 768px)
- **Test Results:** ✅ Site now responsive, no horizontal scroll
```

## Log Format

Append to `{{AUTORUN_FOLDER}}/MOBILE_LOG_{{AGENT_NAME}}_{{DATE}}.md`:

```markdown
## Loop {{LOOP_NUMBER}} - [Timestamp]

### Implementation

#### FIX-001: Add Viewport Meta Tag
- **Status:** IMPLEMENTED ✅
- **File Modified:** `app/layout.tsx`
- **Category:** Core Mobile Support
- **Changes Made:**
  ```tsx
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  ```

- **Testing:**
  - ✅ Tested on Chrome DevTools (375px, 768px, 1024px)
  - ✅ No horizontal scroll
  - ✅ Content scales correctly
- **Impact:**
  - Site now mobile-responsive
  - Foundation for all other mobile improvements

---

```

## Quality Checks

Before marking as IMPLEMENTED:

- [ ] Code follows project conventions (Tailwind patterns, component structure)
- [ ] Mobile viewport tested (375px minimum)
- [ ] Desktop layout not broken
- [ ] Accessibility not regressed
- [ ] No console errors
- [ ] Performance not degraded
- [ ] Changes are minimal and focused

## Common Issues & Solutions

### Issue: State not updating in mobile menu
**Solution:** Ensure component is marked `'use client'` in Next.js App Router

### Issue: Images causing layout shift
**Solution:** Always provide explicit width and height attributes

### Issue: Touch targets still small despite padding
**Solution:** Use `min-h-[44px]` and `min-w-[44px]` classes

### Issue: Tailwind responsive classes not working
**Solution:** Verify Tailwind is configured, check class order (mobile-first)

### Issue: Menu doesn't close on route change
**Solution:** Add route change listener or onClick handler to links

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Implemented a fix:**
1. You've implemented exactly ONE fix from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`
2. You've tested the change on mobile viewport
3. You've updated the item status to `IMPLEMENTED` in the plan
4. You've logged the changes to `{{AUTORUN_FOLDER}}/MOBILE_LOG_{{AGENT_NAME}}_{{DATE}}.md`

**Option B - No PENDING items available:**
1. Plan file doesn't exist, OR
2. It contains no items with status exactly `PENDING`
3. Mark this task complete without changes

## When No Fixes Are Available

If there are no `PENDING` items in the plan file, append to the log:

```markdown
---

## [YYYY-MM-DD HH:MM] - Loop {{LOOP_NUMBER}} Complete

**Agent:** {{AGENT_NAME}}
**Project:** {{AGENT_PATH}}
**Loop:** {{LOOP_NUMBER}}
**Status:** No PENDING fixes available

**Summary:**
- Fixes IMPLEMENTED: [count]
- Fixes FUTURE: [count]
- Fixes PENDING - MANUAL REVIEW: [count]

**Mobile-Ready Status:** [Assessment of current state]

**Recommendation:** [Either "All automatable fixes complete" or "Remaining fixes need manual review"]
```
