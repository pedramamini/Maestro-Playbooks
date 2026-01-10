# Mobile Polish Evaluation - Prioritize Improvements

## Context

- **Playbook:** Mobile Polish
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Evaluate each mobile polish issue from the discovery phase and assign priority and implementation difficulty ratings. This ensures we implement the most impactful improvements first.

## Instructions

1. **Read the issues list** from `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md`
2. **Rate each issue** for user impact and implementation difficulty
3. **Assign implementation status** based on ratings
4. **Group related improvements** that can be done together
5. **Output prioritized plan** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`

## Evaluation Checklist

- [ ] **Evaluate issues (or skip if empty)**: Read `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ISSUES.md`. If it contains no issues OR all issues have been evaluated in `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`, mark this task complete without changes. Otherwise, rate each issue by IMPACT (CRITICAL/HIGH/MEDIUM/LOW) and EFFORT (EASY/MEDIUM/HARD). Mark EASY+HIGH impact or better as PENDING for auto-implementation. Output to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`.

## Rating Criteria

### Impact Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Makes site unusable on mobile, affects all users, SEO impact | Missing viewport tag, broken navigation, major layout breaks |
| **HIGH** | Significantly degrades UX, affects Core Web Vitals, accessibility issues | Large unoptimized images, small touch targets, slow load times |
| **MEDIUM** | Noticeable UX issues, affects some user journeys | Missing input types, table overflow, non-optimized forms |
| **LOW** | Minor polish, edge cases, nice-to-have improvements | Animation tweaks, minor spacing issues, desktop-first CSS refactor |

### Effort Levels

| Level | Criteria | Time Estimate |
|-------|----------|---------------|
| **EASY** | Single file change, configuration update, add attributes | < 30 min |
| **MEDIUM** | New component, refactor existing component, add state management | 30 min - 2 hours |
| **HARD** | Major refactor, multiple components, testing across breakpoints | 2+ hours |

### Auto-Implementation Criteria

Improvements will be auto-implemented if:

- **Impact:** HIGH or CRITICAL
- **Effort:** EASY or MEDIUM

Improvements marked `PENDING - MANUAL REVIEW` if:

- **Impact:** CRITICAL but **Effort:** HARD
- Complex architectural changes
- Require design decisions

Improvements marked `FUTURE` if:

- **Impact:** LOW or MEDIUM with **Effort:** HARD
- Nice-to-have but significant work
- Can be done in future iterations

## Output Format

Create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md` with:

```markdown
# Mobile Polish Implementation Plan - Loop {{LOOP_NUMBER}}

## Summary
- **Total Items:** [count]
- **Auto-Implement (PENDING):** [count]
- **Manual Review:** [count]
- **Future Iteration:** [count]

## Current State
- **Mobile-Ready Score:** [X/10]
- **Core Web Vitals:** [Status from assessment]
- **Accessibility Score:** [Status from assessment]

## Target State
- **Mobile-Ready Score:** 9/10
- **All CRITICAL issues:** Resolved
- **Touch Target Compliance:** 100%
- **Image Optimization:** Complete

---

## PENDING - Ready for Auto-Implementation

### FIX-001: Add Viewport Meta Tag
- **Status:** `PENDING`
- **Issue ID:** ISSUE-001
- **File:** `app/layout.tsx` or `public/index.html`
- **Impact:** CRITICAL
- **Effort:** EASY
- **Category:** Core Mobile Support
- **Implementation Steps:**
  1. Locate document head (layout.tsx for Next.js App Router, _document.tsx for Pages Router, index.html for CRA/Vite)
  2. Add viewport meta tag: `<meta name="viewport" content="width=device-width, initial-scale=1" />`
  3. Verify on mobile device or DevTools
- **Acceptance Criteria:**
  - Viewport meta tag present in HTML head
  - Site scales correctly on mobile devices
  - No horizontal scroll on mobile

### FIX-002: Implement Responsive Hamburger Menu
- **Status:** `PENDING`
- **Issue ID:** ISSUE-002
- **File:** `components/Header.tsx`
- **Impact:** CRITICAL
- **Effort:** MEDIUM
- **Category:** Navigation
- **Implementation Steps:**
  1. Add mobile menu state: `const [mobileMenuOpen, setMobileMenuOpen] = useState(false)`
  2. Create hamburger button component (visible on mobile only)
  3. Create mobile menu drawer/panel
  4. Add Tailwind responsive classes to hide desktop nav on mobile: `className="hidden md:flex"`
  5. Add close button in mobile menu
  6. Implement backdrop overlay when menu open
  7. Add proper ARIA labels for accessibility
- **Acceptance Criteria:**
  - Desktop navigation shows horizontal links (>= 768px)
  - Mobile shows hamburger icon (< 768px)
  - Mobile menu opens/closes on hamburger click
  - Menu accessible via keyboard
  - Smooth animation (optional)
- **Code Pattern (Tailwind + Next.js):**
  ```tsx
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <header>
      {/* Desktop nav */}
      <nav className="hidden md:flex gap-6">
        {links.map(link => <Link href={link.href}>{link.label}</Link>)}
      </nav>

      {/* Mobile hamburger */}
      <button
        onClick={() => setMobileMenuOpen(true)}
        className="md:hidden"
        aria-label="Open menu"
      >
        <MenuIcon />
      </button>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <>
          <div className="fixed inset-0 bg-black/50 z-40" onClick={() => setMobileMenuOpen(false)} />
          <div className="fixed inset-y-0 right-0 w-64 bg-white z-50 p-6">
            <button onClick={() => setMobileMenuOpen(false)}>Close</button>
            <nav className="flex flex-col gap-4 mt-8">
              {links.map(link => <Link href={link.href}>{link.label}</Link>)}
            </nav>
          </div>
        </>
      )}
    </header>
  )
  ```

### FIX-003: Optimize Hero Image with Next.js Image Component

- **Status:** `PENDING`
- **Issue ID:** ISSUE-003
- **File:** `components/Hero.tsx`
- **Impact:** HIGH
- **Effort:** EASY
- **Category:** Performance / Images
- **Implementation Steps:**
  1. Replace `<img>` with Next.js `<Image>` component (if using Next.js)
  2. Add explicit width and height props
  3. Add priority prop for above-fold images
  4. Add sizes attribute for responsive images
  5. Ensure image is in proper format (WebP/AVIF preferred)
- **Acceptance Criteria:**
  - Using Next.js Image component (or equivalent)
  - No layout shift (CLS = 0)
  - Image lazy loads if below fold
  - Proper sizes for different viewports
- **Mocks/Dependencies:** Next.js Image component, or alternative: react-lazy-load-image-component

### FIX-004: Increase Touch Target Sizes

- **Status:** `PENDING`
- **Issue ID:** ISSUE-004
- **File:** `components/CallToAction.tsx` and other button components
- **Impact:** HIGH
- **Effort:** EASY
- **Category:** Accessibility / Touch Targets
- **Implementation Steps:**
  1. Find all buttons/links with small touch targets
  2. Update padding to ensure minimum 44×44px
  3. Use Tailwind classes: `px-4 py-3 min-h-[44px]` or `p-3 min-h-[44px] min-w-[44px]`
  4. For icon buttons, add padding around icon
- **Acceptance Criteria:**
  - All interactive elements >= 44×44px
  - Touch targets have adequate spacing (8px minimum)
  - Passes WCAG 2.5.5 Target Size guidelines
- **Pattern:**

  ```tsx
  // Before
  <button className="px-2 py-1 text-sm">Click</button>

  // After
  <button className="px-4 py-3 text-base min-h-[44px]">Click</button>
  ```

### FIX-005: Add Mobile-Friendly Input Types

- **Status:** `PENDING`
- **Issue ID:** ISSUE-005
- **File:** `components/ContactForm.tsx`
- **Impact:** MEDIUM
- **Effort:** EASY
- **Category:** Forms / UX
- **Implementation Steps:**
  1. Update email inputs: `type="email"`
  2. Update phone inputs: `type="tel"`
  3. Update URL inputs: `type="url"`
  4. Add autocomplete attributes where appropriate
  5. Add inputMode for numeric inputs if needed
- **Acceptance Criteria:**
  - Correct mobile keyboard shown for each input type
  - Autocomplete works where appropriate
  - Form validation uses browser native features
- **Example:**

  ```tsx
  <input type="email" autoComplete="email" />
  <input type="tel" autoComplete="tel" />
  <input type="url" autoComplete="url" />
  <input type="text" inputMode="numeric" pattern="[0-9]*" /> // For numbers
  ```

### FIX-006: Make Tables Responsive with Horizontal Scroll

- **Status:** `PENDING`
- **Issue ID:** ISSUE-006
- **File:** `components/PricingTable.tsx`
- **Impact:** MEDIUM
- **Effort:** EASY
- **Category:** Layout / Tables
- **Implementation Steps:**
  1. Wrap table in overflow container
  2. Add horizontal scroll on mobile
  3. Add visual indicator for scrollability (optional)
  4. Consider hiding less important columns on mobile (if applicable)
- **Acceptance Criteria:**
  - Table scrolls horizontally on mobile
  - Layout doesn't break
  - User can access all table content
- **Pattern:**

  ```tsx
  <div className="overflow-x-auto">
    <table className="min-w-full">
      {/* table content */}
    </table>
  </div>
  ```

### FIX-007: Add Lazy Loading to Gallery Images

- **Status:** `PENDING`
- **Issue ID:** ISSUE-008
- **File:** `components/Gallery.tsx`
- **Impact:** MEDIUM
- **Effort:** EASY
- **Category:** Performance / Images
- **Implementation Steps:**
  1. Add `loading="lazy"` to all below-fold images
  2. Keep first 2-3 images eager (above fold)
  3. Add width/height to prevent CLS
  4. Consider using Intersection Observer for more control
- **Acceptance Criteria:**
  - Below-fold images lazy load
  - Above-fold images load immediately
  - No layout shift during load
- **Pattern:**

  ```tsx
  {images.map((img, i) => (
    <img
      src={img.src}
      loading={i < 3 ? "eager" : "lazy"}
      width={img.width}
      height={img.height}
    />
  ))}
  ```

---

## PENDING - MANUAL REVIEW

### FIX-XXX: Implement Code Splitting for Routes

- **Status:** `PENDING - MANUAL REVIEW`
- **Issue ID:** ISSUE-007
- **File:** Multiple route files
- **Impact:** HIGH
- **Effort:** HARD
- **Category:** Performance / Architecture
- **Reason for Review:** Requires understanding of route structure and dependencies
- **Recommended Approach:**
  1. Use Next.js App Router (automatic code splitting)
  2. Or use React.lazy() for route components
  3. Add Suspense boundaries with loading states
  4. Measure bundle size impact
- **Considerations:**
  - May need to update routing setup
  - Should add loading skeletons
  - Test that all routes work after refactor

---

## FUTURE ITERATION

### FIX-XXX: Refactor to Mobile-First CSS

- **Status:** `FUTURE`
- **Issue ID:** ISSUE-009
- **File:** `styles/globals.css`
- **Impact:** LOW
- **Effort:** HARD
- **Category:** Architecture / CSS
- **Reason:** Large refactor, low user impact if using Tailwind
- **Notes:** If using Tailwind, already mobile-first. If using custom CSS, consider migration in future sprint.

---

## Implementation Groups

Tasks that share setup or can be done together:

### Group A: Core Mobile Foundation (FIX-001, FIX-002)

- Viewport meta tag
- Responsive navigation
- **Impact:** Unlocks mobile usability
- **Recommended Order:** FIX-001 first (prerequisite), then FIX-002

### Group B: Image Optimization (FIX-003, FIX-007)

- Hero image optimization
- Gallery lazy loading
- **Impact:** Major performance improvement
- **Can be done in parallel**

### Group C: Touch & Forms (FIX-004, FIX-005)

- Touch target sizes
- Mobile input types
- **Impact:** Better mobile UX
- **Quick wins, do together**

### Group D: Layout Polish (FIX-006)

- Responsive tables
- **Impact:** Content accessibility
- **Independent, do anytime**

## Estimated Timeline

Based on effort ratings:

- **Loop {{LOOP_NUMBER}}:** FIX-001, FIX-004, FIX-005, FIX-007 (4 EASY tasks)
- **Loop {{LOOP_NUMBER + 1}}:** FIX-002, FIX-003, FIX-006 (3 MEDIUM tasks)
- **Manual Review:** Code splitting (1 HARD task)
- **Future:** CSS architecture refactor

## Success Metrics

After implementation, the site should achieve:

- ✅ 100% viewport compliance
- ✅ Usable navigation on all screen sizes
- ✅ LCP < 2.5s on mobile
- ✅ CLS < 0.1
- ✅ All touch targets >= 44×44px
- ✅ 90+ mobile Lighthouse score

```

## Guidelines

- **Balance impact and effort**: High impact + easy effort = do first
- **Group related work**: Don't split related improvements across loops
- **Be realistic about complexity**: Some changes require design input
- **Consider dependencies**: Viewport before responsive components
- **Measure impact**: Note which fixes improve Core Web Vitals

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Plan created:**
1. You've rated all issues from the issues file
2. You've assigned status (PENDING, MANUAL REVIEW, FUTURE)
3. You've grouped related improvements
4. You've created `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_PLAN.md`

**Option B - No issues to evaluate:**
1. Issues file doesn't exist or contains no issues
2. All issues already evaluated in existing plan
3. Mark task complete without changes
