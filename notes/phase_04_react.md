# Phase 04 — React Core & Reconciliation Master Handbook

> **Comprehensive Revision Guide:** Phase 4 — covers React mental model (JSX, Virtual DOM, Fiber, Reconciliation), Component Lifecycle, State & Props, Snapshot mechanics, Hooks deep dive (`useState`, `useEffect`, `useRef`, `useMemo`, `useCallback`, `useTransition`), Custom Hooks, Forms & Performance.

---

# Topic 1: React Mental Model — JSX, Virtual DOM & Reconciliation

### 1. Simple Definitions (Easy Language)
* **JSX:** Syntactic sugar looking like HTML, compiled at build time into pure `React.createElement()` or `_jsx()` calls.
* **Virtual DOM (VDOM):** In-memory JavaScript object tree describing what the UI should look like.
* **Reconciliation:** The diffing algorithm (React Fiber) comparing the newly returned VDOM tree with the previous VDOM tree to calculate minimal mutations.
* **Re-render:** React calling your component function again to compute a new VDOM snapshot. **Does NOT automatically mean the real DOM was modified.**
* **Commit Phase:** The synchronous phase where React applies calculated mutations to the actual browser DOM.

---

### 2. Under the Hood Mechanics

#### A. JSX Compilation
```jsx
// Source JSX
function Card({ title, onClick }) {
  return (
    <div className="card" onClick={onClick}>
      <h2>{title}</h2>
      <img src="/photo.jpg" alt="Photo" />
    </div>
  );
}

// Compiled Output (Pure JavaScript)
function Card({ title, onClick }) {
  return React.createElement(
    "div",
    { className: "card", onClick: onClick },
    React.createElement("h2", null, title),
    React.createElement("img", { src: "/photo.jpg", alt: "Photo" })
  );
}
```

Key Differences from Raw HTML:
1. `class` → `className`, `for` → `htmlFor` (reserved JS keywords).
2. Event handlers are camelCase function references (`onClick={fn}`), not strings (`onclick="fn()"`).
3. Self-closing tags must be explicitly closed (`<img />`, `<input />`).
4. Exactly one single root element must be returned (or wrap in a Fragment `<></>`).

#### B. The VDOM Object Anatomy
`React.createElement()` returns a lightweight frozen JS object:
```javascript
{
  $$typeof: Symbol.for('react.element'),
  type: 'div',
  key: null,
  props: {
    className: 'card',
    onClick: [Function],
    children: [
      { type: 'h2', props: { children: 'Card Title' } },
      { type: 'img', props: { src: '/photo.jpg', alt: 'Photo' } }
    ]
  }
}
```

#### C. Reconciliation & Diffing Rules
1. **Elements of Different Types:** If root elements have different types (e.g. `<div>` replaced by `<span>`, or `<Header>` replaced by `<Nav>`), React tears down the old tree completely (destroying state and unmounting children) and builds the new tree from scratch.
2. **Elements of Same Type:** React retains the DOM node and updates only the changed attributes/props (e.g., `className`, `style`, or `textContent`).
3. **List Reconciliation & Keys:** Keys provide identity across renders. Without stable unique keys, React relies on array index order, leading to incorrect state mapping, input field cross-contamination, and expensive DOM reparenting.

#### D. The Two-Phase Pipeline: Render vs Commit
```text
State Change Trigger
        ↓
[1. RENDER PHASE (Concurrent / Interruptible)]
- React invokes your component function.
- Produces fresh VDOM element tree.
- Diffs new VDOM tree with previous VDOM tree.
- Calculates minimal DOM patch list.
        ↓
[2. COMMIT PHASE (Synchronous / Uninterruptible)]
- React mutates real browser DOM nodes (inserts, deletes, updates attributes).
- Updates DOM refs.
- Synchronously runs useLayoutEffect.
- Asynchronously schedules useEffect.
```

---
