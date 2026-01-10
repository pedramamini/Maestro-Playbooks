# Mobile Polish Playbook

A comprehensive, step-by-step playbook for implementing mobile-friendly features and optimizations in React-based websites (including Next.js, Tailwind CSS, and other modern React variants).

## Overview

This playbook systematically transforms a desktop-focused React website into a mobile-optimized, responsive experience. It covers everything from basic viewport configuration to advanced responsive patterns like hamburger menus, touch-optimized interfaces, and performance optimizations.

## What This Playbook Does

The Mobile Polish playbook implements:

1. **Core Mobile Foundation**
   - Viewport meta tag configuration
   - Mobile-first responsive design principles
   - Proper breakpoint implementation

2. **Responsive Navigation**
   - Hamburger menu for mobile devices
   - Drawer/slide-out navigation patterns
   - Adaptive menu based on screen size
   - Accessible mobile navigation

3. **Touch Optimization**
   - Minimum 44×44px touch targets (WCAG compliant)
   - Adequate spacing between interactive elements
   - Mobile-friendly button and link sizes
   - Touch-optimized form controls

4. **Image Optimization**
   - Lazy loading for below-fold images
   - Responsive images with srcset
   - Next.js Image component integration (if applicable)
   - WebP/AVIF format support
   - Prevent Cumulative Layout Shift (CLS)

5. **Form Optimization**
   - Mobile-friendly input types (email, tel, url)
   - Appropriate mobile keyboards
   - Autocomplete attributes
   - Touch-friendly form controls

6. **Layout Responsiveness**
   - Responsive tables (horizontal scroll or stacked)
   - Mobile-optimized modals and dialogs
   - Flexible grid and flexbox layouts
   - No horizontal scroll on mobile

7. **Performance Optimizations**
   - Code splitting for routes
   - Component lazy loading
   - Bundle size optimization
   - Mobile network considerations

## Tech Stack Support

This playbook intelligently adapts to your React setup:

- **React + Next.js** - Leverages Next.js Image component, App Router, Pages Router
- **React + Tailwind CSS** - Uses Tailwind responsive utilities and mobile-first approach
- **React + Vite/CRA** - Implements standard responsive patterns
- **TypeScript** - Full TypeScript support
- **CSS Modules / styled-components** - Adapts to your styling solution

## Playbook Structure

The playbook consists of 5 phases that run in sequence:

| Document | Purpose | Output Files | Reset on Completion |
|----------|---------|--------------|---------------------|
| **1_ANALYZE** | Identify tech stack, assess current mobile support, map navigation patterns | `LOOP_N_MOBILE_ASSESSMENT.md` | No |
| **2_FIND_ISSUES** | Search for mobile anti-patterns, missing optimizations, navigation issues | `LOOP_N_MOBILE_ISSUES.md` | No |
| **3_EVALUATE** | Rate issues by impact/effort, assign priority, group improvements | `LOOP_N_MOBILE_PLAN.md` | No |
| **4_IMPLEMENT** | Implement ONE pending fix per loop, test on mobile viewports | Updates to plan file, `MOBILE_LOG_<agent>_<date>.md` | No |
| **5_PROGRESS** | Count completed fixes, test mobile experience, decide loop continuation | `LOOP_N_PROGRESS.md` | Yes (resets docs 1-4 if continuing) |

### Document Details

#### 1. ANALYZE - Project Assessment

- Identifies tech stack (React version, Next.js, Tailwind, etc.)
- Assesses current mobile support
- Maps navigation patterns
- Documents baseline mobile readiness
- **Output:** `MOBILE_ASSESSMENT.md`

#### 2. FIND_ISSUES - Discover Mobile Problems

- Searches for mobile anti-patterns
- Identifies missing optimizations
- Finds navigation issues
- Documents touch target problems
- **Output:** `MOBILE_ISSUES.md`

#### 3. EVALUATE - Prioritize Improvements

- Rates issues by impact (CRITICAL/HIGH/MEDIUM/LOW)
- Rates issues by effort (EASY/MEDIUM/HARD)
- Assigns implementation status (PENDING/MANUAL REVIEW/FUTURE)
- Groups related improvements
- **Output:** `MOBILE_PLAN.md`

#### 4. IMPLEMENT - Apply Fixes

- Implements ONE pending fix per loop iteration
- Follows framework-specific best practices
- Tests on mobile viewports
- Updates implementation status
- **Output:** Updates to plan file, `MOBILE_LOG.md`

#### 5. PROGRESS - Track & Decide

- Counts completed vs pending fixes
- Tests mobile experience
- Measures improvement metrics
- Decides whether to continue looping
- **Output:** `PROGRESS.md` with CONTINUE/STOP recommendation

## How to Use

### Prerequisites

- Maestro installed and configured
- React-based web project
- Access to the codebase

### Running the Playbook

1. **Open Maestro** and navigate to your React project
2. **Import this playbook** into Maestro's Auto Run
3. **Configure loop settings** (recommended: 5-10 loops)
4. **Start Auto Run** and monitor progress
5. **Review outputs** in the `{{AUTORUN_FOLDER}}` directory

### Typical Workflow

**Loop 1:**

- Analyzes project structure
- Identifies tech stack
- Finds 10+ mobile issues
- Prioritizes fixes
- Implements viewport meta tag
- Continues ✅

**Loop 2:**

- Implements responsive hamburger menu
- Continues ✅

**Loop 3:**

- Optimizes images with lazy loading
- Implements mobile input types
- Continues ✅

**Loop 4:**

- Increases touch target sizes
- Makes tables responsive
- Continues ✅

**Loop 5:**

- All CRITICAL and HIGH priority fixes complete
- Remaining items need manual review
- Stops 🛑

### Expected Outputs

After running this playbook, you'll have:

- **Fully responsive navigation** - Works on all screen sizes
- **Mobile-optimized images** - Fast loading, no layout shift
- **Touch-friendly interface** - All elements easily tappable
- **Better performance** - Improved Core Web Vitals scores
- **Accessible mobile experience** - WCAG compliant
- **Comprehensive documentation** - All changes logged

## Key Features

### Incremental Implementation

The playbook implements ONE fix at a time, allowing you to:

- Review each change individually
- Maintain code quality
- Avoid breaking changes
- Track progress clearly

### Framework-Aware

Automatically detects and uses:

- Next.js `<Image>` component for optimization
- Tailwind responsive utilities (`sm:`, `md:`, `lg:`)
- Next.js App Router or Pages Router patterns
- Project-specific component conventions

### Mobile-First Approach

Follows industry best practices:

- Mobile-first CSS (min-width media queries)
- Progressive enhancement
- Touch-first interactions
- Performance optimization for mobile networks

### Accessibility Built-In

All implementations include:

- ARIA labels for screen readers
- Keyboard navigation support
- WCAG 2.5.5 compliant touch targets (44×44px)
- Color contrast verification
- Focus indicators

## Common Improvements

### Navigation Transformation

**Before:**

```tsx
<nav>
  <Link href="/">Home</Link>
  <Link href="/about">About</Link>
  <Link href="/services">Services</Link>
  <Link href="/contact">Contact</Link>
</nav>
```

**After:**

```tsx
{/* Desktop */}
<nav className="hidden md:flex gap-6">
  {links.map(link => <Link href={link.href}>{link.label}</Link>)}
</nav>

{/* Mobile */}
<button className="md:hidden" onClick={() => setMenuOpen(true)}>
  <MenuIcon />
</button>

{menuOpen && <MobileDrawer links={links} onClose={() => setMenuOpen(false)} />}
```

### Image Optimization

**Before:**

```tsx
<img src="/hero.jpg" alt="Hero" />
```

**After:**

```tsx
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority
  sizes="(max-width: 768px) 100vw, 1200px"
/>
```

### Touch Targets

**Before:**

```tsx
<button className="px-2 py-1 text-sm">Click</button>
```

**After:**

```tsx
<button className="px-4 py-3 text-base min-h-[44px]">Click</button>
```

## Performance Impact

Expected improvements after full implementation:

- **Mobile Lighthouse Score:** +20-30 points
- **Largest Contentful Paint (LCP):** -30-50% faster
- **Cumulative Layout Shift (CLS):** Near 0 (< 0.1)
- **First Input Delay (FID):** < 100ms
- **Bundle Size:** -20-40% reduction (with code splitting)

## Manual Review Items

Some improvements require human decision-making:

- **Code Splitting Strategy** - Route-based vs component-based
- **Mobile Menu Design** - Drawer vs full-screen vs accordion
- **Image CDN Setup** - If not using Next.js Image
- **Breakpoint Values** - Custom breakpoints for specific designs
- **Animation Preferences** - Menu transitions, page animations

## Best Practices Implemented

This playbook follows current web standards (2025):

1. **Mobile-First CSS** - Start with mobile, enhance for desktop
2. **WCAG 2.1/2.2 Compliance** - Accessibility guidelines
3. **Core Web Vitals** - Google's performance metrics
4. **Progressive Enhancement** - Works without JavaScript
5. **Semantic HTML** - Proper HTML structure
6. **Touch-Optimized** - 44×44px minimum touch targets
7. **Responsive Images** - srcset, sizes, lazy loading
8. **Modern Image Formats** - WebP, AVIF support

## Customization

### Adjusting Priorities

Edit `3_EVALUATE.md` to customize impact ratings:

- Change CRITICAL thresholds
- Adjust effort estimates
- Modify auto-implementation criteria

### Adding Custom Checks

Edit `2_FIND_ISSUES.md` to add project-specific patterns:

- Custom component checks
- Framework-specific anti-patterns
- Business-specific mobile requirements

### Tailoring Implementation

Edit `4_IMPLEMENT.md` to adjust:

- Code patterns and styles
- Component libraries (Headless UI, Radix, etc.)
- Animation libraries (Framer Motion, React Spring)

## Troubleshooting

### Common Issues

**Issue:** Tailwind responsive classes not working

- **Solution:** Verify Tailwind configuration, check PurgeCSS settings

**Issue:** Next.js Image component errors

- **Solution:** Configure image domains in `next.config.js`

**Issue:** Mobile menu state not updating

- **Solution:** Ensure `'use client'` directive in Next.js App Router

**Issue:** Touch targets still small despite classes

- **Solution:** Use `min-h-[44px]` and `min-w-[44px]` utilities

## Resources

### Responsive Design

- [MDN Responsive Design](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design)
- [Tailwind Responsive Design](https://tailwindcss.com/docs/responsive-design)

### Touch Targets

- [WCAG 2.5.5 Target Size](https://www.w3.org/WAI/WCAG21/Understanding/target-size.html)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/touchscreen-gestures)

### Images

- [Next.js Image Optimization](https://nextjs.org/docs/pages/building-your-application/optimizing/images)
- [web.dev Image Optimization](https://web.dev/fast/#optimize-your-images)

### Performance

- [Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse Performance](https://developer.chrome.com/docs/lighthouse/performance/)

## Contributing

Found a mobile pattern not covered? Have a better implementation approach? Contributions are welcome!

1. Test the pattern on multiple devices/viewports
2. Ensure WCAG compliance
3. Document the approach
4. Submit a pull request

## License

This playbook is part of the maestro-playbooks repository and is licensed under AGPL-3.0, the same as Maestro itself.
