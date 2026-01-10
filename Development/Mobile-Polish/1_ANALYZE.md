# Mobile Polish Analysis - Project Assessment

## Context

- **Playbook:** Mobile Polish
- **Agent:** {{AGENT_NAME}}
- **Project:** {{AGENT_PATH}}
- **Auto Run Folder:** {{AUTORUN_FOLDER}}
- **Loop:** {{LOOP_NUMBER}}

## Objective

Analyze the React-based website to understand its current mobile-readiness state, identify the tech stack (React, Next.js, Tailwind, etc.), and establish a baseline for mobile polish improvements.

## Instructions

1. **Identify the tech stack** - Detect React version, framework (Next.js, CRA, Vite), CSS approach (Tailwind, CSS Modules, styled-components)
2. **Assess current mobile support** - Check viewport meta tag, responsive CSS, mobile testing setup
3. **Identify navigation patterns** - Locate header/navbar components, understand current navigation structure
4. **Document mobile-critical areas** - Forms, images, interactive elements, data tables
5. **Output assessment report** to `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ASSESSMENT.md`

## Analysis Checklist

- [ ] **Assess mobile readiness (if needed)**: First check if `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ASSESSMENT.md` already exists with tech stack and baseline assessment. If it does, skip the analysis and mark this task complete—the assessment is already in place. If it doesn't exist, examine the project structure, identify frameworks and libraries, check for existing mobile optimizations, and document current state.

## What to Identify

### Tech Stack Detection

Look for these files and configurations:

- **package.json** - Check dependencies for:
  - `react`, `react-dom` (version)
  - `next` (Next.js)
  - `tailwindcss`, `@tailwindcss/*`
  - `styled-components`, `@emotion/*`, `css-modules`
  - `react-responsive`, `react-device-detect`

- **Configuration files**:
  - `next.config.js` / `next.config.mjs` (Next.js)
  - `tailwind.config.js` / `tailwind.config.ts` (Tailwind)
  - `vite.config.js` (Vite)
  - `tsconfig.json` (TypeScript)

### Current Mobile Support

Check for existing mobile optimizations:

1. **Viewport Meta Tag**
   - Search for `<meta name="viewport"` in HTML/JSX files
   - Expected: `<meta name="viewport" content="width=device-width, initial-scale=1" />`

2. **Responsive CSS**
   - Tailwind: Check for responsive classes (`sm:`, `md:`, `lg:`, `xl:`)
   - Media queries: Search for `@media` in CSS/SCSS files
   - Mobile-first approach: Look for `min-width` vs `max-width`

3. **Images**
   - Check for `srcset`, `sizes` attributes
   - Next.js `<Image>` component usage
   - Lazy loading: `loading="lazy"` attribute

4. **Navigation**
   - Find header/navbar components
   - Check for mobile menu implementation
   - Look for hamburger menu or drawer patterns

### Mobile-Critical Areas

Identify components that need mobile optimization:

- **Navigation/Header** - Desktop links vs mobile menu
- **Forms** - Input sizes, touch targets, validation
- **Images/Media** - Responsive images, lazy loading
- **Tables** - Horizontal scroll or stacked layouts
- **Modals/Dialogs** - Full-screen on mobile
- **Touch Interactions** - Buttons, swipe gestures

## Output Format

Create `{{AUTORUN_FOLDER}}/LOOP_{{LOOP_NUMBER}}_MOBILE_ASSESSMENT.md` with:

```markdown
# Mobile Assessment Report - Loop {{LOOP_NUMBER}}

## Tech Stack

- **React Version:** [version]
- **Framework:** [Next.js 14 | Create React App | Vite | Other]
- **TypeScript:** [Yes/No]
- **CSS Solution:** [Tailwind CSS | styled-components | CSS Modules | SCSS | Other]
- **Build Tool:** [Webpack | Vite | Turbopack | Other]

## Current Mobile Support

### Viewport Configuration
- **Status:** [✅ Configured | ❌ Missing | ⚠️ Needs Update]
- **Current Tag:** [paste tag if exists]
- **Location:** [file path]

### Responsive Design Approach
- **Method:** [Mobile-first | Desktop-first | Not responsive]
- **Breakpoints:** [List breakpoint values if using Tailwind or custom]
- **Coverage:** [Estimate % of components that are responsive]

### Performance Optimizations
- **Image Optimization:** [✅ Yes | ❌ No | ⚠️ Partial]
  - Lazy loading: [status]
  - Responsive images: [status]
  - Next.js Image component: [if applicable]

- **Code Splitting:** [✅ Yes | ❌ No]
  - Route-based: [status]
  - Component lazy loading: [status]

- **Asset Optimization:** [✅ Yes | ❌ No]
  - Minification: [status]
  - Compression: [status]

## Navigation Assessment

### Header/Navbar
- **Component Location:** `[path/to/header.tsx]`
- **Current Mobile Handling:** [Describe - e.g., "Desktop links only, no mobile menu"]
- **Menu Items Count:** [number]
- **Mobile Menu:** [✅ Implemented | ❌ Missing | ⚠️ Needs Improvement]

### Navigation Pattern
- **Type:** [Hamburger menu | Drawer | Tab bar | None]
- **Implementation:** [CSS-only | JS-based | Not implemented]

## Mobile-Critical Components

### Forms
| Form Location | Mobile-Ready? | Issues |
|---------------|---------------|--------|
| [path] | [✅/❌/⚠️] | [List issues] |

### Images
| Image Usage | Optimization | Issues |
|-------------|--------------|--------|
| Hero images | [status] | [issues] |
| Product images | [status] | [issues] |
| Backgrounds | [status] | [issues] |

### Data Tables
| Table Location | Mobile Strategy | Issues |
|----------------|-----------------|--------|
| [path] | [Responsive/Scroll/None] | [issues] |

### Touch Targets
- **Button Sizes:** [Analysis of touch target sizes]
- **Link Spacing:** [Analysis of link density]
- **Form Controls:** [Analysis of input/select sizes]

## Accessibility

- **ARIA Labels:** [✅ Present | ❌ Missing | ⚠️ Incomplete]
- **Keyboard Navigation:** [✅ Works | ❌ Broken | ⚠️ Partial]
- **Focus Indicators:** [✅ Visible | ❌ Missing | ⚠️ Inconsistent]
- **Color Contrast:** [✅ WCAG AA+ | ⚠️ Some issues | ❌ Fails]

## Browser/Device Testing Setup

- **Testing Tools:** [List any mobile testing tools found in package.json]
- **Responsive Testing:** [Describe current testing approach]
- **Device Preview:** [Tools available]

## Key Findings

### Strengths
1. [What's already mobile-friendly]
2. [Existing optimizations]
3. [Good patterns to maintain]

### Critical Gaps
1. [Most important missing features]
2. [Major mobile UX issues]
3. [Performance blockers]

### Quick Wins
1. [Easy improvements with high impact]
2. [Low-hanging fruit]

## Recommended Implementation Priority

Based on this assessment, prioritize improvements in this order:

1. **High Priority - Core Functionality**
   - [List critical mobile features needed]

2. **Medium Priority - UX Enhancement**
   - [List UX improvements]

3. **Low Priority - Polish**
   - [List nice-to-have features]

## Next Steps

The following tactics will be used to find specific mobile polish opportunities:

1. **Responsive Navigation** - Implement hamburger menu
2. **Viewport & Meta Tags** - Ensure proper configuration
3. **Touch Targets** - Verify 44×44px minimum sizes
4. **Image Optimization** - Add lazy loading and responsive images
5. **Form Optimization** - Mobile-friendly inputs
6. **Performance** - Optimize for mobile networks
```

## Guidelines

- **Be thorough**: Check all major areas of mobile support
- **Be specific**: Include file paths and line numbers
- **Identify patterns**: Note if certain patterns are used consistently
- **Note framework features**: Leverage Next.js Image, Tailwind responsive classes, etc.
- **Prioritize**: Focus on user-facing issues first
