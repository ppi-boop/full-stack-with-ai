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

# Topic 2: Props, State, "State as a Snapshot" & Batching

### 1. Simple Definitions
* **Props:** Read-only arguments a parent passes to a child. To "change" a prop, the parent changes its own state.
* **State:** Memory a component keeps between renders (a plain `let` is reset every render).
* **Snapshot:** Each render is a photo. Inside one render, `count` is a fixed value, even after you call `setCount`.
* **Batching:** All `setState` calls in one event produce one re-render (React 18+ batches everywhere).
* **Updater function:** `setCount(c => c + 1)`. Gets the latest queued value, not the snapshot.

### 2. The Essentials (6 rules)
1. `setCount(count + 1)` three times = +1, not +3. Use `setCount(c => c + 1)` when the new value depends on the old one.
2. `console.log(count)` right after `setCount` shows the OLD value (the snapshot is frozen).
3. **Never mutate state.** Same reference means React skips the update. Replace objects/arrays with new ones.
4. `useState(props.x)` reads the value **only on the first render**. Reset with `key`: `<Editor key={doc.id} />`.
5. Hooks must run in the same order, at the top level (never inside `if` or loops).
6. Derive values during render (e.g. `fullName`); don't store them. Prefer one `status` (`'idle' | 'loading' | 'error' | 'success'`) over several booleans.

### 3. Code Example
```jsx
function Counter() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);   // snapshot: 0 + 1
    setCount(count + 1);   // snapshot: 0 + 1  -> result is 1
  }
  function handleClickRight() {
    setCount(c => c + 1);
    setCount(c => c + 1);  // result is 2
  }
}
```
Immutable updates:
```jsx
setUser(u => ({ ...u, age: u.age + 1 }));                              // object
setItems(items => [...items, newItem]);                                // add
setItems(items => items.filter(i => i.id !== id));                     // remove
setItems(items => items.map(i => i.id === id ? { ...i, done: true } : i)); // update one
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `setCount(count + 1)` ×3 | Same snapshot each time, so +1 total |
| `user.age = 21; setUser(user)` | Same reference, React bails out, UI stale |
| `todos.push(x); setTodos(todos)` | Mutation plus same reference |
| `useState(props.name)` expecting live sync | Initial value only |
| Hook inside `if` | Breaks call-order matching |
| `setTimeout(() => alert(n))` | Alert shows the `n` from the render where you clicked |

### 5. Practice Checks (passed)
* Queue: `setCount(count+1); setCount(c=>c*10); setCount(count+3); setCount(c=>c+1)` from 0 gives **4** (a plain value replaces everything before it; only `c =>` sees the queued value).
* `user.age = 21; setUser(user)` doesn't update (same reference). `setUser({...user, age: 21})` does (new reference).

### 6. Optional / Later (not needed now)
* React stores hooks as a list of slots on the Fiber node, matched by call order. That's why order must not change.
* Queue processing: a plain value replaces the result; an updater transforms the previous result.
* Equal value check uses `Object.is`; React may render the component once more but skips children and effects.
* `useState(() => expensive())` (lazy init) runs once; `useState(expensive())` runs every render.
* `flushSync` forces a synchronous flush (rare). React 17 batched only inside React event handlers.

---
