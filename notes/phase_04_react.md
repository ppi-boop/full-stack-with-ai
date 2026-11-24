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

# Topic 3: Rendering, Re-rendering Triggers, Component Purity & Strict Mode

### 1. Simple Definitions
* **Render:** React calling your component function to get the new UI description. Does NOT mean the real DOM changed.
* **Pure component:** Same props + state always give the same JSX, and rendering changes nothing outside itself (like a math function).
* **Side effect:** Anything that reaches outside the function: fetch, timers, DOM writes, editing outer variables.
* **Strict Mode:** Dev-only wrapper that renders components twice (and re-runs effects once extra) to expose impure code. Does nothing in production.

### 2. The Essentials
**Only 3 things trigger a re-render:**
1. The component's own state changes.
2. Its parent re-renders (children re-render by default, even with identical props).
3. A context it reads changes.

**Purity rules:**
1. Don't change anything outside the component during render (no outer variables, no mutating props/state).
2. No side effects in the render body. Put them in event handlers or `useEffect` (Topic 4).
3. Don't use `Math.random()` / `Date.now()` in render output or keys.
4. Mutating local variables created inside the render is fine.

### 3. Code Example
```jsx
// IMPURE: mutates an outer variable (breaks in Strict Mode: #2, #4, #6)
let guestCount = 0;
function Guest() { guestCount++; return <p>Guest #{guestCount}</p>; }

// PURE
function Guest({ number }) { return <p>Guest #{number}</p>; }

// Side effect in a handler, not in render
function Save({ doc }) {
  function handleClick() { fetch("/save", { method: "POST", body: JSON.stringify(doc) }); }
  return <button onClick={handleClick}>Save</button>;
}
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `fetch` / `setInterval` in the component body | Runs every render; fetch + `setState` makes an infinite loop |
| Editing an outer variable during render | Output depends on how many times React renders |
| Mutating `props` | Props are read-only; corrupts the parent's data |
| Component defined inside another component | New type each render, so remount and state reset |
| "My `console.log` ran twice" | Strict Mode (dev only) |
| "Props didn't change, so child won't re-render" | Wrong. Parent re-render re-renders the child (stop with `React.memo`, Topic 6) |

### 5. Practice Checks (passed)
* Button click in `Parent` re-renders `Child` once (trigger: parent re-render).
* `fetch(...).then(setUser)` in the render body loops forever: `setUser` changes state, which re-renders, which runs the fetch again. Fix: `useEffect` or an event handler.

### 6. Optional / Later (not needed now)
* The render phase may be paused or restarted by React, which is another reason it must be pure.
* Strict Mode also checks that refs and effects clean up properly.
* React Compiler (Topic 6) relies on components being pure to auto-memoize safely.

---

# Topic 4: Side Effects & Lifecycle (`useEffect`)

### 1. Simple Definitions
* **`useEffect`:** Runs your code AFTER React has put the UI on screen. Home for side effects: fetch, subscriptions, timers, manual DOM work.
* **Dependency array:** Values the effect uses. React re-runs the effect only when one changed.
* **Cleanup function:** What you `return` from the effect. Runs before the next effect run and on unmount. Undoes what the effect set up.
* **Race condition:** Two async requests in flight; the older one finishes last and overwrites the newer result.

### 2. The Essentials
1. **Three forms:** no array = every render (rare); `[]` = once after mount; `[id]` = after mount and whenever `id` changes.
2. **An effect sees the snapshot of the render that created it** (Topic 2). Put every prop/state it reads in the deps. Anything long-lived (interval, listener, request) keeps the values from the render that made it.
3. **Cleanup anything that must be undone:** `clearInterval`, `removeEventListener`, `socket.close()`, `controller.abort()`.
4. **Strict Mode (dev):** mount, cleanup, mount again. If the second run breaks, your cleanup is missing.
5. **Fetch race fix:** `AbortController` in the effect + `return () => controller.abort()`. Ignore `AbortError` in `catch`.
6. **You might not need an effect:** derived data (compute in render), responding to a user action (event handler), resetting state on prop change (`key`), production data fetching (TanStack Query / Next.js server components in Phase 5).

### 3. Code Example
```jsx
function Profile({ id }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/users/${id}`, { signal: controller.signal })
      .then(r => r.json())
      .then(setUser)
      .catch(err => { if (err.name !== "AbortError") console.error(err); });
    return () => controller.abort();
  }, [id]);

  return <p>{user?.name}</p>;
}

// Interval: updater avoids needing `seconds` in deps; cleanup stops it
useEffect(() => {
  const id = setInterval(() => setSeconds(s => s + 1), 1000);
  return () => clearInterval(id);
}, []);
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Missing dependency (`[]` but reads `count`) | Stale closure: interval/listener keeps seeing the first render's value |
| Object/array literal in deps | New reference every render, so effect runs every render |
| `setState` in an effect with no deps | Re-render, effect again, infinite loop |
| No cleanup on interval/listener | Leaks and duplicates (Strict Mode exposes it) |
| `useEffect(async () => ...)` | Effect must return cleanup or nothing, not a Promise. Define an async function inside and call it |
| Effect to compute derived state | Extra render with briefly wrong data. Compute in render |
| Silencing `exhaustive-deps` lint | The warning is almost always right |

### 5. Practice Checks (passed)
* Search-box race: the older "re" request finishes last, so the user sees the "re" results. Cleanup runs before the next effect and aborts the old request.
* Demo (stale closure): `useEffect(..., [])` with an interval reading `count` logs 0 forever; with `[count]` it logs 1, 2, 3 because cleanup clears the old interval and a new one sees the new render.
* Reading stale state in a long-lived callback: fix with `[count]` in deps (or a ref, Topic 5). `c => c + 1` fixes *writing* state, not *reading* it.

### 6. Optional / Later (not needed now)
* `useLayoutEffect` runs before paint (measuring DOM). Rarely needed.
* `useEffectEvent` reads the latest values without making them dependencies.
* Effects don't run on the server (matters for Next.js, Phase 5).

---

# Topic 5: `useRef` — Escape Hatches, DOM Access & Storing Mutable Values

### 1. Simple Definitions
* **Ref:** A box `{ current: ... }` React keeps between renders. Changing `ref.current` does NOT re-render.
* **State vs ref:** State shows on screen and re-renders when changed. A ref holds values that don't appear on screen, and changing it is silent.
* **Escape hatch:** A way outside React's "describe the UI" model (focus an input, play a video). Use sparingly.

### 2. The Essentials
1. A ref is the same box every render and is never a snapshot (always holds the latest value).
2. **Use 1: DOM access.** `<input ref={inputRef} />`, then `inputRef.current.focus()`. Use for focus, scroll, measure, media. Prefer it over `document.querySelector`.
3. **Use 2: non-display values.** Timer IDs, previous values, sockets, "first render" flags.
4. Don't read or write `ref.current` during render (breaks purity). Use event handlers and effects.
5. `ref.current` is `null` until the component mounts.
6. **Stale-closure fix:** keep a ref in sync with state, and have the long-lived callback read the ref.

### 3. Code Example
```jsx
function Counter() {
  const [count, setCount] = useState(0);
  const latest = useRef(count);                          // 1. create the box

  useEffect(() => { latest.current = count; }, [count]); // 2. keep it fresh

  useEffect(() => {
    const id = setInterval(() => console.log(latest.current), 1000); // 3. READ the ref
    return () => clearInterval(id);
  }, []);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```
Compare: `[count]` in deps restarts the interval on each change; the ref version keeps one interval and still reads the live value.

### 4. State or Ref?
| Situation | Use |
|---|---|
| Shown on screen / must update the UI | State |
| Timer ID, socket, previous value | Ref |
| Latest value inside a long-lived callback | Ref |
| Focus, scroll, measure a DOM node | Ref |

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Displayed data stored in a ref | No re-render, so the UI stays stale |
| Reading `ref.current` in the render body | Unpredictable output, breaks purity |
| `inputRef.current.focus()` on first render | `current` is `null` |
| `document.querySelector` inside React | Bypasses React |
| Ref used to dodge a real deps bug | Hides the stale-data problem |

### 6. Practice Checks (passed)
* Search text shown on screen = state. `setTimeout` ID = ref. Previous page number used only in an effect = ref.
* Stale interval fix: create the ref, sync it in an effect on `[count]`, and READ `latest.current` in the interval (reading `count` there stays stale).

### 7. Optional / Later (not needed now)
* `forwardRef` / React 19 `ref` as a prop; callback refs (`ref={el => ...}`); `useImperativeHandle`.

---
