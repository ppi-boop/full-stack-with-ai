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

# Topic 6: Memoization & Performance (`useMemo`, `useCallback`, `React.memo`, Compiler)

### 1. Simple Definitions
* **Memoization:** Remember a result and reuse it when the inputs haven't changed.
* **`React.memo`:** Skips re-rendering a component when all its props are the same (shallow `Object.is` per prop).
* **`useMemo`:** Remembers a computed value (or stabilizes an object/array reference).
* **`useCallback`:** Remembers a function so it keeps the same reference until deps change.

### 2. The Essentials
1. Re-rendering is normal and usually fast. Memoize only after **measuring** a slow spot (React DevTools Profiler).
2. `React.memo` only helps if props keep the **same reference**.
3. **The trap:** inline objects, arrays and functions (`{}`, `[]`, `() => {}`, `.filter(...)`) are new every render, so memo never skips.
4. `useCallback` helps only when the function goes to a `memo`'d child or is an effect dependency.
5. `useMemo` for expensive computations or to stabilize a reference.
6. Deps rules = `useEffect` rules. Missing deps cause a **stale closure** (`useCallback(() => log(count), [])` always uses the first `count`).
7. **Don't memoize:** cheap work, rarely re-rendered components, props that change every time anyway, or anything unmeasured.
8. **Fix structure first:** move state down into a small component, or pass `children`.
9. **React Compiler:** build-time auto-memoization; needs pure components (Topic 3). Check the official docs for the status on your React version.

### 3. Code Example
```jsx
const HeavyList = React.memo(function HeavyList({ rows, onSelect }) { /* ... */ });

function Page({ users }) {
  const rows = useMemo(() => users.filter(u => u.active), [users]);   // stable array
  const onSelect = useCallback(id => console.log(id), []);            // stable function
  return <HeavyList rows={rows} onSelect={onSelect} />;
}

// BETTER: move state down so Page never re-renders on keystrokes
function SearchBox() {
  const [text, setText] = useState("");
  return <input value={text} onChange={e => setText(e.target.value)} />;
}
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `React.memo` + inline `{}` / `() => {}` prop | New reference each render, memo never skips |
| `useCallback` with no memo'd child / effect dep | Adds cost, no benefit |
| Missing deps in `useCallback` / `useMemo` | Stale closure |
| Memoizing everything "just in case" | More code, more bugs, often slower |
| Memoizing before measuring | May fix something that isn't slow |
| Mutating a memoized value | Same reference, so the cached result is wrong |

### 5. Practice Checks
* **Passed:** `useCallback(() => console.log(count), [])` prints `0, 0, 0` over three clicks (stale snapshot from the first render). Fix: `[count]`, or drop `useCallback` if nothing needs a stable reference.
* **Explained, revisit in the project:** `memo`'d list still re-renders because `users.filter(...)` and `id => ...` are new references each render. Fix: `useMemo` / `useCallback`, or move the input state into its own component.

### 6. Optional / Later (not needed now)
* `memo` with a custom comparison function (rarely a good idea).
* `useMemo` is a hint, not a guarantee; React may drop the cache.
* List virtualization (`react-window`) beats memoizing for thousands of rows.

---

# Topic 7: Context API & Prop Drilling vs State Management

### 1. Simple Definitions
* **Prop drilling:** Passing a prop through components that don't use it, just to reach a deep child.
* **Context:** Shares a value with a whole subtree without passing props by hand (a notice board any descendant can read).
* **Provider / Consumer:** The Provider puts a value on the board; any component reading it with `useContext` is a consumer.

### 2. The Essentials
1. Three parts: `createContext(default)`, `<Ctx.Provider value={...}>`, `useContext(Ctx)`. React 19: `<Ctx value={...}>` and `use(Ctx)`.
2. **A changed context `value` re-renders EVERY consumer** (re-render trigger #3), even if it only reads part of the value.
3. **Reference trap:** `value={{ user, setUser }}` is a new object each render, so all consumers re-render. Fix: `useMemo(() => ({ user, setUser }), [user])` (`setUser` is stable).
4. Use context for **low-frequency, app-wide** values: theme, auth user, locale. NOT for fast-changing data (input text, mouse position).
5. Wrap in a custom hook that throws if the Provider is missing (`useAuth()`), instead of silently getting the default.
6. **Composition first:** if only one deep child needs data, create it high up and pass it as a prop/`children`. No context needed.
7. Context only *delivers* a value; the state still lives in `useState`/`useReducer` above.

### 3. Code Example
```jsx
const AuthContext = createContext(null);

function AuthProvider({ children }) {            // children keeps its reference
  const [user, setUser] = useState(null);
  const value = useMemo(() => ({ user, setUser }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

function useAuth() {
  const ctx = useContext(AuthContext);
  if (ctx === null) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
```

### 4. Decision Guide
| Situation | Use |
|---|---|
| Drilling 1-2 levels | Just pass props |
| Intermediate components don't need the data | Composition (`children`) |
| Rarely-changing value needed all over (theme, auth) | Context |
| Complex client state with many actions | Zustand / Redux Toolkit |
| Server data (lists, cache, refetch) | TanStack Query, NOT context |

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Inline `value={{ a, b }}` | New object each render, every consumer re-renders |
| Fast-changing data in context | Re-renders all consumers on every change |
| One giant context | Any change re-renders every consumer; split it |
| Context for server data | Rebuilds caching/refetch by hand |
| `useContext` outside Provider | Silently gets the default; throw in a custom hook |
| Context at the first sign of drilling | Composition or plain props is often simpler |

### 6. Practice Checks (passed)
* Drilling `user` to `UserBadge`: context or a store; composition (pass `<UserBadge user={user} />` down) is the simplest for a single deep consumer.
* Typing in an input beside a Provider with `value={{ theme, setTheme }}`: consumers re-render because `App` re-renders (trigger 2) AND the value is a new object (trigger 3). Best fix: move the input state into its own component (so `App` stops re-rendering). `useMemo` on the Provider's `value` (not on consumers) helps when the Provider is its own `{ children }` component. Memoizing `value` alone doesn't stop re-renders caused by the parent re-rendering.

### 7. Optional / Later (not needed now)
* `use(Context)` (React 19) can be called conditionally.
* Selector-based stores (Zustand) let components subscribe to only part of the state.
* `useReducer` + context is a built-in Redux-like pattern.

---

# Topic 8: Advanced Hooks & React 19 (`useTransition`, `useOptimistic`, `useActionState`, `use`)

> **Note:** These shine most with a framework (Next.js Server Actions, Phase 5). In a plain client app, TanStack Query covers most data work. Learn the idea and the use case now.

### 1. Simple Definitions
* **Transition:** Marks a state update as non-urgent so React can interrupt it and keep the UI responsive.
* **Action:** An async function used for a form or mutation.
* **Optimistic update:** Show the expected result immediately; revert if it fails.
* **Suspense:** Shows a fallback (spinner) while something inside is still waiting.

### 2. The Essentials
1. **`useTransition`:** `const [isPending, startTransition] = useTransition();` Typing stays urgent (`setText`), the heavy list update goes in `startTransition(() => setQuery(...))`. It keeps the UI responsive; it does NOT make code faster.
2. **`useDeferredValue(value)`:** a lagging copy of a value. Helps render cost, not network requests (not a debounce).
3. **`useActionState(action, initialState)`** returns `[state, formAction, isPending]`. Use with `<form action={formAction}>`; the action gets `(prevState, formData)`.
4. **`useOptimistic(state, updateFn)`:** temporary value while an action runs; reverts when the action ends. Must run inside an action or transition.
5. **`use(promise | context)`:** suspends until the promise resolves (needs `<Suspense>` above). Can be called conditionally. The promise must be stable (from a cache, library, parent, or Server Component).
6. **`useFormStatus()`** (`react-dom`): a button inside a form reads the form's pending state.

### 3. Code Example
```jsx
// useActionState
async function save(prev, formData) {
  const name = formData.get("name");
  if (!name) return { error: "Name is required" };
  await api.save(name);
  return { error: null };
}
function Form() {
  const [state, formAction, isPending] = useActionState(save, { error: null });
  return (
    <form action={formAction}>
      <input name="name" />
      <button disabled={isPending}>Save</button>
      {state.error && <p>{state.error}</p>}
    </form>
  );
}
```

### 4. Which Hook?
| Need | Use |
|---|---|
| Smooth typing while a heavy list re-renders | `useTransition` / `useDeferredValue` |
| Form with validation errors + pending | `useActionState` |
| Show result instantly, confirm later (likes, todos) | `useOptimistic` |
| Wait for a promise (usually from a framework) | `use` + `<Suspense>` |
| Submit button aware of pending form | `useFormStatus` |

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `use(fetch(...))` in a client component's render | New promise every render, so suspend, resolve, re-render, new promise: infinite loop (also a side effect in render) |
| Expecting `useTransition` to speed up slow code | It only keeps the UI responsive |
| Wrapping the controlled input's own `setState` in a transition | Input feels laggy; only the heavy part is non-urgent |
| `useOptimistic` outside an action/transition | No revert; React warns |
| `useDeferredValue` to debounce API calls | Defers rendering, not requests |
| No `<Suspense>` above `use(promise)` | Nothing to show while waiting |

### 6. Practice Checks
* **Passed:** typing + heavy list = `useTransition`; instant Like = `useOptimistic`; form errors + pending = `useActionState`.
* **Explained, revisit in Next.js:** `use(fetch().then(...))` in render loops because a new promise is created every render (purity + new reference). The promise must be created once and passed in.

### 7. Optional / Later (not needed now)
* Streaming Server Components with Suspense (Phase 5).
* `useId`, `useSyncExternalStore`, `useInsertionEffect` (mostly for library authors).
* After an `await` inside a transition, later state updates need their own `startTransition` (check the React 19 docs when needed).

---

# Topic 9: Custom Hooks & Logic Extraction

### 1. Simple Definitions
* **Custom hook:** A function whose name starts with `use` and that calls other hooks. Moves reusable logic out of components.
* **What is shared:** the logic (code), NOT the state. Each call gets its own independent state.
* **Logic extraction:** Move stateful code out so the component only describes the UI.

### 2. The Essentials
1. A custom hook is just a function that uses hooks (no special API).
2. Two components calling the same hook get two separate states. To share state, use context or a store (Topic 7).
3. Rules of hooks still apply: top level only, only in components/hooks, name starts with `use`.
4. **Extract when:** same stateful logic in 2+ places, or a component mixes too many concerns. Name it by WHAT, not HOW (`useOnlineStatus`).
5. **Don't extract:** one-time wrapper around one `useState`; logic with no hooks (use a plain function); abstractions that hide what's happening.
6. Return an array for 2 values (like `useState`); an object for more.
7. Real libraries (TanStack Query, `usehooks-ts`) provide production-grade versions; write your own to learn.

### 3. Code Example
```jsx
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = () => setOn(v => !v);
  return [on, toggle];
}

function useDebounce(value, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

function useFetch(url) {
  const [state, setState] = useState({ status: "loading", data: null, error: null });
  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading", data: null, error: null });
    fetch(url, { signal: controller.signal })
      .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
      .then(data => setState({ status: "success", data, error: null }))
      .catch(error => { if (error.name !== "AbortError") setState({ status: "error", data: null, error }); });
    return () => controller.abort();
  }, [url]);
  return state;
}

function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {            // lazy init: runs once
    try {
      const stored = localStorage.getItem(key);
      return stored !== null ? JSON.parse(stored) : initialValue;
    } catch { return initialValue; }
  });
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  return [value, setValue];
}
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Expecting components to share the hook's state | Each call has its own state; use context/store |
| Name without `use` | Linter can't enforce the rules of hooks |
| Hook inside `if` / loop | Breaks call order |
| Missing deps inside the hook | Same stale closure bugs |
| Returning a new object/function every render | Consumers with it in deps re-run effects every render |
| Extracting too early or too much | More indirection, harder to read |
| Hook for non-hook logic | A plain function is simpler |

### 5. Practice Checks
* **Passed:** two components each calling `useToggle()` have independent state (logic is shared, state is not).
* **Revisit in the mini project:** write `useLocalStorage` from memory. Common slips: use `initialValue` (the real parameter), lazy init that READS `localStorage`, an effect that WRITES it, `JSON.parse` / `JSON.stringify`, and return the real `setValue`.

### 6. Optional / Later (not needed now)
* `renderHook` from React Testing Library to test hooks (Topic 12).
* Hooks taking callbacks should keep the latest callback in a ref to avoid stale closures.
* `localStorage` doesn't exist on the server (guard in Next.js, Phase 5).

---

# Topic 10: Forms & Validation (Controlled vs Uncontrolled, React Hook Form / Zod)

### 1. Simple Definitions
* **Controlled input:** React state is the source of truth (`value` + `onChange`).
* **Uncontrolled input:** The DOM holds the value; read it via a `ref` or `FormData` on submit.
* **Schema (Zod):** One description of valid data, used for validation and TypeScript types.
* **React Hook Form (RHF):** Form library using mostly uncontrolled inputs (`register`), so typing causes few re-renders.

### 2. The Essentials
1. **Controlled** for live behaviour (counter, formatting, validate-as-you-type, dependent UI). **Uncontrolled** for simple submit-only forms (`defaultValue` + `FormData`).
2. `e.preventDefault()` on `onSubmit` (or use `<form action={fn}>` in React 19).
3. Gotchas: `value` without `onChange` = frozen input; start controlled state as `""` not `undefined`; checkbox uses `checked`; `type="number"` still gives a string.
4. **Validation layers:** HTML built-in (UX hints), client-side (Zod/RHF, good UX), **server-side (the real protection, never trust the client)**.
5. Show errors on blur or after first submit, not on the first keystroke.
6. Zod: `z.object({...})`, `z.infer<typeof schema>` for the type, `schema.safeParse(input)` returns `{ success, data | error }` without throwing.
7. RHF + Zod: `useForm({ resolver: zodResolver(schema) })`, `register("field")`, `handleSubmit(onSubmit)`, `formState: { errors, isSubmitting }`.
8. Accessibility: `<label htmlFor>`, `aria-invalid`, errors in `role="alert"`, disable the button while submitting.

### 3. Code Example
```tsx
const schema = z.object({
  email: z.string().email("Enter a valid email"),
  password: z.string().min(8, "At least 8 characters"),
});
type FormValues = z.infer<typeof schema>;

function SignupForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } =
    useForm<FormValues>({ resolver: zodResolver(schema) });

  return (
    <form onSubmit={handleSubmit(async v => { await api.signup(v); })} noValidate>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" {...register("email")} aria-invalid={!!errors.email} />
      {errors.email && <p role="alert">{errors.email.message}</p>}
      {/* password field the same way */}
      <button disabled={isSubmitting}>Sign up</button>
    </form>
  );
}
```

### 4. When to Use Which
| Situation | Choice |
|---|---|
| 1-2 simple fields | Plain controlled/uncontrolled inputs |
| Real form: validation, many fields, TypeScript | RHF + Zod |
| Next.js with Server Actions (Phase 5) | `<form action>` + `useActionState` + server-side Zod |

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `<input value={name} />` with no `onChange` | Frozen, read-only input |
| Forgetting `e.preventDefault()` | Page reloads on submit |
| `undefined` initial state for a controlled input | Uncontrolled to controlled warning |
| Client-only validation | Trivially bypassed (DOM edit, `curl`) |
| Errors on first keystroke | Annoying UX |
| No label / `aria-invalid` / `role="alert"` | Inaccessible |
| Allowing double submits | Disable the button while pending |

### 6. Practice Checks (passed)
* `<input value={name} />` is frozen because `value` forces state and nothing changes it. Fixes: add `onChange={e => setName(e.target.value)}` (controlled), or use `defaultValue` instead of `value` (uncontrolled).
* The server must validate again because anyone can edit the DOM or skip the browser (`curl`, Postman); frontend validation is only UX.

### 7. Optional / Later (not needed now)
* Zod's API changes between major versions (e.g. `z.email()` in newer versions); check the docs for your version.
* `useFieldArray` for dynamic fields; multi-step wizard forms.
* Mapping server errors onto fields ("email already taken").

---

# Topic 11: React Architecture, Component Composition & Patterns (skimmed, not practised)

> **Status:** Lower priority. Read the 3 essentials; practise them in the mini project. Folder structure will come naturally in Next.js (Phase 5).

### 1. The 3 Essentials
1. **Compose with `children` / slot props.** The component owns the layout; the caller supplies the content. Also avoids prop drilling.
   ```jsx
   <Card header={<h2>Orders</h2>} footer={<Pagination />}>
     <OrdersTable />
   </Card>
   ```
2. **Where state lives:** in the lowest component that needs it (colocation). If two siblings need it, lift it to their closest common parent (props down, callbacks up). Use context/store only if lifting means passing through many layers. Derive instead of duplicating state.
3. **Handle 4 states** (loading, error, **empty**, success) and use **error boundaries** (`react-error-boundary`) at meaningful boundaries (a page or widget). They catch **render** errors only, NOT errors in event handlers, async code (`fetch`) or on the server.

### 2. Quick Reference
* **Props API:** prefer `variant="primary"` / `size="lg"` over boolean explosions (`isPrimary isDanger isLarge`). Spread `...rest` onto the root element. Give sensible defaults.
* **Logic vs UI:** custom hook (logic) + dumb component (JSX) replaces the old container/presentational split.
* **Compound components:** `Tabs`, `Tabs.Tab`, `Tabs.Panel` share state via context (Topic 7).
* **Folders:** start by type (`components/`, `hooks/`); move to by feature (`features/orders/{components,hooks,api.ts,types.ts}`) as the app grows.
* **Rule of three:** abstract only after writing it three times.

### 3. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Component defined inside another component | New type every render, so remount and state reset |
| Boolean prop explosion | Contradictory states, messy API |
| Giant 500-line component | Hard to read and test |
| All state global | Needless re-renders and indirection |
| Derived data stored in state | Out-of-sync copies |
| Abstracting too early | Wrong abstraction costs more than duplication |
| Only one error boundary at the top | One bug blanks the whole app |
| Expecting error boundaries to catch `fetch` errors | They only catch render errors |
| Forgetting the empty state | Looks broken |

### 4. Practice Checks (not attempted; answers given)
* Card usage: `header` slot + `children` + optional `footer`; better than string props because callers can pass any JSX.
* `FilterBar` + `ProductList` siblings: put `category` in `ProductsPage`; pass `category` + `onCategoryChange` to `FilterBar` and `category` to `ProductList`. No context needed (one level).

### 5. Optional / Later (not needed now)
* Render props and HOCs (older patterns replaced by hooks).
* Polymorphic `as` components, headless UI libraries (Radix, shadcn/ui), Storybook.
* Barrel files (`index.ts` re-exports) can hurt tree-shaking.

---

# Topic 12: React Testing (React Testing Library + Vitest) — overview only

> **Status:** Overview only, not practised. Real testing practice comes in **Project 1 (Admin Dashboard)** and **Phase 14**.

### 1. What It's For
* Tests give you confidence to refactor and ship without breaking things. They appear in most job descriptions and in Project 1's requirements.
* **Vitest** = test runner (Jest-compatible, Vite-native). **React Testing Library (RTL)** = renders components and finds things like a user would. **jsdom** = fake browser in Node. **`@testing-library/user-event`** = simulates real typing/clicking. **`@testing-library/jest-dom`** = matchers like `toBeInTheDocument()`.

### 2. Key Ideas
1. **Test what the user sees, not implementation.** Click, type, then check the screen. Never assert on internal state.
2. **Arrange, Act, Assert.** `render(...)`, then `await user.click(...)`, then `expect(...)`. Always `await` user-event.
3. **Query priority:** `getByRole` (best, also checks accessibility) > `getByLabelText` > `getByText` > `getByTestId` (last resort). Proper labels/roles make code easier to test.
4. **Query families:** `getBy` throws if missing; `queryBy` returns `null` (use to assert something is NOT there); `findBy` waits (async content).
5. **Mock** network calls (`vi.spyOn(globalThis, "fetch")`, or MSW for realistic mocks). Reset mocks between tests.
6. **Custom hooks:** `renderHook` + `act`.
7. Don't test internals, library code, or use big snapshots. Coverage % is only a rough signal.

### 3. Code Example
```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";

describe("Counter", () => {
  it("increments when the button is clicked", async () => {
    const user = userEvent.setup();
    render(<Counter />);                                             // Arrange
    await user.click(screen.getByRole("button", { name: "Add" }));   // Act
    expect(screen.getByText("Count: 1")).toBeInTheDocument();        // Assert
  });
});
```
Setup (Vite): `npm i -D vitest jsdom @testing-library/react @testing-library/user-event @testing-library/jest-dom`; in `vite.config.ts` set `test: { environment: "jsdom", globals: true, setupFiles: "./src/setupTests.ts" }`; in `setupTests.ts` add `import "@testing-library/jest-dom/vitest"`.

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `getByText(...)` to assert absence | `getBy` throws when missing; use `queryBy...` + `.not.toBeInTheDocument()` |
| Not awaiting `user.click` / `findBy` | Assertion runs too early, flaky test |
| `getBy` for async content | Fails immediately; use `await findBy` |
| Querying by class / CSS | Breaks on styling changes |
| Asserting on internal state | Breaks on harmless refactors |
| Mocks leaking between tests | Order-dependent failures |

### 5. Practice Checks
* Not attempted (decided overview-only). Revisit in Project 1 / Phase 14: write tests for `useDebounce`, a form with validation errors, and a data-loading component.

### 6. Optional / Later
* MSW for network mocking, fake timers for debounce tests, Playwright E2E (Phase 14), `jest-axe` accessibility checks, wrapping consumers in Providers for context tests.

---

# Phase 4 Complete

All 12 topics covered. **Topics 1-10 studied with practice checks; Topics 11 and 12 are overview only.**
Weak spots to keep practising: stale closures, and "new reference every render defeats `memo`/`use`/effect deps".

---
