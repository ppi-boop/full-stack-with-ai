# Phase 03 — HTML, CSS & Browser Fundamentals Master Handbook

> **Comprehensive Revision Guide:** Phase 3 — covers the Box Model, layout systems (Flexbox, Grid), positioning, typography, responsive design, animations, and browser rendering.

---

## Quick Navigation
* [Topic 1: Box Model, Display & Document Flow](#topic-1-box-model-display--document-flow)
* [Topic 2: Flexbox — One-Dimensional Layout](#topic-2-flexbox--one-dimensional-layout)
* [Topic 3: CSS Grid — Two-Dimensional Layout](#topic-3-css-grid--two-dimensional-layout)
* [Topic 4: Positioning — static, relative, absolute, fixed, sticky](#topic-4-positioning)
* [Topic 5: Typography, Colors, Custom Properties (CSS Variables)](#topic-5-typography-colors-css-variables)
* [Topic 6: Responsive Design — Media Queries, Viewport, rem/em/clamp](#topic-6-responsive-design)
* [Topic 7: Responsive Navigation, Tables, Forms & Dashboards](#topic-7-responsive-navigation-tables-forms-dashboards) ← **Last Completed**

---

# Topic 1: Box Model, Display & Document Flow

### Key Rules
- Every element is a rectangular box: **content → padding → border → margin**
- `box-sizing: border-box` — padding and border are INCLUDED in the width. Use this always. `content-box` (default) is a trap.
- `display: block` — takes full width, stacks vertically. `display: inline` — flows with text, ignores width/height. `display: inline-block` — flows with text but respects width/height.
- `margin: auto` on a block element with a fixed width = horizontal centering.
- Margin collapse: vertical margins between adjacent block elements collapse to the larger of the two — does NOT happen with Flexbox or Grid children.

### Critical Code
```css
*, *::before, *::after {
  box-sizing: border-box; /* Always set this globally */
}

.container {
  width: 800px;
  margin: 0 auto; /* Centers horizontally */
  padding: 24px;
}
```

---

# Topic 2: Flexbox — One-Dimensional Layout

### Key Rules
- Flexbox is for **one axis at a time**: either row or column.
- **Container properties** (on the parent): `display: flex`, `flex-direction`, `justify-content` (main axis), `align-items` (cross axis), `flex-wrap`, `gap`.
- **Item properties** (on the children): `flex-grow`, `flex-shrink`, `flex-basis`, shorthand `flex`, `align-self`, `order`.
- `flex: 1` = `flex-grow: 1; flex-shrink: 1; flex-basis: 0%` — item grows to fill available space.
- `justify-content: space-between` — first item at start, last item at end, equal gaps between.

### Critical Code
```css
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.sidebar { flex: 0 0 240px; } /* Fixed width, no grow/shrink */
.main    { flex: 1; }         /* Fills remaining space */
```

---

# Topic 3: CSS Grid — Two-Dimensional Layout

### Key Rules
- Grid is for **two axes simultaneously**: rows AND columns.
- `grid-template-columns: repeat(3, 1fr)` — 3 equal columns. `fr` = fractional unit of remaining space.
- `grid-column: 1 / 3` — span from column line 1 to 3 (spans 2 columns).
- `gap` works on both row and column gaps.
- `grid-template-areas` — named layout regions, reads like ASCII art.
- Use Grid for page layout, Flexbox for component-level alignment.

### Critical Code
```css
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  min-height: 100vh;
  gap: 16px;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

---

# Topic 4: Positioning

### Key Rules
| Value | Behavior |
|---|---|
| `static` | Default. In normal flow. `top/left` ignored. |
| `relative` | In flow, but `top/left` offsets FROM its natural position. Creates positioning context for children. |
| `absolute` | OUT of flow. Positioned relative to nearest `position: relative/absolute/fixed` ancestor. |
| `fixed` | OUT of flow. Positioned relative to the viewport. Stays on screen when scrolling. |
| `sticky` | In flow until threshold, then behaves like `fixed` within its scroll container. |

- `z-index` only works on positioned elements (not static).
- An `absolute` child with no positioned ancestor defaults to the `<html>` element.

### Critical Code
```css
.parent   { position: relative; }
.tooltip  { position: absolute; top: 100%; left: 0; } /* just below parent */
.header   { position: sticky; top: 0; z-index: 100; } /* sticks to top */
.overlay  { position: fixed; inset: 0; } /* inset: 0 = top/right/bottom/left: 0 */
```

---

# Topic 5: Typography, Colors & CSS Variables

### Key Rules
- **CSS Variables (`--name`):** Defined on `:root` (global) or any element (scoped). Accessed with `var(--name)`. Zero runtime overhead — native CSS, not a preprocessor.
- **`em`** = relative to the element's own font-size. **`rem`** = relative to the root (`html`) font-size. Use `rem` for consistent sizing across the document.
- Color formats: `hsl(hue, saturation%, lightness%)` is the most maintainable — easy to derive shades by changing lightness only.
- `font-display: swap` in `@font-face` — shows fallback font immediately, swaps when custom font loads (prevents invisible text).

### Critical Code
```css
:root {
  --color-primary: hsl(220, 90%, 56%);
  --color-primary-dark: hsl(220, 90%, 40%);
  --color-text: hsl(0, 0%, 10%);
  --color-bg: hsl(0, 0%, 98%);
  --font-base: 1rem;        /* 16px */
  --font-lg: 1.25rem;       /* 20px */
  --radius: 8px;
  --shadow: 0 2px 8px hsl(0 0% 0% / 0.1);
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: var(--font-base);
  color: var(--color-text);
  background: var(--color-bg);
}
```

---

# Topic 6: Responsive Design — Media Queries, Viewport, rem/em/clamp

### Key Rules
- **Mobile-first:** Start with styles for small screens, use `min-width` media queries to add complexity for larger screens. NOT max-width.
- **Common breakpoints:** 640px (sm), 768px (md), 1024px (lg), 1280px (xl).
- **`clamp(min, preferred, max)`** — fluid sizing without media queries: `font-size: clamp(1rem, 2.5vw, 1.5rem)`.
- **Viewport units:** `vw` (1% of viewport width), `vh` (1% of viewport height). Careful with `100vh` on mobile — use `100dvh` (dynamic viewport height) instead.
- **`meta viewport` tag is mandatory:** `<meta name="viewport" content="width=device-width, initial-scale=1">` — without this, mobile browsers zoom out to desktop width.

### Critical Code
```css
/* Mobile first */
.grid { display: grid; grid-template-columns: 1fr; gap: 16px; }

@media (min-width: 768px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .grid { grid-template-columns: repeat(3, 1fr); }
}

/* Fluid font — no media queries needed */
h1 { font-size: clamp(1.75rem, 4vw, 3rem); }
```

---

# Topic 7: Responsive Navigation, Tables, Forms & Dashboards

### Navigation Patterns
```css
/* Desktop: horizontal nav */
.nav { display: flex; align-items: center; gap: 24px; }

/* Mobile: hamburger — hide links, show toggle */
@media (max-width: 767px) {
  .nav-links { display: none; }
  .nav-links.open { display: flex; flex-direction: column; }
  .hamburger { display: block; }
}
```

### Responsive Tables
```css
/* Horizontal scroll for tables that can't reflow */
.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch; /* smooth scroll on iOS */
}

/* OR: card layout on mobile */
@media (max-width: 640px) {
  table, thead, tbody, tr, th, td { display: block; }
  td::before {
    content: attr(data-label); /* shows column name on each cell */
    font-weight: bold;
  }
  thead { display: none; }
}
```

### Forms Best Practices
```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input, select, textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  font-size: 1rem; /* prevents iOS zoom (must be >= 16px) */
  outline: none;
}

input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px hsl(220 90% 56% / 0.2); /* focus ring */
}
```

### Dashboard Layout Pattern
```css
.dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 60px 1fr;
  height: 100vh;
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-rows: 60px auto 1fr;
  }
}
```

---

# Topic 8: CSS Animations, Transitions & Transforms

### Key Rules
- **Transition** = smooth change between two states triggered by a state change (hover, class toggle). Needs a trigger.
- **Animation** = plays automatically using `@keyframes`. Full control — loops, direction, delay, fill-mode.
- **Transform** = visual-only movement. Does NOT affect document flow. Other elements don't react to it.
- **Performance rule:** Only animate `transform` and `opacity` — they are GPU-accelerated and never cause reflow. Never animate `width`, `height`, `top`, `left`, `margin` — they trigger reflow on every frame = jank.

### Transition
```css
.button {
  background: hsl(220, 90%, 56%);
  transition: background 200ms ease, transform 150ms ease;
  /* property | duration | timing-function */
}
.button:hover {
  background: hsl(220, 90%, 40%);
  transform: scale(1.05);
}
```

Timing functions: `ease` (default), `ease-in`, `ease-out`, `ease-in-out`, `linear`, `cubic-bezier()`

### Transform — never use top/left to move things
```css
/* Chain multiple transforms on ONE property — second one overrides if split */
.card:hover {
  transform: translateY(-4px) scale(1.02); /* correct */
}

/* Move with transform, NOT with left/top */
.box { transition: transform 300ms; }
.box:hover { transform: translateX(20px); } /* GPU-accelerated, smooth */
```

### @keyframes Animation
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.card {
  animation: fadeInUp 400ms ease-out forwards;
  /* name | duration | timing | fill-mode */
}
```

`animation-fill-mode: forwards` — element keeps the final keyframe state after animation ends. Without it, element snaps back to its original state (broken-looking).


### Accessibility
```css
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
```

---

# Topic 9: Browser Rendering Pipeline

### The Pipeline
HTML to DOM to CSSOM to Render Tree to Layout (Reflow) to Paint to Composite

### Reflow vs Repaint vs Composite
- Reflow = geometry changes (width, height, margin, top, display). Most expensive.
- Repaint = visual changes only (color, background). No layout change.
- Composite only = transform and opacity. GPU-accelerated. Free. Always prefer for animation.

### Layout Thrashing — batch reads before writes
```javascript
// Bad: forces reflow every iteration
boxes.forEach(b => { const w = b.offsetWidth; b.style.width = w*2+"px"; });

// Good: all reads first, all writes after
const widths = Array.from(boxes).map(b => b.offsetWidth);
boxes.forEach((b, i) => { b.style.width = widths[i]*2+"px"; });
```

### Script and CSS blocking
- script in head without defer/async blocks HTML parsing
- defer: after HTML parsed, in order. Use for app scripts.
- async: as soon as downloaded, any order. Use for 3rd-party scripts.
- CSS is render-blocking — browser will not paint until all CSS is downloaded.

---

# Topic 10: Semantic HTML and Accessibility

### Semantic elements
header, nav, main, article, section, aside, footer, figure, figcaption.
Use button for actions, a href for navigation. Never a div with an onClick.

### ARIA — only when native HTML is insufficient
- aria-label: accessible name for elements without visible text
- aria-expanded: state of collapsible elements
- aria-live="polite": announces dynamic content to screen readers
- aria-hidden="true": hides decorative elements from screen readers
- Meaningful alt on all images. Empty alt="" on decorative ones.

### Focus — never remove outline, replace it
```css
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

# Topic 11: Web Performance

### Core Web Vitals
- LCP (Largest Contentful Paint) < 2.5s: preload hero image, fetchpriority="high"
- CLS (Cumulative Layout Shift) < 0.1: always set width and height on images
- INP (Interaction to Next Paint) < 200ms: avoid long JS tasks on main thread

### Key techniques
```html
<link rel="preload" as="image" href="/hero.webp">
<img src="/hero.webp" fetchpriority="high" width="1200" height="600" alt="Hero">
<img src="/card.jpg" width="400" height="300" alt="Card">
<img src="/photo.jpg" loading="lazy" width="800" height="600" alt="Photo">
<script src="app.js" defer></script>
<script src="analytics.js" async></script>
```

---

# Topic 12: Browser Storage

| Storage | Capacity | Persists | Sent to server |
|---|---|---|---|
| localStorage | 5MB | Until cleared | No |
| sessionStorage | 5MB | Until tab closes | No |
| Cookie | 4KB | Set expiry | Yes every request |
| IndexedDB | Hundreds MB | Until cleared | No |

### localStorage — strings only, synchronous
```javascript
localStorage.setItem("theme", "dark");
localStorage.setItem("user", JSON.stringify({ id: 1 }));
const theme = localStorage.getItem("theme");
const user  = JSON.parse(localStorage.getItem("user") ?? "null");

// SSR guard — window does not exist on server
if (typeof window !== "undefined") {
  localStorage.setItem("key", "value");
}
```

### Cookies — auth must be server-set
- HttpOnly: JS cannot read the cookie. Prevents XSS token theft.
- Secure: sent over HTTPS only.
- SameSite=Strict or Lax: prevents CSRF attacks.
- Auth tokens must be HttpOnly cookies set by server. Never store in localStorage.

---
