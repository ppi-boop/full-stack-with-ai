# Phase 4 — React

*Research date: 2026-10-09. React docs checked: react.dev (React 19.2 era). Written for a learner who already uses React at work, so this phase is gap-filling with depth, not a beginner course.*

## Why this phase matters

You already ship React code, so the risk is not "I cannot build a component". The risk is a set of half-understood ideas that work until the app gets big: why a component re-rendered, why an effect fires twice, why a list item kept the wrong text, or why `useMemo` did nothing. Interviewers and senior reviewers probe exactly these points. This phase also updates your mental model to React 19 and the React Compiler, because a lot of older advice (wrap everything in `useCallback`, use `forwardRef`, use `useFormState`) is now outdated or unnecessary. Be honest with yourself: if you cannot explain, from memory, the render phase vs the commit phase, you have a gap worth fixing this week.

## Prerequisites and "skip test"

You can skip a topic below only if you can DEMONSTRATE it, not just recognise it.

- Build, with no AI help and in under 30 minutes, a TypeScript component with a controlled form (3 fields, validation on blur and on submit, error messages tied to inputs with `aria-describedby`).
- Explain out loud (or in writing) what triggers a re-render, and name three things that do NOT cause one.
- Given a buggy component with an effect that fetches data and has a stale-response race, fix it with cleanup (`AbortController` or an `ignore` flag).
- Given a list with `key={index}` and inputs inside each row, predict the bug after deleting the first row, then fix it.
- Write a test with React Testing Library that finds a button by role, clicks it with `userEvent`, and asserts the UI changed.

If you pass all five, skim the concepts and spend the time on Phase 5 and Project 1. If you fail any, study that section carefully.

> **Honest note:** "I use React at work" and "I understand React" are different claims. Most gaps hide in effects, keys, and memoization. These are also the most common interview topics.

## Concepts explained

A map of this section. General React concepts come first. Everything that only exists in a framework (Next.js) is in Phase 5 and clearly marked there.

### Components, JSX and the render model

**[Must learn now]**

A component is a function that takes props and returns a description of UI (JSX). JSX is not HTML. It is syntax that becomes function calls which create plain objects ("elements"). React's job is to compare the description you return now with the one from last time and update the real DOM as little as needed.

Analogy: a component is a recipe card. Each time the data changes, React re-reads the recipe and compares the new dish to the old photo of the dish, then fixes only the differences.

The key mental model from the official docs is three steps: **trigger** (state changed or first mount), **render** (React calls your component functions to compute the new description), **commit** (React applies the differences to the DOM, then runs effects). Rendering is just calling your function. It must be pure: same props and state in, same JSX out, no side effects, no mutating things that existed before the render.

```tsx
type GreetingProps = { name: string; unread?: number };

export function Greeting({ name, unread = 0 }: GreetingProps) {
  // Pure: compute from props, never mutate props
  return (
    <p>
      Hello {name}
      {unread > 0 && <span> ({unread} new)</span>}
    </p>
  );
}
```

Common mistake: mutating a prop or a module-level variable during render, or calling `Math.random()` / `Date.now()` in render and expecting stable output. In Strict Mode (dev only) React renders twice on purpose to expose this.

Interview questions:
- What is the difference between the render phase and the commit phase?
- Why must a component be pure? What does Strict Mode do to help you find impurity?
- Is JSX required to use React?

### Props, state and "state is a snapshot"

**[Must learn now]**

Props are inputs from the parent. State is memory owned by the component. The most missed idea: **state is a snapshot**. Inside one render, the value of `count` is fixed, even if you call `setCount` three times. Calling the setter asks React to schedule another render with a new value.

```tsx
function Counter() {
  const [count, setCount] = useState(0);
  function addThree() {
    setCount(count + 1); // uses snapshot: 0 + 1
    setCount(count + 1); // still 0 + 1
    setCount(count + 1); // still 0 + 1 -> final result 1
    // Use the updater form when the next value depends on the previous one:
    // setCount((c) => c + 1) three times -> 3
  }
  return <button onClick={addThree}>{count}</button>;
}
```

State updates are batched (several `set` calls in one event become one render). Never mutate state objects or arrays; create new ones (`[...items, newItem]`, `{ ...user, name }`). Keep state minimal: do not store anything you can compute from other state or props ("derived state"). Choose the state structure carefully: avoid contradictory booleans (`isLoading` and `isError` and `isSuccess`), prefer one `status` string union.

Common mistake: storing a copy of a prop in state (`useState(props.value)`) and then wondering why it does not update when the prop changes. State is only initialised once.

Interview questions:
- Why does calling `setCount(count + 1)` three times add only one?
- When do you use the updater function form of a setter?
- Why do we not mutate state directly?

### Rendering and re-rendering (the big one)

**[Must learn now]**

A component re-renders when (1) its own state changes, (2) its parent re-renders (by default, ALL children re-render, even if their props are identical), or (3) a context it reads changes. A re-render means "React calls your function again". It does NOT mean "the DOM is rebuilt". After rendering, React compares and only touches the DOM where the output differs. So a re-render is often cheap; it only matters when the render itself is expensive or runs very often.

Things that do NOT cause a re-render: changing a `ref.current`, mutating a normal variable, mutating state without calling the setter. Setting state to the same value (compared with `Object.is`) usually bails out.

Fix order when something feels slow (cheapest first): (1) move state down so fewer components depend on it, (2) lift expensive content up and pass it as `children` (the "children as slot" trick keeps it from re-rendering), (3) split the context, (4) only then memoize. Use the React DevTools Profiler to measure ("Highlight updates" and "Why did this render?") before changing anything.

```tsx
// Slow: typing in the input re-renders <ExpensiveTree /> every keystroke
function Page() {
  const [text, setText] = useState("");
  return (
    <>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <ExpensiveTree />
    </>
  );
}
// Fix 1: move the state into its own small component
function SearchBox() {
  const [text, setText] = useState("");
  return <input value={text} onChange={(e) => setText(e.target.value)} />;
}
function PageFixed() {
  return (
    <>
      <SearchBox />
      <ExpensiveTree />
    </>
  );
}
```

Common mistake: believing "re-render = slow" and memoizing everything. Or defining a component function inside another component, which creates a new component type every render and destroys all state of the inner component.

Interview questions:
- Does a parent re-render always re-render its children? How can you prevent it?
- What is the difference between a re-render and a DOM update?
- Why is defining a component inside another component a bug?

### Event handlers

**[Must learn now]**

Handlers are functions you pass to `onClick`, `onChange` and so on. They run after render, so they are the right place for side effects caused by a user action (send a POST, navigate, open a dialog). Handlers see the snapshot of the render they were created in. React uses a synthetic event that wraps the browser event; you can call `e.preventDefault()` and `e.stopPropagation()` as usual. Events bubble up the component tree, so a child click also fires parent handlers unless stopped.

Common mistake: calling the function instead of passing it (`onClick={doIt()}` runs during render). Putting "after user clicked" logic in an effect instead of the handler.

Interview questions:
- What is the difference between `onClick={fn}` and `onClick={fn()}`?
- Where should a POST request triggered by a button live: in the handler or in an effect? Why?

### Conditional rendering and lists

**[Must learn now]**

Use `&&`, ternaries, or early `return null`. Watch out for `{count && <Badge />}` which renders `0` when `count` is zero. Use `count > 0 &&`. For lists, use `.map()` and give every item a stable `key`.

Common mistake: forgetting that `0`, `""` and `NaN` render differently from `false`/`null`/`undefined`.

Interview question: Why can `{items.length && <List />}` print a stray `0`?

### Keys and reconciliation

**[Must learn now]**

Reconciliation is how React decides what changed between two renders. React walks the old and new trees. If the element type at a position is the same, it keeps the existing instance (and its state) and updates props. If the type differs, it throws away the subtree and builds a new one. In lists, the **key** tells React which item is which across renders.

Rules for keys: unique among siblings, stable (same item, same key each render), not random (`Math.random()` makes React recreate every row every render). Use a database id. `key={index}` is only safe for static lists that are never reordered, filtered or edited.

Analogy: keys are name tags at a party. If everyone swaps tags, React thinks the people swapped, so Anna's drink (state) ends up with Bob.

The same mechanism has a useful trick: change a component's `key` to reset all its state on purpose (for example `<ProfileForm key={userId} />` when the selected user changes). The official guide "Preserving and Resetting State" covers this, and it is often a better fix than an effect that syncs state from props.

```tsx
{todos.map((t) => (
  <TodoRow key={t.id} todo={t} />   // stable id, not index
))}

<ProfileForm key={selectedUserId} user={user} /> // new key = fresh state
```

Common mistake: `key={index}` with inputs or checkboxes inside rows, then deleting or sorting rows; the typed text stays at the old position.

Interview questions:
- What happens if two siblings share a key? If a key changes on every render?
- When is `key={index}` acceptable?
- How can you reset a component's state without an effect?

### Controlled vs uncontrolled inputs

**[Must learn now]**

A controlled input's value lives in React state (`value` + `onChange`). An uncontrolled input keeps its value in the DOM; you read it on submit via a ref or `FormData`. Controlled gives instant validation, formatting, and dependent fields. Uncontrolled is simpler and faster for large forms and plays well with React 19 form Actions and Server Actions (see below). A mixed state (`value` that flips from `undefined` to a string) triggers the "uncontrolled to controlled" warning, so initialise with `""`.

```tsx
function NameField() {
  const [name, setName] = useState(""); // "" not undefined
  return (
    <label>
      Name
      <input value={name} onChange={(e) => setName(e.target.value)} />
    </label>
  );
}
```

Common mistake: setting `value` without `onChange` (field becomes read-only), or storing every keystroke of a 40-field form in the top-level state of a big component, causing slow typing.

Interview question: When would you choose an uncontrolled input on purpose?

### Forms and validation (including React 19 Actions)

**[Must learn now]**

Pick a rule: validate on the server always (the client is advisory), and validate on the client for fast feedback. Put validation in a pure function or schema (for example Zod) outside JSX so you can unit test it. Bind server errors back to fields by name. Show errors next to the input, connect them with `aria-describedby`, and set `aria-invalid`.

React 19 added **Actions**: you can pass a function to `<form action={fn}>`. React runs it inside a transition, gives you pending state, and resets uncontrolled fields after success. The related hooks are:

- `useActionState(action, initialState)` returns `[state, formAction, isPending]`. It was renamed from the old `useFormState`; the old name is deprecated.
- `useFormStatus()` inside a child of the form gives `pending`, `data`, `method`, `action`.
- `useOptimistic(value)` shows a temporary value while the async work runs, then snaps to the real result or reverts on failure.

```tsx
"use client"; // only needed inside Next.js; plain React needs nothing
import { useActionState } from "react";

type State = { error?: string; ok?: boolean };

async function saveName(prev: State, formData: FormData): Promise<State> {
  const name = String(formData.get("name") ?? "").trim();
  if (name.length < 2) return { error: "Name is too short" };
  await fetch("/api/profile", { method: "POST", body: JSON.stringify({ name }) });
  return { ok: true };
}

export function ProfileForm() {
  const [state, formAction, isPending] = useActionState(saveName, {});
  return (
    <form action={formAction}>
      <input name="name" aria-invalid={!!state.error} aria-describedby="name-err" />
      <p id="name-err" role="alert">{state.error}</p>
      <button disabled={isPending}>{isPending ? "Saving..." : "Save"}</button>
    </form>
  );
}
```

Common mistake: only validating on the client; disabling the submit button without giving the user a reason; reading `FormData` values without checking types.

Interview questions:
- What does `useActionState` return, and what was it called before?
- Why must validation also happen on the server?
- Controlled form vs `FormData`: trade-offs?

### Lifting state up and composition

**[Must learn now]**

When two siblings need the same data, move the state to their closest common parent and pass it down. Before reaching for Context or a store, try **composition**: pass JSX as `children` or as a named prop so the middle components never need to know about the data. This avoids "prop drilling" without any global state.

```tsx
function Layout({ sidebar, children }: { sidebar: React.ReactNode; children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-[240px_1fr]">
      <aside>{sidebar}</aside>
      <main>{children}</main>
    </div>
  );
}
```

Common mistake: creating a Context for something only two levels deep, or building a "god component" with ten boolean props instead of composing smaller pieces.

Interview questions:
- What is prop drilling and name three ways to avoid it.
- What is the "children as a prop" pattern and why does it help performance?

### Hooks: useState, useReducer, useRef

**[Must learn now]**

Rules of Hooks: call hooks at the top level of a component or custom hook, never inside conditions, loops or nested functions, so React can match each hook call to its stored slot by call order. The ESLint plugin `eslint-plugin-react-hooks` enforces this.

- `useState` for simple independent values.
- `useReducer` when many state fields change together or the next state depends on an action type. It makes transitions explicit and testable.
- `useRef` holds a value that survives renders without causing a re-render: DOM nodes (focus, scroll, measure), timers, "previous value", the latest callback. Never read or write `ref.current` during render (except lazy init); do it in handlers and effects.

React 19 note: `ref` is now a normal prop on function components, so new code no longer needs `forwardRef`. Ref callbacks can also return a cleanup function.

Common mistake: using `useRef` to store data that should update the screen (it will not re-render).

Interview questions:
- Why are hook calls order-dependent?
- `useState` vs `useRef`: when does each fit?
- When would you pick `useReducer`?

### Effects: what they are for

**[Must learn now]**

An effect (`useEffect`) is an escape hatch to **synchronise a component with an external system**: a WebSocket, a browser API listener, a third-party widget, the network. It runs after the commit. It is not "componentDidMount". The right question is not "when should this run?" but "what external thing must stay in sync with these values?".

The shape is: setup function, optional cleanup function returned, dependency array. React calls cleanup before re-running the effect and on unmount. In dev Strict Mode React runs setup, cleanup, setup once on mount to prove your cleanup is correct; if that breaks your code, your cleanup is missing. This double run is NOT a bug in React.

```tsx
useEffect(() => {
  const ws = new WebSocket(`wss://example.test/rooms/${roomId}`);
  ws.onmessage = (e) => addMessage(JSON.parse(e.data));
  return () => ws.close();          // cleanup
}, [roomId]);                       // re-sync when roomId changes
```

Dependencies are not a list you choose; they are every reactive value (props, state, values derived from them) that the effect reads. Lint the dependency array and obey it. If a dependency causes too many re-runs, the fix is to change the code (move the function inside the effect, move constants outside the component, derive less), not to delete the dependency.

New in React 19.2: `useEffectEvent` lets you read the latest props or state inside an effect without making that value a dependency (for example logging "connected" with the current theme without reconnecting when the theme changes). It must be called only from effects, and must not be put in the dependency array. Newer ESLint rules in `eslint-plugin-react-hooks` v6 expect this.

Common mistakes: effects without cleanup (leaks, duplicate listeners); missing dependencies (stale values); `async` function passed directly to `useEffect`; objects or functions created during render used as dependencies (new identity every render, so the effect runs every time).

Interview questions:
- Why does my effect run twice in development?
- What is the dependency array really saying?
- What goes in a cleanup function? Give three examples.
- What does `useEffectEvent` solve?

### Avoiding unnecessary effects

**[Must learn now]**

This is the single most valuable page in the React docs for working developers: "You Might Not Need an Effect". The rule: if there is no external system involved, you probably do not need an effect. Replace these patterns:

| Pattern you often see | Better approach |
| --- | --- |
| `useEffect` that sets state derived from props or state | Compute it during render (`const fullName = first + " " + last`) |
| Effect to filter or sort a list into state | Compute during render; `useMemo` only if measured slow |
| Effect that runs after a button click | Put the logic in the click handler |
| Effect to reset state when a prop changes | Give the component a `key`, or compute during render |
| Chain of effects that each set state | Compute the next state in one handler |
| Effect to tell the parent something changed | Call the parent's callback in the same event handler |
| Effect that subscribes to an external store | `useSyncExternalStore` |
| Effect for data fetching in a framework app | Server Components, a data library (TanStack Query, SWR), or the framework loader |

```tsx
// Bad: extra render + stale intermediate state
const [visible, setVisible] = useState<Todo[]>([]);
useEffect(() => setVisible(todos.filter((t) => !t.done)), [todos]);

// Good: derive during render
const visible = todos.filter((t) => !t.done);
```

Interview questions:
- Give three cases where an effect is the wrong tool and the replacement for each.
- Why is "derived state in an effect" an anti-pattern?

### Context API and state-management decisions

**[Must learn now]**

Context lets a parent provide a value to any descendant without passing props. It is good for low-frequency, app-wide values: theme, locale, current user, feature flags. Its weakness: when the provided value changes, EVERY component that reads that context re-renders, and `React.memo` on those components does not stop it. React 19 lets you write `<ThemeContext value={...}>` instead of `<ThemeContext.Provider>`.

A decision guide (choose the simplest that works):

| Kind of state | Where it should live |
| --- | --- |
| Local UI (open/closed, input draft) | `useState` in the component |
| Shared by a few nearby components | Lift to the common parent, or composition |
| URL-worthy (filters, page, tab, search term) | The URL (search params). Shareable and survives refresh |
| Server data (lists, details) | A server-state library (TanStack Query / SWR) or Server Components. Do not copy it into global state |
| App-wide, rarely changes | Context |
| Complex client state read by many, changes often | A small store (Zustand, Redux Toolkit, Jotai) |
| Form state | Form state belongs in the form (React Hook Form or native `FormData`) |

Split contexts by how often they change (for example `ThemeContext` separate from `CartContext`), and keep the provider value stable (`useMemo` on the value object, or put state and dispatch in two contexts). Combine with `useReducer` for a lightweight store.

Common mistake: putting server data in Context or Redux and hand-writing loading/error/stale logic. Another: one giant `AppContext` where every keystroke re-renders the whole app.

Interview questions:
- Why can Context cause performance problems? How do you reduce them?
- When would you reach for Redux/Zustand instead of Context?
- Where should the "current page number" of a table live?

### Error boundaries

**[Must learn now]**

An error boundary catches errors thrown during rendering of its children and shows a fallback UI instead of white-screening the whole app. It does NOT catch errors in event handlers, async code (promises, `setTimeout`), or server-side rendering. For handlers, use `try/catch` and set error state.

React still requires a class component for a hand-written boundary (`getDerivedStateFromError` and `componentDidCatch`). In practice use the `react-error-boundary` library, or your framework's built-in boundary (Next.js `error.tsx` is a boundary for a route segment, see Phase 5).

Place boundaries at meaningful granularity: one per route and one around risky widgets (a chart, a third-party embed), so one failure does not hide everything.

Common mistake: wrapping the whole app in one boundary only; expecting a boundary to catch a failed `fetch` in an effect.

Interview questions:
- What errors do error boundaries not catch?
- How do you reset an error boundary after the user fixes the problem?

### Custom hooks, reusable components and folder structure

**[Must learn now]**

A custom hook is a function whose name starts with `use` that calls other hooks to share **stateful logic** (not state itself: each call gets its own state). Extract one when logic repeats or when a component mixes too many concerns (`useDebouncedValue`, `useLocalStorage`, `useMediaQuery`, `useDisclosure`). Keep them small and typed.

Reusable components: accept `className` and spread remaining props (`...rest`), support `ref` (as a plain prop in React 19), prefer composition (`<Card><Card.Header/></Card>`) over a pile of boolean props, and keep styling variants in one place (`cva` or a map). Accessibility belongs inside the component (labels, roles, focus management) so every use is accessible by default.

Folder structure: organise by feature, not by file type, once the app has more than a few screens.

```text
src/
  features/
    orders/
      components/   OrderTable.tsx, OrderFilters.tsx
      hooks/        useOrders.ts
      api.ts        typed fetch functions
      schemas.ts    Zod schemas and types
  components/ui/    Button.tsx, Input.tsx, Dialog.tsx   (shared primitives)
  lib/              utils, constants
```

Rule of thumb: code used by one feature lives in that feature; promote it to shared only when a second feature needs it.

Interview questions:
- What can and can't a custom hook share?
- How do you decide between a prop and composition?

### Data fetching with loading, error and empty states

**[Must learn now]**

Every data view has at least four states: **loading**, **error**, **empty**, **success**. Write all four on purpose. A discriminated union keeps them honest:

```ts
type Remote<T> =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: T };
// "empty" is success with data.length === 0: render a friendly empty state
```

Hand-written `useEffect` + `fetch` has pitfalls: race conditions (an old response overwrites a newer one), no cancellation, no caching, no retry, duplicate requests in Strict Mode. If you must write it yourself, cancel with `AbortController` and ignore aborted errors:

```tsx
useEffect(() => {
  const ctrl = new AbortController();
  setStatus("loading");
  fetch(`/api/orders?page=${page}`, { signal: ctrl.signal })
    .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
    .then((data) => { setData(data); setStatus("success"); })
    .catch((err) => { if (err.name !== "AbortError") setStatus("error"); });
  return () => ctrl.abort();
}, [page]);
```

Note: `fetch` does not reject on HTTP 404 or 500; check `response.ok` yourself. In real apps prefer a server-state library: TanStack Query gives caching, deduplication, retries, background refetch, `isPending`/`isError`, `placeholderData` for smooth pagination, and mutations with cache invalidation. React 19 also adds `use(promise)` to read a promise during render with `Suspense` for loading and an error boundary for errors; the promise should come from a cache or a Server Component, not be created fresh on each render.

Common mistakes: no error state; spinner forever on failure; empty list looks the same as "still loading"; fetching in an effect on the server-rendered path of a framework when a Server Component would do it; no cancellation.

Interview questions:
- How do you avoid a race condition between two quick requests?
- Why does `fetch` not throw on a 500?
- When would you add TanStack Query instead of `useEffect`?

### Transitions, Suspense and concurrent features

**[Learn during projects]**

`useTransition` marks a state update as non-urgent so typing stays responsive while a heavy re-render happens in the background (and gives `isPending`). `useDeferredValue` gives a lagging copy of a value for the same purpose. `Suspense` shows a fallback while a child waits for data or lazy code (`React.lazy`). These matter in Next.js (Phase 5) because navigation and Server Actions run inside transitions. React 19.2 also adds `<Activity>`, which hides UI (like `display: none`) while keeping its state and cleaning up its effects.

Interview question: What is the difference between `useTransition` and `useDeferredValue`?

### Performance and memoization (and when NOT to memoize)

**[Must learn now]**

`React.memo(Component)` skips re-render when props are shallow-equal. `useMemo(fn, deps)` caches a computed value. `useCallback(fn, deps)` caches a function identity. They are tools for two cases only: (1) a computation that is measurably expensive, (2) keeping a stable identity that a memoized child or an effect dependency needs.

When NOT to memoize:
- The child is not wrapped in `memo` (a stable function prop changes nothing).
- The computation is cheap (filtering 50 items, string concat).
- The dependencies change on almost every render (the cache never hits).
- You have not measured. Profile first.
- You are building app code in a codebase using the **React Compiler**.

The **React Compiler** (stable 1.0; Next.js 16 supports it through the `reactCompiler` option, which is OFF by default) adds memoization at build time, so manual `useMemo`, `useCallback` and `React.memo` are usually unnecessary in compiler-enabled code. It requires code that follows the Rules of React (pure render, no mutation). Existing manual memoization can stay. Enabling it raises build times because it uses Babel. Treat it as an option to evaluate, and check the official docs for the current install steps.

Other real performance tools, in order of effect: render less (state colocation, composition), render fewer things (pagination, virtualization of long lists, for example TanStack Virtual), load less code (`lazy`, dynamic import), and avoid layout thrash. Always measure with the Profiler and Lighthouse.

```tsx
// Worth it: heavy work, stable inputs
const sorted = useMemo(() => sortBig(rows, sortKey), [rows, sortKey]);

// Pointless: child is not memoized, so it re-renders anyway
const onClick = useCallback(() => setOpen(true), []);
return <PlainChild onClick={onClick} />;
```

Common mistakes: memoizing everything "just in case"; wrong or missing dependencies making cached values stale; passing a new object literal to a memoized child (`style={{...}}`), which defeats `memo`.

Interview questions:
- When does `useCallback` actually help?
- Why can `React.memo` fail to prevent re-renders?
- What does the React Compiler change about how you write code?

### Testing fundamentals

**[Must learn now]**

Test what the user sees and does, not implementation details. The standard stack is Vitest or Jest as the runner, React Testing Library (RTL) for rendering and queries, `@testing-library/user-event` for realistic interactions, and `jest-dom` matchers. Prefer queries by role and label (`getByRole("button", { name: /save/i })`), which also nudges you to accessible markup. Use `findBy*` for async appearance, `queryBy*` to assert absence. Mock the network at the boundary with MSW rather than mocking `fetch` inside components.

```tsx
test("shows validation error then saves", async () => {
  const user = userEvent.setup();
  render(<ProfileForm />);
  await user.click(screen.getByRole("button", { name: /save/i }));
  expect(await screen.findByRole("alert")).toHaveTextContent(/too short/i);
});
```

Test pyramid for a frontend: many fast unit tests (pure functions, hooks, small components), some integration tests (a page with mocked API), a few end-to-end tests (Playwright) for critical flows. Coverage percentage is a smoke alarm, not a goal.

Common mistakes: testing internal state or CSS class names; using `getByTestId` for everything; not awaiting async UI; snapshot tests of huge trees.

Interview questions:
- Why prefer `getByRole` over `getByTestId`?
- How do you test a component that fetches data?
- What do you NOT unit test?

### Accessibility and maintainability

**[Must learn now]**

Use real elements (`button` for actions, `a` for navigation, `label` tied to inputs). Manage focus when opening dialogs and after route changes. Make every interactive thing reachable and operable by keyboard. Do not rely on color alone for state. Use ARIA only when native HTML cannot do the job. Add `eslint-plugin-jsx-a11y`, and test with the keyboard and a screen reader at least once per project. For maintainability: TypeScript strict mode, small components (a good guide is under about 150 lines), colocated tests, no dead props, and clear names.

Interview questions:
- When do you use `div onClick` instead of `button`? (Almost never. Explain why.)
- How do you make a modal accessible?

### Common React mistakes checklist

**[Must learn now]**

- Component defined inside another component.
- Using `index` as `key` in dynamic lists.
- Effect used for derived data or for event logic.
- Missing cleanup or missing dependencies.
- Mutating state or props.
- Memoizing without measuring.
- Putting server data in global state.
- No error and empty states.
- Fetch without `response.ok` check.
- `Math.random()` or `Date.now()` in render.
- Async function passed directly to `useEffect`.

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Render model and state | Trigger, render, commit; state as snapshot; batching | [Render and Commit](https://react.dev/learn/render-and-commit), [State as a Snapshot](https://react.dev/learn/state-as-a-snapshot), [Queueing updates](https://react.dev/learn/queueing-a-series-of-state-updates) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Predict output of 3 snippets, then run them |
| Re-rendering and profiling | Parent re-renders, context, DevTools Profiler | [React Developer Tools](https://react.dev/learn/react-developer-tools), [Profiler](https://react.dev/reference/react/Profiler) | [Exploring React Performance](https://www.youtube.com/watch?v=uAmRtE52mYk) (React Conf, English, duration not verified) | Intermediate | 2 h | Profile a slow list; fix by moving state down |
| Keys and reconciliation | Keys, state reset with key | [Rendering Lists](https://react.dev/learn/rendering-lists), [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state) | [React Reset Component State With the Key Prop](https://www.youtube.com/watch?v=pu-FjumEY94) (Coding in Flow, English, duration not verified); Hindi option: [How React works under the Hood](https://www.youtube.com/watch?v=UKn4aVlnB9A) (Coder Army, language not verified from title, duration not verified) | Intermediate | 1.5 h | Reproduce index-key bug, then fix |
| Effects | Sync with external system, cleanup, dependencies | [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects), [useEffect](https://react.dev/reference/react/useEffect), [Removing Effect Dependencies](https://react.dev/learn/removing-effect-dependencies) | [Mastering React's useEffect](https://www.youtube.com/watch?v=dH6i3GurZW8) (Jack Herrington, English, duration not verified) | Intermediate | 3 h | Build a chat-room connect/disconnect with cleanup |
| Avoiding effects, Effect Events | Derived state, handlers, useEffectEvent | [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects), [useEffectEvent](https://react.dev/reference/react/useEffectEvent) | [New React useEffectEvent Hook Crash Course](https://www.youtube.com/watch?v=NZJUEzn10FI) (Web Dev Simplified, English, duration not verified) | Intermediate | 2.5 h | Refactor 5 effects in a sample app; delete at least 3 |
| Forms and Actions | Controlled inputs, FormData, useActionState, useOptimistic | [React 19 release post](https://react.dev/blog/2024/12/05/react-19), [useActionState](https://react.dev/reference/react/useActionState), [form](https://react.dev/reference/react-dom/components/form) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Build a form with pending, error, success |
| Context and state decisions | Context cost, reducer, URL state | [Passing Data Deeply with Context](https://react.dev/learn/passing-data-deeply-with-context), [Scaling Up with Reducer and Context](https://react.dev/learn/scaling-up-with-reducer-and-context), [Choosing the State Structure](https://react.dev/learn/choosing-the-state-structure) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Fill the state-placement table for your work app |
| Data fetching | Loading/error/empty, abort, TanStack Query | [TanStack Query docs](https://tanstack.com/query/latest), [use](https://react.dev/reference/react/use), [Suspense](https://react.dev/reference/react/Suspense) | No video verified for this topic; use the official documentation above. | Intermediate | 3 h | Write a fetch hook with AbortController, then replace with Query |
| Memoization and Compiler | memo, useMemo, useCallback, Compiler | [memo](https://react.dev/reference/react/memo), [useMemo](https://react.dev/reference/react/useMemo), [useCallback](https://react.dev/reference/react/useCallback), [React Compiler](https://react.dev/learn/react-compiler) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Measure before/after on a 5,000-row list |
| Testing | RTL, user-event, Vitest, MSW | [Testing Library intro](https://testing-library.com/docs/react-testing-library/intro/), [Queries](https://testing-library.com/docs/queries/about), [user-event](https://testing-library.com/docs/user-event/intro), [Vitest](https://vitest.dev/guide/), [MSW](https://mswjs.io/docs/) | [React Testing for Beginners: Start Here!](https://www.youtube.com/watch?v=8Xwq35cPwYg) (Programming with Mosh, English, duration not verified) | Beginner to intermediate | 3 h | Test a form + a data table with MSW |
| Accessibility | Roles, focus, keyboard | [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/), [Testing Library queries](https://testing-library.com/docs/queries/about) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Keyboard-only walk through your dashboard |

## Verification notes

- All React/testing documentation links above returned HTTP 200 when fetched on 2026-10-09. I read the content of these pages in full or in summary: React 19 release post, React 19.2 post, You Might Not Need an Effect, memo, useEffectEvent, React Compiler landing page. The remaining doc links were checked to resolve (HTTP 200) but I did not read them end to end.
- The authoring machine could not open youtube.com directly (TLS connection failed), so `curl` against YouTube oEmbed and `lengthSeconds` could not be run. Instead I confirmed each video's exact title and channel through the noembed.com oEmbed mirror, which returns data fetched from YouTube. I did NOT verify durations, upload dates, or the video content beyond title and channel. Treat all durations as "not verified".
- Videos confirmed by title and channel: "Exploring React Performance" (React Conf); "React Reset Component State With the Key Prop" (Coding in Flow); "How React works under the Hood | React reconciliation, fibre, diffing, key | ReactJS Full Course #6" (Coder Army; the title suggests Hindi-medium content but language is not verified); "Mastering React's useEffect" (Jack Herrington); "New React useEffectEvent Hook Crash Course" (Web Dev Simplified); "React Testing for Beginners: Start Here!" (Programming with Mosh).
- Possibly outdated: the Mosh testing video may use Jest rather than Vitest and may predate React 19. The `useEffect` video predates `useEffectEvent`. Use the official docs as the source of truth for React 19/19.2 behavior.

## Hands-on exercises

1. **Re-render lab.** Create a page with a text input and a slow component (loop 2 ms per item, 200 items). Record a Profiler session. Fix it three ways: move state down, pass the slow part as `children`, then `memo`. Write down which fix was simplest and why.
2. **Key bug lab.** Build a list of 5 rows, each with a text input. Use `key={index}`, type in row 1, delete row 0, observe. Fix with ids. Then add `key` on a `<UserForm>` to reset state when the selected user changes.
3. **Effect audit.** Take one of your real components with 2 or more effects. For each effect, write "external system: ___". If you cannot fill it in, rewrite the code without the effect.
4. **Cancelable fetch.** Write `useOrders(page, query)` with `AbortController`, loading/error/empty states and a discriminated union result. Type it strictly. Then rebuild it with TanStack Query and compare lines of code and behavior on fast page switching.
5. **Form with Actions.** Build a form with `useActionState`, an inline validator (Zod), accessible error messages, and a pending state. Add `useOptimistic` to show the new item at once in a list.
6. **Context cost.** Make a context with `{ theme, user, cart }` in one value. Count re-renders when only `cart` changes. Split it into three contexts and measure again.
7. **Error boundary.** Add a boundary around a widget that throws on a button click in render. Add a "Try again" that resets it. Confirm it does not catch an error thrown inside an `onClick`.
8. **Tests.** Write 6 RTL tests: a form validation test, a list render test, an empty state test, an error state test (MSW returns 500), a keyboard interaction test, and a custom hook test with `renderHook`.
9. **Memoization experiment.** Render 5,000 rows. Measure with the Profiler: baseline, with `memo` plus stable props, and (optional) with the React Compiler on. Write a one-paragraph conclusion.

## Checkpoint

Answer these without notes, then check the docs.

- **Explain:** (a) What happens between `setState` and the screen updating? (b) Why do we get double effects in dev? (c) What does a key do? (d) Context vs a store vs URL state for "selected tab".
- **Modify code:** Given a component with `useEffect(() => setFiltered(...), [items, query])`, remove the effect. Given a row list with `key={i}`, make deletions correct.
- **Debug:** A search box fires a request per keystroke and old responses sometimes overwrite new ones. Find and fix the race (cancellation or ignore flag, plus debounce).
- **Write tests:** Write an RTL test for a form that shows an inline error and a success message, using `userEvent` and role queries.

**Ready to move on when** you can pass the five skip-test items above without help, you have completed exercises 1, 2, 4 and 8, and you can explain "when NOT to memoize" in two minutes to a colleague.


# Phase 5 — Next.js and Frontend Architecture (App Router)

*Research date: 2026-10-09. Docs checked: nextjs.org/docs, shown as version 16.4 (page "last updated" dates between 2026-09-01 and 2026-10-06). Everything in this phase is Next.js-specific unless a heading says "general React".*

## Why this phase matters

Next.js is the framework most React jobs in India and worldwide ask for, and you already use it. The problem is that the App Router changed a lot between Next.js 13, 14, 15 and now 16, and many tutorials and AI answers still describe old behavior (implicit `fetch` caching, `middleware.ts`, synchronous `params`, `getServerSideProps`). Knowing which model is current, and being able to say WHY a page is static, cached or dynamic, is what separates "I follow tutorials" from "I own the architecture". This phase also gives you the frontend half of the full-stack story: when Server Functions and Route Handlers are enough, and when you need a separate backend (Phase 6).

> **Outdated?:** Be careful with anything written before late 2025. Next.js 16 removed synchronous access to `params`, `searchParams`, `cookies()` and `headers()`; renamed `middleware` to `proxy`; made Turbopack the default bundler; removed `next lint`; and introduced Cache Components (`use cache`) as the new caching model. The old caching model is documented separately in the official guide "Caching and Revalidating (Previous Model)". When an AI assistant or blog post disagrees with the docs, the docs win.

## Prerequisites and "skip test"

- Phase 4 skip-test items (or equivalent) done.
- You can explain what SSR, SSG and CSR mean and the browser's request/response cycle (Phase 0 and Phase 3).
- To skip a topic you must demonstrate it: create a fresh app, add a nested layout with a route group, a dynamic route with `loading.tsx`, `error.tsx` and `not-found.tsx`, a Server Component that fetches data, and a Client Component island; then explain in one sentence per route whether it renders at build time or request time and why.

## Concepts explained

Legend used below: **[Next.js]** = framework feature that does not exist in plain React. **[React]** = a React feature (stable in React 19) that Next.js uses and plain React can also use, although Server Components and Server Functions need a framework or bundler support.

### Installation, setup and project structure

**[Must learn now]** **[Next.js]**

Requirements today: Node.js 20.9 or newer, TypeScript 5.1 or newer, modern browsers (Chrome/Edge/Firefox 111+, Safari 16.4+). Create an app with `npx create-next-app@latest my-app` (or add `--yes` for defaults). The recommended defaults are TypeScript, ESLint, Tailwind CSS, App Router, Turbopack, Cache Components enabled, an `AGENTS.md` file for coding agents, the `@/*` import alias, no `src/` folder, and the React Compiler OFF. Scripts are `next dev`, `next build`, `next start`. Turbopack is the default bundler for both dev and build; use `--webpack` to opt out. `next build` no longer runs the linter, so add `eslint` as its own script and CI step.

```text
app/
  layout.tsx          root layout (required, has <html> and <body>)
  page.tsx            route "/"
  globals.css
  (marketing)/        route group: folder name not in URL
    about/page.tsx    "/about"
  dashboard/
    layout.tsx        nested layout, persists across child navigations
    loading.tsx       instant fallback (a Suspense boundary)
    error.tsx         error boundary for this segment ("use client")
    not-found.tsx
    page.tsx          "/dashboard"
    orders/
      page.tsx        "/dashboard/orders"
      [id]/page.tsx   "/dashboard/orders/123"  (dynamic segment)
  api/health/route.ts Route Handler (GET /api/health)
proxy.ts              runs before routes (was middleware.ts)
next.config.ts
```

Rules: the folder tree defines URLs; only `page` and `route` files make a folder publicly routable; colocate components next to routes safely (private folders start with `_`). Use `server-only` to make the build fail if secret code is imported into the client.

Common mistake: reading a tutorial that uses `pages/` and `getServerSideProps` (Pages Router, legacy for new apps) and mixing it with `app/`.

Interview questions:
- What does a route group do? A private folder?
- Why does the root layout have to contain `<html>` and `<body>`?

### Pages, layouts, templates, dynamic routes, navigation and loading states

**[Must learn now]** **[Next.js]**

- A **layout** wraps its children and does NOT re-render or lose state when you navigate between its child pages (partial rendering). A `template` is similar but remounts on navigation.
- **Dynamic segments** `[id]`, catch-all `[...slug]`, optional catch-all `[[...slug]]`. In Next.js 16, `params` and `searchParams` are Promises you must `await` (or read with `use()` in a Client Component). Run `npx next typegen` to get the global `PageProps<'/route'>`, `LayoutProps` and `RouteContext` type helpers.
- **Navigation:** the `<Link>` component (prefetches visible links), `useRouter()` for programmatic navigation in Client Components, `redirect()` and `notFound()` on the server. Next.js 16 reworked prefetching (layout deduplication and incremental prefetching), so you may see more but smaller prefetch requests.
- **Loading states:** `loading.tsx` wraps the page in a Suspense boundary automatically; a `<Suspense fallback>` around a slow component is more precise. Note: a layout that itself reads uncached or runtime data does NOT fall back to the same segment's `loading.tsx`, so put slow reads in the page or in their own Suspense boundary.
- **Parallel routes** (`@slot`) and **intercepting routes** exist for modals and dashboards. In Next.js 16 every parallel slot needs an explicit `default.tsx`, or the build fails. Treat both as **[Learn later if needed]**.

```tsx
// app/dashboard/orders/[id]/page.tsx  (Next.js 16: params is a Promise)
export default async function OrderPage(props: PageProps<"/dashboard/orders/[id]">) {
  const { id } = await props.params;
  const order = await getOrder(id);       // server-side data access
  if (!order) notFound();
  return <OrderDetails order={order} />;
}
```

Common mistake: forgetting `await params` (this is a hard error in Next.js 16, not a warning), or doing an auth check only in a layout (layouts do not re-run on every navigation).

Interview questions:
- Why do layouts not re-render on navigation, and what security trap does this create?
- What is the difference between `loading.tsx` and `<Suspense>`?

### Server Components vs Client Components

**[Must learn now]** **[React concept, Next.js defaults]**

In the App Router every component is a **Server Component** by default. It runs only on the server (at build or request time), can be `async`, can read databases and secrets directly, and sends zero component JavaScript to the browser. Add `"use client"` at the top of a file to mark the **boundary** where the Client Component module graph starts: that file and everything it imports ends up in the browser bundle. Client Components still pre-render to HTML on the server for the first load, then hydrate.

Use a Client Component when you need state, effects, event handlers, browser APIs or custom hooks. Keep them as small "islands" at the leaves (a search box, a chart, a dropdown), not at the top of the page.

Rules that trip people up:
- Props from Server to Client must be serializable (plain data, no functions except Server Functions, no class instances). Dates are fine in React but check JSON consumers.
- You can pass a Server Component as `children` or another prop to a Client Component (the "interleaving" pattern), so a client `Modal` can wrap a server `Cart`.
- Context does not work in Server Components. Create a client `Providers` component and render it as deep as possible (wrap `{children}` only).
- A third-party library without `"use client"` that uses hooks must be wrapped in your own client file.
- Do not put secrets in files a Client Component imports. `NEXT_PUBLIC_` variables are inlined into client code; anything else becomes an empty string there. Add `import "server-only"` to guard modules.

Analogy: the server is the kitchen, the browser is the table. The kitchen prepares the heavy dishes. Only interactive things (a pepper grinder) go to the table.

Interview questions:
- What does `"use client"` actually do? Does every child need it?
- How can a Server Component appear inside a Client Component?
- Why is wrapping the whole app in a client provider at the root a missed optimization?

### Rendering: static, dynamic, SSR, CSR, streaming and Partial Prerendering

**[Must learn now]** **[Next.js]**

Vocabulary: CSR means the browser builds the UI with JavaScript. SSR means the server renders HTML per request. Static rendering (SSG) means HTML is built once at build time and served from a CDN. Streaming means the server sends HTML in chunks as parts become ready, using Suspense boundaries. **Partial Prerendering (PPR)** means a route has a static shell (prerendered HTML) with holes that stream in at request time.

In the current model (Cache Components enabled, which `create-next-app` now turns on by default), you no longer pick static or dynamic for a whole page with a config flag. Instead, at build time Next.js prerenders everything it can. Each part of the tree falls into one of:
- Predictable work (imports, pure computation, sync file reads): included in the static shell automatically.
- Cached with `use cache`: result is cached and included in the shell if its lifetime is long enough.
- Runtime or uncached work (cookies, headers, `searchParams`, uncached `fetch`, database queries): must be inside `<Suspense>` so the fallback ships in the shell and the content streams in per request. If not, the dev overlay shows a "blocking route" insight and tells you how to fix it.
- Random or time values (`Math.random()`, `Date.now()`, `crypto.randomUUID()`): call `await connection()` first inside Suspense to make them per-request, or cache them.

Tip from the docs: the deeper in the tree you `await` runtime data (`params`, `cookies()`), the more of the page can be prerendered. Push the `await` down into a small component inside Suspense.

Bots and crawlers get a fully rendered page rather than a streamed shell, so SEO still works.

Interview questions:
- Explain static shell + streamed holes (PPR) in two sentences.
- Which APIs make a component request-time?
- Why does `loading.tsx` not appear when a layout reads `cookies()`?

### Data fetching and caching (current model) — read this carefully

**[Must learn now]** **[Next.js]**

This is the most outdated area in tutorials. Facts as of Next.js 16.4 docs:

1. **Fetch in Server Components** with plain `async/await` and `fetch`, or call your DB/ORM directly. `fetch` requests are **not cached by default** (they used to be in Next.js 13/14). Identical `fetch` calls in one render pass are memoized (deduplicated).
2. For non-`fetch` data (ORM, SQL) deduplicate within one request with `React.cache` (a React API, request-scoped).
3. **Cache explicitly with `use cache`** (needs `cacheComponents: true` in `next.config.ts`). Put the directive at the top of an async function (data-level) or a component/page (UI-level). Arguments and captured values become the cache key. Pair it with `cacheLife('hours')` (profiles: seconds, minutes, hours, days, weeks, max, or custom) and optionally `cacheTag('orders')` for on-demand invalidation.
4. Variants: `use cache: private` for results that depend on cookies/headers/search params (kept per-browser, in the prefetch), and `use cache: remote` for a durable shared cache across serverless instances. The default `use cache` store is in-memory and per instance, so on serverless it may recompute.
5. **Streaming uncached data:** wrap in `<Suspense>` and keep the fetch uncached.
6. **Parallel fetching:** start requests first, then `await Promise.all([...])`. Sequential `await`s inside one component create waterfalls. For independent sections, give each its own Suspense boundary.
7. **Client Components** can receive a promise from the server and read it with `use(promise)` inside Suspense, or use SWR / TanStack Query for client-driven data.

```tsx
import { cacheLife, cacheTag } from "next/cache";

export async function getProducts() {
  "use cache";
  cacheLife("hours");
  cacheTag("products");
  const res = await fetch("https://dummyjson.com/products?limit=20");
  if (!res.ok) throw new Error("Failed to load products");
  return res.json();
}
```

Old APIs and where they went (if `cacheComponents` is on): route segment configs `dynamic`, `revalidate`, `fetchCache` error and are replaced by `use cache` + `cacheLife`; `fetch(..., { cache, next: { revalidate, tags } })` options move to `use cache` + `cacheLife` + `cacheTag`; `unstable_noStore` is unnecessary; `export const dynamicParams` is unsupported; `runtime = "edge"` is unsupported; `experimental.ppr` and `experimental.dynamicIO` were removed and replaced by `cacheComponents`. `unstable_cache` still works, and migrating is optional. `cacheLife` and `cacheTag` lost their `unstable_` prefix. If you are not using Cache Components, read the "previous model" guide instead.

> **Warning:** Cache Components is not a rename-only change. Turning it on for an existing app can surface build errors for uncached data outside Suspense. The official migration guide describes `instant = false` as an opt-out per segment while you migrate route by route.

Common mistakes: expecting `fetch` to be cached because a 2023 article said so; caching per-user data in a shared `use cache` function (cache keys include arguments, so pass the user id or use `use cache: private`); forgetting that caches are scoped per deployment.

Interview questions:
- How did the default caching of `fetch` change between Next.js 14 and 16?
- What is the cache key for a `use cache` function?
- When do you use `revalidateTag` vs `updateTag`?

### Server Functions (Server Actions), forms and mutations

**[Must learn now]** **[React concept + Next.js integration]**

Terminology as per the current docs: a **Server Function** is an async function that runs on the server and is called from the client over the network (always a POST). Used for mutations or as a form `action`, it is called a **Server Action**. Mark with `"use server"` at the top of a function or a file. You can define inline ones only in Server Components; Client Components import them from a `"use server"` file or receive them as props.

Typical flow in a form: `<form action={createOrder}>` receives `FormData`; validate with Zod on the server; check auth; mutate; then revalidate and redirect.

Cache and refresh APIs after a mutation (all from `next/cache`, except `redirect`):
- `updateTag('orders')` — Server Actions only. Expires the tag and the user sees fresh data immediately (read-your-own-writes). New in Next.js 16.
- `revalidateTag('orders', 'max')` — stale-while-revalidate. The second argument (a cacheLife profile) is now required; the one-argument form is deprecated.
- `revalidatePath('/orders')` — revalidate a route.
- `refresh()` — refresh the client router without touching tagged data.
- `redirect('/orders')` — throws a control-flow exception, so code after it does not run; call revalidate first.

UI: `useActionState(action, initial)` gives `[state, formAction, pending]` for validation errors and pending UI. `useFormStatus` for nested submit buttons. `useOptimistic` for instant feedback. Server Components with form actions work before JavaScript loads (progressive enhancement).

**Security (non-negotiable):** Server Functions are public POST endpoints. Anyone can call them directly with crafted requests, so every function must itself check authentication AND authorization (does this user own this order?) and validate all input. Do not rely on hiding a button or on `proxy.ts` matcher coverage. The docs also note the client currently dispatches Server Functions one at a time, so do not use them for parallel data reads; use Server Components for reads.

```ts
"use server";
import { z } from "zod";
import { updateTag } from "next/cache";
import { redirect } from "next/navigation";
import { requireRole } from "@/lib/dal";

const Schema = z.object({ name: z.string().min(2), qty: z.coerce.number().int().min(1) });

export async function createOrder(prev: unknown, formData: FormData) {
  await requireRole("admin");                       // authZ inside the function
  const parsed = Schema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
  await db.orders.create(parsed.data);
  updateTag("orders");
  redirect("/dashboard/orders");
}
```

Common mistake: trusting client-provided ids (IDOR); returning raw error objects; forgetting to revalidate so the list looks stale.

Interview questions:
- Are Server Actions secure by default? What must you do?
- `updateTag` vs `revalidateTag` vs `revalidatePath`?
- Why call `revalidate*` before `redirect`?

### Route Handlers and when to use them

**[Must learn now]** **[Next.js]**

A Route Handler is a `route.ts` file exporting functions named after HTTP verbs (`GET`, `POST`, ...) using the standard Web `Request` and `Response`. Use them for: webhooks (Stripe, Razorpay), endpoints called by non-React clients (mobile app), file download or streaming, OAuth callbacks, a proxy to hide a third-party API key. Do NOT use a Route Handler to fetch data for your own Server Components; call the function directly. With Cache Components on, `GET` handlers follow the same prerender model as pages: cache data by calling a `use cache` helper from inside the handler (you cannot put the directive on the `GET` export). Treat every handler like a public API: authenticate, authorize, validate, return correct status codes. A POST handler is also a CSRF consideration if you use cookie auth (use SameSite cookies and check Origin; see Phase 14).

Interview question: Server Function or Route Handler for a mobile app endpoint? Why?

### Authentication and protected pages

**[Must learn now]** **[Next.js]**

The official guide splits auth into three jobs: **authentication** (who are you), **session management** (remember it across requests), **authorization** (what may you do). The recommended structure:

1. Prefer a maintained library (Auth.js, Better Auth, Clerk, Supabase and others are listed in the docs) over rolling your own. For learning, build it once by hand.
2. Stateless session: sign a small token (user id, role, expiry; no PII) with `jose`, store it in an `HttpOnly`, `Secure`, `SameSite=Lax` cookie set on the server, with the secret in an env var. Or a database session where the cookie holds an encrypted session id.
3. **Data Access Layer (DAL):** one server-only module with `verifySession()` (wrapped in `React.cache`) and `getUser()`. Every data read and every Server Function calls it. Return **DTOs** (only the fields needed), never whole DB rows.
4. **`proxy.ts`** (new name for middleware, Node.js runtime) is for optimistic checks only: read the cookie, redirect unauthenticated users away from `/dashboard`. Do not do database calls in it because it runs on every route including prefetches. It is not your only line of defense.
5. Do not rely on layout checks. Layouts do not re-run on each navigation and do not guard sibling parallel slots. Check next to the data, or in the leaf component.
6. Remember Server Actions and Route Handlers need their own checks.

```ts
// proxy.ts  (Next.js 16; was middleware.ts)
import { NextResponse, type NextRequest } from "next/server";

export function proxy(req: NextRequest) {
  const hasSession = req.cookies.has("session");
  if (!hasSession && req.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", req.url)); // optimistic only
  }
}
export const config = { matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"] };
```

With Cache Components, reading the session is runtime data, so the docs have a separate guide ("Authentication with Cache Components"). Read it before combining auth with `use cache`.

Common mistake: a "protected" page that is only hidden by a client-side redirect; storing the JWT in `localStorage`; checking roles only in the UI.

Interview questions:
- Why isn't `proxy.ts` enough for authorization?
- Why HttpOnly cookies rather than localStorage for tokens?
- What is a DAL and a DTO?

### Metadata, SEO and image optimization

**[Must learn now]** **[Next.js]**

Export a `metadata` object, or an async `generateMetadata` function for dynamic pages, from `layout` or `page`. File conventions generate `sitemap.xml`, `robots.txt`, `opengraph-image` and icons. Under Cache Components, `generateMetadata` that reads runtime data needs special handling (cache the external data with `use cache`, or add a dynamic marker). The `next/image` component gives responsive `srcset`, lazy loading, modern formats and CLS protection (give `width`/`height` or `fill` with a sized parent, and `priority`/`preload` for the LCP image). Next.js 16 changed image defaults: `minimumCacheTTL` is 4 hours, `qualities` defaults to `[75]`, remote images need `images.remotePatterns` (`images.domains` is deprecated), and local images with query strings need `localPatterns` config. Use `next/font` for self-hosted fonts without layout shift.

Common mistake: unsized images (layout shift); using `<img>` for hero images; forgetting `alt`.

Interview questions: How does `next/image` improve Core Web Vitals? Where would you set a per-page title?

### Error handling and not-found

**[Must learn now]** **[Next.js + React]**

- `error.tsx` (must be `"use client"`) is an error boundary for a segment, receiving `error` and a `reset` function. `global-error.tsx` handles root layout errors.
- `not-found.tsx` plus `notFound()` for missing resources (returns a 404 status).
- Expected errors (validation, "email taken") should be returned as state from Server Functions, not thrown. Unexpected ones throw to the boundary.
- Never send raw error messages with secrets to the client; log on the server.
- With Cache Components you can use `catchError` for component-level boundaries.

Interview question: Which errors go to `error.tsx` and which should be returned as values?

### Environment variables and configuration

**[Must learn now]** **[Next.js]**

`.env.local` for secrets (never commit), `.env.example` for documentation. Only variables prefixed `NEXT_PUBLIC_` are inlined into the browser bundle at **build** time; all others stay server-only. `serverRuntimeConfig` and `publicRuntimeConfig` were removed in Next.js 16: to read a value at request time instead of build time, call `await connection()` first and then read `process.env`. Validate env on startup with Zod so the app fails fast. Never prefix a secret with `NEXT_PUBLIC_`.

Interview question: Why can a `NEXT_PUBLIC_` value not be changed after the build without rebuilding?

### API integration, pagination, search, filters and URL query params

**[Must learn now]** **[Next.js + general React]**

Put list state in the URL so views are shareable, back-button friendly and server-renderable: `/orders?page=2&q=ali&status=paid&sort=-createdAt`. Pattern:

1. The page reads `searchParams` (a Promise) in a small async Server Component wrapped in Suspense, and passes parsed values to the data function.
2. Parse and validate params with Zod (coerce numbers, default values, whitelist sort fields). Never pass raw query values into SQL or an API.
3. A client `SearchBox` uses `useSearchParams`, `usePathname`, `useRouter`; debounce input about 300 ms; call `router.replace` with a new `URLSearchParams` and reset `page` to 1 when filters change. Wrap components using `useSearchParams` in Suspense.
4. Pagination: offset (`page`, `limit`) is simple and fine for admin tables; cursor-based is better for very large or fast-changing data (Phase 7 and 17).
5. Use `startTransition` / `useTransition` for the URL update so the old table stays visible with a pending style.

Common mistake: storing filters in `useState` only (lost on refresh, not shareable); firing a request per keystroke; not resetting `page` on filter change; unvalidated `sort` parameter.

Interview questions:
- Why keep filters in the URL?
- Offset vs cursor pagination trade-offs?

### Deployment, production builds and performance troubleshooting

**[Must learn now]** **[Next.js]**

Deployment options per the docs: Node.js server (`next build` then `next start`), Docker container, static export (limited: no proxy, no Server Functions), or a platform adapter (Vercel and others). For learning, Vercel's free tier is the fastest path; Phase 15 covers Docker and AWS. Production checklist: set env vars on the host, run `next build` in CI with lint and type check as separate steps (since 16, build doesn't lint), set image `remotePatterns`, add error monitoring, check bundle size, and use the official production checklist guide.

Performance troubleshooting, in order: (1) measure with Lighthouse and Web Vitals (LCP, INP, CLS); (2) find waterfalls: sequential awaits, layouts blocking on slow data; (3) check what became a Client Component and how much JS it ships (Next.js 16 removed `First Load JS` from build output because it was inaccurate for RSC apps, so use Lighthouse or the bundle analyzer); (4) add Suspense boundaries so the shell is not blocked; (5) cache expensive reads with `use cache`; (6) fix images and fonts; (7) only then micro-optimize. The dev overlay with Cache Components also reports "blocking route" insights.

Interview questions: How would you diagnose a slow dashboard page? What does the build output tell you?

### Next.js 16 specifics worth knowing (quick reference)

**[Learn during projects]** **[Next.js]**

| Topic | Older behavior (tutorials) | Current (16.x docs) |
| --- | --- | --- |
| Bundler | webpack default, `--turbopack` flag | Turbopack default for dev and build |
| `params`, `searchParams`, `cookies()`, `headers()` | Sync access allowed with warning (15) | Async only; sync removed |
| Middleware | `middleware.ts`, Edge runtime | `proxy.ts`, Node.js runtime (middleware deprecated) |
| `fetch` caching | Cached by default (13/14), then uncached (15) | Uncached; opt in with `use cache` |
| PPR | `experimental.ppr` | Part of Cache Components (`cacheComponents: true`) |
| `revalidateTag('x')` | One argument | Needs cacheLife profile: `revalidateTag('x', 'max')` |
| Read-your-writes | Awkward | `updateTag()` in Server Actions |
| Linting | `next lint`, run by build | Removed; run ESLint or Biome yourself |
| React version | React 18/19 | App Router uses React canary with 19.2 features |
| Image defaults | cache TTL 60 s, any quality | TTL 4 h, `qualities` `[75]`, stricter local/remote rules |
| Parallel routes | `default.js` optional | `default.js` required |

> **Honest note:** The docs also mention newer 16.x items (for example `ensureStatic` in 16.4, partial prefetching, an `instant` route config) that are still maturing. Learn the core model first; revisit these when you hit a real need. I read the caching and migration pages but not every 16.x API page, so verify details in the reference before relying on them.

### The modern full-stack AI frontend: Vercel AI SDK and streaming UI

**[Must learn now]** **[Next.js]**

When building full-stack AI applications, standard HTTP request/response cycles feel broken: waiting 10 seconds for a full LLM completion gives users a blank screen. Traditional Server-Sent Events (SSE) or raw WebSockets require parsing raw chunk buffers, handling connection drops, and manually managing message history state in React.

The **Vercel AI SDK** (`ai` and `@ai-sdk/react`) is the modern standard for connecting React and Next.js App Router frontends with streaming AI models.

Key concepts:
1. **`useChat` hook:** Manages conversation history, user input, optimistic message updates, streaming status, loading indicators, and error states with a single hook.
2. **`streamText` and Route Handlers:** On the server, a Route Handler (`app/api/chat/route.ts`) calls the model and returns a streamed response via `toDataStreamResponse()`.
3. **Generative UI / Tool Invocation:** The model can call client-side or server-side tools that render interactive React components (e.g. order summary cards, approval confirmation dialogs) directly into the message feed instead of plain text.
4. **Cancellation and Abort:** Built-in `stop()` function uses standard browser `AbortController` to immediately terminate the model stream when the user clicks "Stop" or navigates away, saving token costs.

```tsx
// app/api/chat/route.ts
import { anthropic } from "@ai-sdk/anthropic";
import { streamText } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: anthropic("claude-sonnet-5-5"),
    messages,
  });
  return result.toDataStreamResponse();
}
```

```tsx
// app/chat/page.tsx
"use client";
import { useChat } from "@ai-sdk/react";

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, stop } = useChat();

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      {messages.map((m) => (
        <div key={m.id} className={m.role === "user" ? "text-right" : "text-left"}>
          <span className="font-semibold">{m.role}: </span>
          {m.content}
        </div>
      ))}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input value={input} onChange={handleInputChange} placeholder="Ask..." className="border p-2 flex-1" />
        <button type="submit" disabled={isLoading} className="bg-blue-600 text-white px-4">Send</button>
        {isLoading && <button type="button" onClick={stop} className="bg-red-500 text-white px-3">Stop</button>}
      </form>
    </div>
  );
}
```

Common mistake: handling stream chunks manually with raw `fetch()` and `ReadableStreamDefaultReader` instead of using the AI SDK's established protocol.

Interview questions:
- What is the difference between streaming plain text vs streaming structured UI components in Next.js?
- How does `AbortController` protect your API billing when a user abandons a stream?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Full-stack AI UI | Vercel AI SDK, useChat, streamText | [AI SDK Core](https://sdk.vercel.ai/docs/introduction), [AI SDK UI](https://sdk.vercel.ai/docs/ai-sdk-ui/overview) | No video verified for this topic; use the official documentation above. | Intermediate | 2.5 h | Build a streaming chat UI with stop button |
| Setup and structure | create-next-app, folders, routing files | [Installation](https://nextjs.org/docs/app/getting-started/installation), [Project structure](https://nextjs.org/docs/app/getting-started/project-structure), [Layouts and pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages) | No video verified for this topic; use the official documentation above. | Beginner to intermediate | 2 h | Scaffold app, add route group and nested layout |
| Navigation and loading | Link, prefetch, loading.tsx, Suspense | [Linking and navigating](https://nextjs.org/docs/app/getting-started/linking-and-navigating), [loading.js](https://nextjs.org/docs/app/api-reference/file-conventions/loading), [Streaming guide](https://nextjs.org/docs/app/guides/streaming) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Add skeletons and measure perceived load |
| Server vs Client Components | Boundary, props, providers, server-only | [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components), [use client](https://nextjs.org/docs/app/api-reference/directives/use-client), [React Server Components](https://react.dev/reference/rsc/server-components) | No video verified for this topic; use the official documentation above. | Intermediate | 3 h | Convert a client-heavy page to server + small islands |
| Rendering, PPR, Cache Components | Static shell, streaming, use cache, cacheLife | [Caching](https://nextjs.org/docs/app/getting-started/caching), [cacheComponents](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents), [use cache](https://nextjs.org/docs/app/api-reference/directives/use-cache), [Instant navigation](https://nextjs.org/docs/app/guides/instant-navigation) | [Next.js Explained: Partial Prerendering (PPR)](https://www.youtube.com/watch?v=MTcPrTIBkpA) (Delba, English, about 10 min per Next.js docs, not independently verified); [Next.js 16: Master Partial Pre-rendering & Cache Components in 24 Minutes](https://www.youtube.com/watch?v=WJn1rXesTtg) (Clerk, English, "24 minutes" is from the title only); Hindi: [Next.js 16 caching, detailed explanation in Hindi](https://www.youtube.com/watch?v=gqZLb6zDJaQ) (Coder's Gyan, Hindi per title, duration not verified) | Intermediate | 4 h | Make a page with static shell, cached block and streamed block |
| Previous caching model | Why old tutorials differ | [Caching and Revalidating (Previous Model)](https://nextjs.org/docs/app/guides/caching-without-cache-components), [Migrating to Cache Components](https://nextjs.org/docs/app/guides/migrating-to-cache-components) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Map 5 old snippets to the new APIs |
| Data fetching | Server fetch, parallel, React.cache, use() | [Fetching data](https://nextjs.org/docs/app/getting-started/fetching-data), [cache (React)](https://react.dev/reference/react/cache), [Revalidating](https://nextjs.org/docs/app/getting-started/revalidating) | No video verified for this topic; use the official documentation above. | Intermediate | 2.5 h | Convert a sequential waterfall into parallel + Suspense |
| Server Functions, forms, mutations | use server, FormData, updateTag, revalidateTag | [Mutating data](https://nextjs.org/docs/app/getting-started/mutating-data), [Server Actions guide](https://nextjs.org/docs/app/guides/server-actions), [Forms guide](https://nextjs.org/docs/app/guides/forms), [Server Functions (React)](https://react.dev/reference/rsc/server-functions), [Data security](https://nextjs.org/docs/app/guides/data-security) | [Using Forms in Next.js (Server Actions, Revalidating Data)](https://www.youtube.com/watch?v=dDpZfOQBMaU) (leerob channel, English, duration and exact Next.js version not verified; may predate updateTag and the Next.js 16 changes) | Intermediate | 3 h | Create/delete order with Zod, auth check, revalidation |
| Route Handlers | GET/POST, webhooks, caching | [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers), [route.js reference](https://nextjs.org/docs/app/api-reference/file-conventions/route) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Build /api/health and a signed webhook receiver |
| Authentication | Sessions, cookies, DAL, proxy | [Authentication guide](https://nextjs.org/docs/app/guides/authentication), [proxy.js](https://nextjs.org/docs/app/api-reference/file-conventions/proxy) | [Next.js App Router Authentication (Sessions, Cookies, JWTs)](https://www.youtube.com/watch?v=DJvM2lSPn6w) (leerob channel, English, about 11 min per Next.js docs, not independently verified; likely uses the old middleware name) | Intermediate | 4 h | Login, cookie session, DAL, role-gated page |
| Metadata and images | generateMetadata, next/image, fonts | [Metadata and OG images](https://nextjs.org/docs/app/getting-started/metadata-and-og-images), [generateMetadata](https://nextjs.org/docs/app/api-reference/functions/generate-metadata), [Images](https://nextjs.org/docs/app/getting-started/images), [Image component](https://nextjs.org/docs/app/api-reference/components/image) | No video verified for this topic; use the official documentation above. | Beginner to intermediate | 1.5 h | Add dynamic titles and an OG image |
| Errors and not-found | error.tsx, not-found.tsx | [Error handling](https://nextjs.org/docs/app/getting-started/error-handling), [error.js](https://nextjs.org/docs/app/api-reference/file-conventions/error), [not-found.js](https://nextjs.org/docs/app/api-reference/file-conventions/not-found) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Trigger and reset a segment error |
| Env vars, deployment, performance | NEXT_PUBLIC_, build, checklist | [Environment variables](https://nextjs.org/docs/app/guides/environment-variables), [Deploying](https://nextjs.org/docs/app/getting-started/deploying), [Production checklist](https://nextjs.org/docs/app/guides/production-checklist), [Self-hosting](https://nextjs.org/docs/app/guides/self-hosting), [Vercel + Next.js](https://vercel.com/docs/frameworks/nextjs) | No video verified for this topic; use the official documentation above. | Intermediate | 2.5 h | Deploy; run Lighthouse; fix the top 2 issues |
| URL state, search, pagination | useSearchParams, debounce, Zod | [useSearchParams](https://nextjs.org/docs/app/api-reference/functions/use-search-params), [Zod](https://zod.dev/) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | URL-driven table with search, filter, sort, page |
| Testing in Next.js | Vitest/RTL, e2e for async components | [Next.js testing guide](https://nextjs.org/docs/app/guides/testing), [Playwright](https://playwright.dev/docs/intro) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | One Playwright test for login and the orders table |

## Verification notes

- Next.js pages marked as read in full or in summary on 2026-10-09: upgrade guide to version 16, Caching, Mutating Data, Installation, Fetching Data, Authentication guide, Server and Client Components, proxy.js, Migrating to Cache Components, and the testing guide section on async Server Components. All other nextjs.org, react.dev, vendor and library links in the table returned HTTP 200 but I did not read them end to end.
- YouTube: same limitation as Phase 4. youtube.com could not be reached from the authoring machine, so oEmbed via YouTube and `lengthSeconds` could not be fetched. Title and channel were confirmed through the noembed.com mirror for: "Next.js Explained: Partial Prerendering (PPR)" by Delba; "Next.js 16: Master Partial Pre-rendering & Cache Components in 24 Minutes" by Clerk; "I Can't Believe Next.js 16 did This With Caching! Detailed Explanation in Hindi | Day 53/100" by Coder's Gyan; "Using Forms in Next.js (Server Actions, Revalidating Data)" by leerob; "Next.js App Router Authentication (Sessions, Cookies, JWTs)" by leerob.
- The "10 minutes" and "11 minutes" durations come from the Next.js docs pages that link those two videos; I did not confirm them. No other duration is claimed. Language "English" is assumed from the titles and channels; only the Coder's Gyan video states "Hindi" in its title.
- Outdated risk: the auth and forms videos are older than the Next.js 16 release (they likely show `middleware.ts`, sync `cookies()`, and possibly `useFormState`). Use them for concepts only and copy code from the current docs.
- I did not find, and so do not recommend, a complete verified Next.js 16 course. A Hindi playlist ("Chai aur full stack NextJS") appeared in search, but its title could not be verified via oEmbed (playlist lookup failed), so it is not included.

## Hands-on exercises

1. **Fresh app audit.** Run `npx create-next-app@latest` with defaults. Read `next.config.ts` and `AGENTS.md`. List which features are on (Cache Components, Turbopack) and which are off (React Compiler).
2. **Route anatomy.** Build `/dashboard` with a nested layout, a `(marketing)` route group, `[id]` dynamic route, `loading.tsx`, `error.tsx` (force an error), and `not-found.tsx` (call `notFound()`).
3. **Boundary drill.** Build a product list as a Server Component and a "Add to wishlist" button as a Client Component island. Check the Network tab to confirm component JS only loads for the island.
4. **Three kinds of content.** On one page show (a) static text, (b) a `use cache` block with `cacheLife("minutes")` and `cacheTag`, (c) a block reading `cookies()` inside Suspense. Use the dev overlay to confirm which part is in the static shell.
5. **Waterfall fix.** Create two slow data functions (500 ms each). Show the sequential version (1 s), the `Promise.all` version, and the two-Suspense-boundaries version. Record timings.
6. **Mutation flow.** Create an order via Server Action with Zod validation and `useActionState`. After success call `updateTag` and `redirect`. Then call the same action with `curl` while logged out and confirm it is rejected.
7. **Auth.** Implement a cookie session with `jose`, a DAL (`verifySession`, `getUser`), `proxy.ts` optimistic redirect, and a role check in the DAL. Prove that deleting the `proxy.ts` file does not expose data.
8. **URL table.** Build a table where search, status filter, sort and page are in the URL, debounced, validated by Zod, with pending UI via `useTransition`.
9. **Upgrade drill.** Take a snippet from an old tutorial (sync `params`, `fetch` with `next: { revalidate }`, `middleware.ts`) and port it to Next.js 16 using the upgrade and migration guides.
10. **Deploy and measure.** Deploy to Vercel, run Lighthouse on mobile, and write down LCP, INP, CLS and one fix.

## Checkpoint

- **Explain:** (a) Server vs Client Component and where the boundary is; (b) what goes into the static shell and what streams; (c) `fetch` caching defaults today vs Next.js 14; (d) why Server Functions need their own auth checks; (e) what `proxy.ts` is for and not for.
- **Modify code:** Convert a sequential data page to parallel with Suspense; convert `middleware.ts` to `proxy.ts`; change `revalidateTag("x")` to the new signature; add `await` to a sync `params` usage.
- **Debug:** A page shows stale orders after creating one. List three causes (missing `updateTag`/`revalidateTag`, cached with long `cacheLife`, client router cache) and how you would verify each. A build fails with a "blocking route" insight: find the uncached read and wrap or cache it.
- **Write tests:** One RTL test for the search box (typing updates the URL via a mocked router) and one Playwright test for the protected route redirect.

**Ready to move on when** you have a deployed Next.js app with auth, a mutation, a URL-driven table, error and not-found pages, and you can explain every route's rendering mode in one sentence without guessing.


# Weeks 5 and 6 — Study plan for Phases 4 and 5

## Week plan

*Calendar assumption: 8 to 10 hours per week next to a full-time job. Week 5 covers Phase 4 (React gaps) and the first half of Phase 5. Week 6 covers the second half of Phase 5 and builds Project 1. Both weeks assume Weeks 1 to 4 are done (JavaScript, TypeScript, HTML/CSS/HTTP basics).*

### Week 5 — React deep gaps and Next.js App Router start (estimated hours: 9)

**Learning objectives**
- Explain render, commit, re-render triggers and state snapshots without notes.
- Use keys, effects, cleanup and memoization correctly, and know when not to use them.
- Choose where state should live (local, lifted, URL, server-state, context, store).
- Scaffold a Next.js 16 app and explain its folder, routing, layout and Server/Client Component model.

**Topics and subtopics** (in recommended order)
1. **[Must learn now]** Render model, state as snapshot, re-render triggers (Phase 4).
2. **[Must learn now]** Keys, reconciliation, state reset with `key`.
3. **[Must learn now]** Effects, cleanup, dependencies, "You Might Not Need an Effect", `useEffectEvent`.
4. **[Must learn now]** Forms, controlled vs uncontrolled, React 19 Actions (`useActionState`, `useOptimistic`).
5. **[Must learn now]** Context, state-placement decisions, error boundaries, custom hooks, folder structure.
6. **[Must learn now]** Data fetching states (loading/error/empty/success), cancellation, TanStack Query overview.
7. **[Must learn now]** Memoization, when NOT to memoize, React Compiler overview; testing with RTL.
8. **[Must learn now]** Next.js setup, folder structure, routes, layouts, dynamic segments, navigation, `loading.tsx` (Phase 5, Next.js-specific).
9. **[Must learn now]** Server vs Client Components and the `"use client"` boundary (first look).
10. **[Learn later if needed]** Parallel and intercepting routes, `useDeferredValue`, `<Activity>`, React Compiler setup.

**Small prerequisite concepts**
- What a pure function is (Phase 1) and what a TypeScript discriminated union is (Phase 2).
- The browser event loop and what `fetch` returns (Phase 1).
- How HTML forms submit and what `FormData` is (Phase 3).
- Basic terminal and Node 20.9 or newer installed (Phase 0).

**Reading**
- [Render and Commit](https://react.dev/learn/render-and-commit), [State as a Snapshot](https://react.dev/learn/state-as-a-snapshot), [Preserving and Resetting State](https://react.dev/learn/preserving-and-resetting-state)
- [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect), [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects), [Separating Events from Effects](https://react.dev/learn/separating-events-from-effects)
- [React 19 release post](https://react.dev/blog/2024/12/05/react-19), [memo](https://react.dev/reference/react/memo), [React Compiler](https://react.dev/learn/react-compiler)
- [Next.js Installation](https://nextjs.org/docs/app/getting-started/installation), [Project structure](https://nextjs.org/docs/app/getting-started/project-structure), [Layouts and pages](https://nextjs.org/docs/app/getting-started/layouts-and-pages), [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)

**Video**
- [Mastering React's useEffect](https://www.youtube.com/watch?v=dH6i3GurZW8), Jack Herrington, English, duration not verified.
- [React Reset Component State With the Key Prop](https://www.youtube.com/watch?v=pu-FjumEY94), Coding in Flow, English, duration not verified.
- [Exploring React Performance](https://www.youtube.com/watch?v=uAmRtE52mYk), React Conf, English, duration not verified.
- Optional Hindi: [How React works under the Hood (reconciliation, diffing, key)](https://www.youtube.com/watch?v=UKn4aVlnB9A), Coder Army, language not verified from title, duration not verified.

**Hands-on exercises**
1. Do Phase 4 exercises 1 (re-render lab), 2 (key bug), 3 (effect audit) and 4 (cancelable fetch).
2. Do Phase 4 exercise 5 (form with Actions) and exercise 8 (six RTL tests).
3. Write a one-page "where does this state live?" table for 8 pieces of state in your current work app.
4. Do Phase 5 exercises 1, 2 and 3 (fresh app audit, route anatomy, boundary drill).
5. Sunday revision: close the editor and re-explain render vs commit and the three re-render triggers to a rubber duck (or to Claude as an interviewer, see the interview-practice prompt in the AI workflow section of the handbook).

**What you must build**
A small "Notes" mini-app in Next.js 16 with TypeScript: a nested dashboard layout, a `[id]` detail route with `loading.tsx`, `error.tsx` and `not-found.tsx`, a server-rendered list, and one Client Component island (search or like button). Include 6 RTL tests (Phase 4 exercise 8). Commit it to GitHub with a short README.

**Completion checklist**
- [ ] I can explain trigger, render and commit in my own words.
- [ ] I fixed an index-key bug and a stale-response race.
- [ ] I removed at least 3 unnecessary effects in a real or sample codebase.
- [ ] I can say when NOT to use `useMemo`/`useCallback`/`memo`.
- [ ] I wrote a form with `useActionState` and accessible errors.
- [ ] I have the state-placement table.
- [ ] I scaffolded a Next.js 16 app and know what each file in `app/` does.
- [ ] I can explain the `"use client"` boundary and show an island in the Network tab.
- [ ] Six RTL tests pass; `npm run lint` and `tsc --noEmit` are clean.

**Self-test**
1. A parent re-renders and its child receives identical props. Does the child re-render? How do you stop it, and should you?
2. Why does an effect run twice in development, and what does that tell you?
3. When is `key={index}` safe? Show a bug when it is not.
4. What is the difference between a Server Component and a Client Component, and what does "use client" mark?
5. In Next.js 16 how do you read `params` in a page?

**Common mistakes**
- Skipping Phase 4 because "I know React" and then failing interviews on keys and effects.
- Marking the root layout or whole pages `"use client"`.
- Copying a Next.js tutorial from 2023 (Pages Router, sync `params`).
- Memoizing before measuring.
- Spending the whole week on reading and writing no code.

**Ready to continue when**
You pass the Phase 4 checkpoint, your Notes app runs with the route files above, and you can explain, route by route, which components are server and which are client and why.

**Slower-track option**
Spread Phase 4 over Week 5 and Phase 5 setup/routing over a second week. Cut: optional Hindi video, `useOptimistic`, error boundaries (keep Next.js `error.tsx`), Compiler reading. Keep: re-render lab, key bug, effect audit, Notes app. Your overall calendar then shifts by one week; protect Project 1 because it is your first portfolio piece.


### Week 6 — Next.js finish and Project 1: Admin dashboard (estimated hours: 10)

**Learning objectives**
- Fetch, cache and stream data with the current Next.js 16 model (Cache Components) and explain every cache decision.
- Build mutations with Server Functions, validate on the server, revalidate with `updateTag`/`revalidateTag`.
- Implement cookie-session auth with a Data Access Layer and `proxy.ts`.
- Put list state in the URL (search, filter, sort, pagination) and handle loading, error and empty states.
- Test, deploy and measure a real app (Project 1 below).

**Topics and subtopics** (in recommended order)
1. **[Must learn now]** Rendering model: static shell, streaming, PPR; `use cache`, `cacheLife`, `cacheTag`.
2. **[Must learn now]** Data fetching: parallel, waterfalls, `React.cache`, Suspense boundaries.
3. **[Must learn now]** Server Functions, forms, `updateTag`, `revalidateTag`, `redirect`.
4. **[Must learn now]** Route Handlers (the mock API) and when to use them.
5. **[Must learn now]** Authentication: session cookie, DAL, DTOs, `proxy.ts`.
6. **[Must learn now]** Metadata, `next/image`, `error.tsx`, `not-found.tsx`, environment variables.
7. **[Must learn now]** URL state for search, filters, sort and pagination.
8. **[Must learn now]** Deploy to Vercel; Lighthouse; production checklist.
9. **[Learn during projects]** TanStack Query for one client-driven widget; Playwright smoke test.
10. **[Learn later if needed]** Docker/self-hosting (Phase 15), ISR with Cache Components, `use cache: remote`, parallel/intercepting routes.

**Small prerequisite concepts**
- Cookies: `HttpOnly`, `Secure`, `SameSite` (Phase 3).
- What a JWT is and why not to put PII in it (you will deepen this in Phase 6).
- Zod basics: `object`, `string`, `coerce.number`, `safeParse`.
- HTTP status codes: 200, 201, 400, 401, 403, 404, 422.

**Reading**
- [Caching](https://nextjs.org/docs/app/getting-started/caching), [Fetching Data](https://nextjs.org/docs/app/getting-started/fetching-data), [Revalidating](https://nextjs.org/docs/app/getting-started/revalidating)
- [Mutating Data](https://nextjs.org/docs/app/getting-started/mutating-data), [Server Actions guide](https://nextjs.org/docs/app/guides/server-actions), [Data security](https://nextjs.org/docs/app/guides/data-security)
- [Authentication guide](https://nextjs.org/docs/app/guides/authentication), [proxy.js](https://nextjs.org/docs/app/api-reference/file-conventions/proxy)
- [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers), [Environment variables](https://nextjs.org/docs/app/guides/environment-variables), [Production checklist](https://nextjs.org/docs/app/guides/production-checklist)
- [Upgrading to version 16](https://nextjs.org/docs/app/guides/upgrading/version-16) (skim the breaking changes) and [Migrating to Cache Components](https://nextjs.org/docs/app/guides/migrating-to-cache-components) (skim the first half)

**Video**
- [Next.js Explained: Partial Prerendering (PPR)](https://www.youtube.com/watch?v=MTcPrTIBkpA), Delba, English, about 10 minutes per the Next.js docs, not independently verified.
- [Next.js 16: Master Partial Pre-rendering & Cache Components in 24 Minutes](https://www.youtube.com/watch?v=WJn1rXesTtg), Clerk, English, duration from title only.
- [Next.js App Router Authentication (Sessions, Cookies, JWTs)](https://www.youtube.com/watch?v=DJvM2lSPn6w), leerob, English, about 11 minutes per the Next.js docs, not independently verified. May show older API names; follow the docs.
- Optional Hindi: [Next.js 16 caching, detailed explanation in Hindi](https://www.youtube.com/watch?v=gqZLb6zDJaQ), Coder's Gyan, Hindi per title, duration not verified.

**Hands-on exercises**
1. Phase 5 exercises 4 (three kinds of content), 5 (waterfall fix), 6 (mutation flow) and 7 (auth).
2. Phase 5 exercise 8 (URL table), which becomes the core of Project 1.
3. Phase 5 exercise 9 (port old snippets to Next.js 16).
4. Build Project 1 milestones M0 to M8 (see below). Milestone M9 (polish) and the advanced list are optional.

**What you must build**
Project 1: the "OpsBoard" admin dashboard (specification below), deployed to Vercel with a README, at least 15 automated tests, and a Lighthouse score noted in the README.

**Completion checklist**
- [ ] I can explain what each route renders at build time vs request time.
- [ ] No data is fetched in `useEffect` where a Server Component would do.
- [ ] Every Server Function checks auth, role and input.
- [ ] Orders table works from the URL (page, q, status, sort) and survives refresh.
- [ ] Loading, error and empty states exist for every list and detail view.
- [ ] Project 1 acceptance criteria are met (see below); app deployed; README written.
- [ ] I can demo the project in 3 minutes and explain one trade-off.

**Self-test**
1. When do you use `updateTag` and when `revalidateTag`? What changed in `revalidateTag`'s signature?
2. Why is `proxy.ts` not enough to protect data?
3. What happens if you read `cookies()` outside a Suspense boundary under Cache Components?
4. Why keep the page number in the URL?
5. When would you choose a Route Handler instead of a Server Function?

**Common mistakes**
- Building the UI first and bolting auth on at the end.
- Copying `fetch` cache options from old articles.
- Using Server Functions for reads.
- Skipping empty and error states, then calling the project "done".
- Over-scoping Project 1 (charts, dark mode, drag-and-drop) before the MVP works.

**Ready to continue when**
Project 1's MVP acceptance criteria all pass, it is deployed with a README, you can answer the project interview questions below, and the Phase 5 checkpoint is done. Anything in the "advanced" list can wait; do not start Phase 6 late because of it.

**Slower-track option**
Treat Week 6 as two weeks: finish Phase 5 reading and exercises 4 to 9 first, then build Project 1 MVP only (milestones M0 to M6). Drop TanStack Query, Playwright and Lighthouse tuning until after Phase 6. Do not drop the auth, validation and tests: they are the point of the project.


# Project 1 — OpsBoard: Frontend Admin Dashboard

*Stack: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Zod. Mock REST API built with Route Handlers. This is a frontend-focused project: the "backend" is deliberately fake and replaceable. In Project 2 you will build the real Express API and point this dashboard at it.*

## Problem statement and real-world use case

A small online shop (think a Surat textile seller or a local electronics store) has orders, customers and products in spreadsheets. Staff lose time finding an order, checking its status or seeing today's totals. They need a private web dashboard where staff log in, see key numbers, search and filter orders, open an order, change its status, and manage customers and products. Managers can edit; viewers can only read. This is the classic internal "admin panel", one of the most common real tasks for a full-stack or frontend engineer.

## Requirements and user stories

Functional:
- As a staff member, I log in with email and password and am sent to the dashboard; if I am not logged in, protected pages send me to the login page.
- As a staff member, I see KPIs: orders today, revenue this week, pending orders, low-stock products.
- As a staff member, I see an orders table with search (order number or customer name), status filter, sort and pagination, and the state is kept in the URL.
- As a staff member, I open an order to see its items, customer and status history.
- As a manager, I can change an order's status (pending, paid, shipped, cancelled) and create or edit a customer or product with validated forms.
- As an admin, I can delete a customer who has no orders, with a confirmation dialog.
- As a viewer, I cannot see edit and delete controls, and direct attempts are rejected by the server.
- As any user, I see clear loading skeletons, a friendly empty state, and a clear error state with a retry.
- As a mobile user, I can use the table (cards or horizontal scroll) and the navigation (drawer).

Non-functional: responsive from 360 px, keyboard accessible, Lighthouse accessibility 90 or higher, no secrets in the client bundle, TypeScript strict, 15+ automated tests.

## MVP vs advanced

| MVP (must ship) | Advanced (after MVP) |
| --- | --- |
| Login, logout, cookie session, `proxy.ts` redirect, DAL | Refresh/rotating sessions, "remember me" |
| Roles: admin, manager, viewer enforced on the server | Per-resource permissions |
| Dashboard KPIs (cached with `use cache`) | Charts (revenue per day) with a lazy-loaded chart library |
| Orders table: search, status filter, sort, pagination via URL | Saved filters, CSV export, column visibility |
| Order detail page and status change (Server Action) | Optimistic status update with `useOptimistic` |
| Customers and products CRUD with Zod validation | Bulk actions, image upload for products |
| Loading, error, empty, not-found states | Skeletons matching real layout, toasts |
| 15+ tests, deployed on Vercel, README | Playwright e2e in CI, dark mode, i18n, command palette |

## Suggested architecture

```text
Browser
  |  navigates (HTML + RSC stream)           posts forms (Server Functions)
  v
Next.js app (Vercel or Node)
  proxy.ts                 optimistic redirect if no session cookie
  Server Components        pages call lib/data (DAL) directly
  Client Components        table toolbar, forms, dialogs, mobile nav
  Server Functions         create/update/delete + auth + Zod + updateTag
  lib/dal.ts               verifySession(), requireRole(), getUser()
  lib/api/                 typed client for the REST API (fetch + Zod parse)
  app/api/**/route.ts      MOCK REST API (in-memory seed data)
        ^
        |  later: swap API_BASE_URL to the real Express API (Project 2)
```

Key decisions to write in your README:
1. Read data in Server Components through the typed client and the DAL; use Server Functions only for writes.
2. The mock API is a separate layer with its own Zod-validated contract, so replacing it later is a one-line env change.
3. Cache what is shared and slow (KPIs) with `use cache`, tagged `stats`; never cache per-user data in a shared cache.
4. State placement: URL for table state, local state for dialogs, Server Components for server data, no global store.

## Folder structure

```text
opsboard/
  app/
    (auth)/login/page.tsx            login form (useActionState)
    (app)/
      layout.tsx                     shell: sidebar, header, user menu
      dashboard/page.tsx             KPI cards in Suspense
      orders/
        page.tsx                     table (reads searchParams)
        loading.tsx  error.tsx
        [id]/page.tsx  [id]/not-found.tsx
      customers/ page.tsx, new/page.tsx, [id]/edit/page.tsx
      products/  page.tsx, new/page.tsx, [id]/edit/page.tsx
    api/                             MOCK API route handlers
      auth/login/route.ts            (optional; login may call the DAL directly)
      orders/route.ts, orders/[id]/route.ts
      customers/route.ts, customers/[id]/route.ts
      products/route.ts, products/[id]/route.ts
      stats/route.ts
    layout.tsx  globals.css  not-found.tsx
  components/
    ui/        Button, Input, Select, Dialog, Table, Badge, Skeleton, Pagination
    orders/    OrdersTable, OrdersToolbar (client), StatusBadge, StatusForm
    customers/ CustomerForm   products/ ProductForm
  lib/
    dal.ts            server-only: verifySession, requireRole
    session.ts        server-only: sign/verify cookie with jose
    api/              client.ts, orders.ts, customers.ts, products.ts, stats.ts
    schemas/          order.ts, customer.ts, product.ts, query.ts (Zod)
    mock/             db.ts (in-memory), seed.ts
    env.ts            validates process.env with Zod
    utils.ts          cn(), formatCurrency(), formatDate()
  actions/            orders.ts, customers.ts, products.ts, auth.ts ("use server")
  proxy.ts
  tests/              unit/, components/, e2e/
  next.config.ts  vitest.config.ts  .env.example  README.md
```

Why each folder exists: `components/ui` holds reusable primitives with no business logic; feature folders hold feature UI; `lib/schemas` is the single source of truth for types and validation (derive TS types with `z.infer`); `actions` keeps all mutations in one auditable place; `lib/dal.ts` is the only place that reads the session.

## Data model (schema and entities)

The data lives in memory behind the mock API, but design it like a real database (you will build it in Phase 7 and Project 2).

| Entity | Fields | Notes |
| --- | --- | --- |
| StaffUser | id, email (unique), name, role (admin, manager, viewer), passwordHash | Seed 3 users, one per role. Hash with a real algorithm even in mock (for example `bcryptjs`) |
| Customer | id, name, email (unique), phone, city, createdAt | Delete only if no orders |
| Product | id, sku (unique), name, priceCents (integer), stock, createdAt | Money as integer cents |
| Order | id, number (unique, e.g. ORD-1001), customerId, status, totalCents, createdAt, updatedAt | Status machine below |
| OrderItem | id, orderId, productId, qty, unitPriceCents | Price copied at purchase time |
| OrderStatusEvent | id, orderId, from, to, byUserId, at | Powers the history list |

Relationships: Customer 1-N Order; Order 1-N OrderItem; Product 1-N OrderItem (so Order and Product are M-N through OrderItem); Order 1-N OrderStatusEvent; StaffUser 1-N OrderStatusEvent.

Allowed status transitions: pending to paid or cancelled; paid to shipped or cancelled; shipped is final; cancelled is final. Enforce this in the API and show only valid next actions in the UI. Seed about 200 orders, 60 customers, 40 products so pagination and search are meaningful.

## API endpoints (mock REST contract)

All JSON. All except login require a valid session. Errors use one shape: `{ "error": { "code": "VALIDATION", "message": "...", "fields": { "email": "Invalid" } } }`.

| Method and path | Purpose | Roles | Notes |
| --- | --- | --- | --- |
| POST /api/auth/login | Verify credentials | public | 401 on bad credentials, same message for unknown email and wrong password |
| GET /api/stats | KPI numbers | all | Cacheable |
| GET /api/orders | List | all | Query: page, pageSize (max 50), q, status, sort (createdAt, -createdAt, totalCents, -totalCents). Returns `{ items, total, page, pageSize }` |
| GET /api/orders/:id | Detail with items and history | all | 404 if missing |
| PATCH /api/orders/:id/status | Change status | admin, manager | 409 on invalid transition |
| GET /api/customers | List | all | Same query style |
| POST /api/customers | Create | admin, manager | 422 on validation error, 409 on duplicate email |
| PATCH /api/customers/:id | Update | admin, manager | |
| DELETE /api/customers/:id | Delete | admin | 409 if customer has orders |
| GET, POST /api/products and PATCH /api/products/:id | List, create, update | read: all, write: admin, manager | |

Optional: for read-only practice data you can also point the list views at the public [DummyJSON](https://dummyjson.com/docs) API, which I confirmed returns paginated, searchable `users` and `products` (`limit`, `skip`, `q` search, `sortBy`, `order`). It does not know your auth or your orders, so use it only as an extra data source for an advanced exercise.

## Packages and setup

```bash
npx create-next-app@latest opsboard --yes
cd opsboard
npm i zod jose bcryptjs clsx tailwind-merge server-only
npm i -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/user-event \
  @testing-library/jest-dom msw @types/bcryptjs
# optional: npm i @tanstack/react-query ; npm i -D @playwright/test
```

Notes:
- Check the `package.json` that `create-next-app` produced; do not downgrade `next`, `react` or `react-dom`.
- Add scripts: `"test": "vitest"`, `"typecheck": "tsc --noEmit"`, `"lint": "eslint"`. Next.js 16 does not lint during `next build`, so CI must run lint, typecheck, test and build separately.
- Env: `SESSION_SECRET` (generate with `openssl rand -base64 32`), `API_BASE_URL` (for example `http://localhost:3000/api` locally). Commit `.env.example`, never `.env.local`.
- UI primitives: write your own small `components/ui` set, or copy from [shadcn/ui](https://ui.shadcn.com/docs). For tables with sorting you may study [TanStack Table](https://tanstack.com/table/latest), but a server-driven table needs very little code, so do not add it for the MVP.
- Install and configure ESLint with the Next.js config and `eslint-plugin-jsx-a11y`.

## Implementation milestones

| # | Milestone | What "done" looks like | Est. time |
| --- | --- | --- | --- |
| M0 | Setup | App runs, strict TS, lint and test scripts work, repo and `.env.example` committed, README skeleton | 0.5 h |
| M1 | Shell and design system | Root layout, sidebar/drawer nav, `components/ui` primitives, responsive at 360 px | 1 h |
| M2 | Mock API and schemas | Seed data, route handlers for all endpoints, Zod schemas, typed client that parses responses | 1.5 h |
| M3 | Auth | Login form with `useActionState`, jose cookie session, `verifySession`, `proxy.ts`, logout, role helper | 1.5 h |
| M4 | Orders list | URL-driven table: q (debounced), status, sort, page; Suspense skeleton, empty and error states | 2 h |
| M5 | Order detail and status change | Dynamic route, `notFound()`, Server Function with role check and valid-transition rule, `updateTag` | 1 h |
| M6 | Customers and products CRUD | Zod-validated forms, field-level errors, delete with confirm dialog, role-gated controls | 1.5 h |
| M7 | Dashboard KPIs and caching | KPIs with `use cache`, `cacheLife`, `cacheTag("stats")`; status change invalidates stats | 0.75 h |
| M8 | Tests, accessibility, deploy | 15+ tests, keyboard pass, Vercel deploy, Lighthouse, README finished | 1.5 h |
| M9 | Polish (optional) | Optimistic UI, toasts, charts, Playwright, dark mode | open |

The sum of M0 to M8 is about 11 hours, slightly above one week. Budget by starting M0 to M2 at the end of Week 5 if you can, or use the slower-track plan. Teach yourself in small steps: finish each milestone with a commit and a working demo before the next.

Per-milestone tips:
- **M2:** write the Zod schema first, then the route handler, then the client function. Types flow from schemas (`z.infer`). Validate query params and bodies in the handlers; respond with the error shape above.
- **M3:** keep all cookie code in `lib/session.ts`; set `httpOnly`, `secure` (in production), `sameSite: "lax"`, a 7-day expiry; payload only has `userId`, `role`, `exp`. `proxy.ts` only checks the cookie exists and decodes; the DAL does the real check on each data read.
- **M4:** in `orders/page.tsx` keep the page itself synchronous and non-blocking; put the `await searchParams` and data fetch in a child component inside `<Suspense>` so the heading and filters render immediately. Parse query with a Zod schema that has defaults and a whitelist for `sort`. When any filter changes, reset `page` to 1.
- **M5:** the status Server Function re-checks the role, loads the order, validates the transition, writes the change and event, then calls `updateTag("stats")` and revalidates the order. Return `{ ok: false, message }` for expected errors.
- **M7:** only cache shared data. KPIs are the same for everyone, so `use cache` is safe. A "my recent orders" widget is user-specific, so do not put it inside a shared `use cache` function without the user id in the arguments.

## Test cases

Unit tests (Vitest):
- `formatCurrency(1999)` returns the expected string; `cn()` merges classes.
- Query schema: defaults applied, `pageSize` capped at 50, invalid `sort` rejected, `page=abc` falls back or errors as designed.
- Status transition function allows pending to paid and rejects shipped to pending.
- Order, customer and product Zod schemas: valid and invalid cases (negative price, bad email, empty name).
- Session helper: valid token verifies; tampered or expired token is rejected.

Component tests (React Testing Library + user-event + MSW):
- Login form shows field errors for empty input and a general error for bad credentials; button disabled while pending.
- OrdersTable renders rows from a fixture; shows the empty state when `items` is empty; shows the error state with a retry on a 500.
- OrdersToolbar: typing in search updates the URL (mocked router) after the debounce; changing the status filter resets page to 1.
- CustomerForm: validation messages are tied to inputs (`aria-describedby`); server `fields` errors render under the right inputs.
- Delete dialog traps focus, closes on Escape, and only calls the action after confirm.
- Viewer role: edit and delete buttons are not rendered.

Server logic tests:
- Server Function rejects a request without a session; rejects a viewer; rejects invalid input; accepts a valid manager request (call the function directly with a mocked session).
- Route handlers: 401 without session, 403 for wrong role, 404 missing id, 409 on invalid transition, 422 on invalid body.

Optional e2e (Playwright): log in as manager, filter orders by `paid`, open one, change status to `shipped`, see the history entry; log in as viewer and confirm no edit controls; visit `/dashboard` logged out and land on `/login`. The Next.js testing guide recommends end-to-end tests over unit tests for async Server Components, which is why the table and page-level behavior is covered here rather than by unit-rendering async pages.

## Security checklist (prioritized)

1. **Server-side authorization on every Server Function and Route Handler** (role plus ownership). The UI hiding a button is cosmetics.
2. **Validate all input with Zod** on the server: bodies, form data, and query params (whitelist `sort`, cap `pageSize`).
3. **Session cookie:** `HttpOnly`, `Secure`, `SameSite=Lax`, short expiry, secret in env, minimal payload, no PII in the token.
4. **DAL pattern:** one `verifySession()` used by all reads and writes; return DTOs with only needed fields (never `passwordHash`).
5. **`proxy.ts` is a convenience redirect only**, not the security boundary.
6. **No secrets in client code:** only `NEXT_PUBLIC_` values reach the browser; use `import "server-only"` in `lib/dal.ts`, `lib/session.ts` and `lib/mock/db.ts`.
7. **Password handling:** hash with bcrypt (cost 10 or more); generic login error message; basic rate limiting on login (simple in-memory counter is fine for the mock; real limiter in Project 2).
8. **XSS:** never use `dangerouslySetInnerHTML` with user data; React escapes by default.
9. **CSRF:** Server Actions are POST-only and rely on SameSite cookies plus Origin checks done by the framework; do not add GET endpoints that mutate.
10. **Error handling:** generic messages to the client, details only in server logs.
11. **Dependencies:** run `npm audit`; commit the lockfile; keep Next.js on a patched version.
12. **Headers:** review security headers (CSP, frame options) in the Next.js docs when you deploy; a strict CSP is an advanced item.

## Deployment plan

1. Push to GitHub. Make sure `npm run lint`, `npm run typecheck`, `npm test` and `npm run build` pass locally.
2. Create a Vercel project from the repo (see [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs) and the [Next.js deployment options](https://nextjs.org/docs/app/getting-started/deploying)). Framework preset: Next.js.
3. Add env vars in the Vercel dashboard: `SESSION_SECRET`, `API_BASE_URL` (your deployed URL plus `/api`).
4. Deploy a preview, test login and the critical flows, then promote to production.
5. Be honest about the mock: in-memory data resets when serverless instances restart. Write that in the README. (Project 2 and Phase 7 replace this with a real database.)
6. Run Lighthouse on the dashboard and orders pages (mobile). Record LCP, INP, CLS and one fix you made.
7. Add a GitHub Actions workflow with lint, typecheck, test, build (you will formalize CI/CD in Phase 15).
8. Rollback plan: keep the previous deployment; use "promote previous deployment" if a release breaks login.

## README structure

1. Title, one-sentence description, screenshot or GIF, live URL.
2. Features (MVP list) and roles with demo credentials (clearly marked as fake).
3. Tech stack and why (Next.js 16, TS, Tailwind, Zod, jose).
4. Architecture diagram (text) and key decisions (reads vs writes, caching, state placement).
5. Getting started: prerequisites (Node 20.9+), install, env vars table, run, test.
6. Project structure.
7. API contract summary and status codes.
8. Testing approach and how to run it.
9. Security notes (what is enforced where).
10. Performance notes (Lighthouse numbers, caching choices).
11. Known limitations (mock data resets, no real DB) and roadmap.

## Acceptance criteria

- [ ] Logging in as admin, manager and viewer works; wrong password shows a generic error; logout clears the cookie.
- [ ] Visiting any app route while logged out redirects to `/login`; deleting `proxy.ts` still does not expose data (the DAL blocks it).
- [ ] The orders table supports search, status filter, sort and pagination from the URL; refresh and back/forward keep the state; changing a filter resets to page 1.
- [ ] A bad `?sort=` or `?page=-5` does not crash the page (validated fallback).
- [ ] Order detail shows items and history; unknown id shows the not-found page.
- [ ] Manager can change status only along valid transitions; viewer attempting the action via a direct request gets a 403-style rejection.
- [ ] Customer and product forms validate on server and client, show field errors accessibly, and a duplicate email shows a clear message.
- [ ] Every list has loading, empty and error states; error state has a retry.
- [ ] KPIs are cached with a documented `cacheLife` and update after a status change.
- [ ] No page is a Client Component at the top level without a reason documented in the README.
- [ ] Usable at 360 px and with keyboard only; Lighthouse accessibility 90 or higher.
- [ ] 15+ automated tests pass; lint and typecheck are clean; the app is deployed; the README is complete.

## Common mistakes

- Fetching table data in `useEffect` from a Client Component when a Server Component with Suspense is simpler and faster.
- Putting filter state in `useState` instead of the URL.
- Checking roles only in the UI.
- Trusting `searchParams` and form data without parsing them.
- Caching user-specific data in a shared `use cache`, or expecting `fetch` to be cached by default.
- Using `key={index}` in the table.
- Storing money as floating-point numbers.
- Forgetting to reset `page` when filters change.
- Marking the whole layout `"use client"` for a single dropdown.
- Following a 2023 tutorial (sync `params`, `middleware.ts`, `getServerSideProps`).
- No empty state: an empty search looks like a broken page.
- Starting with charts and animations before login, tables and tests work.
- Letting AI generate the whole project: you must be able to rebuild the orders table and the status Server Function from memory.

## Interview questions

1. Walk me through what happens when I open `/orders?status=paid&page=2` (server vs client, caching, streaming).
2. Why did you keep table state in the URL? What are the downsides?
3. Where is authorization enforced and why not only in `proxy.ts`?
4. A Server Function is a public endpoint. How did you secure it?
5. Explain your cache strategy. What is tagged, what invalidates it, and what must never be in a shared cache?
6. How would you handle 1 million orders? (Cursor pagination, indexes, server-side search, virtualization; see Phase 7 and 17.)
7. How did you avoid waterfalls on the dashboard page?
8. Why is `useEffect` rarely used in your project?
9. How did you test async Server Components, and what would you test differently?
10. What changes when the mock API is replaced by a real Express or FastAPI backend? What stays the same?
11. Why store money as integer cents?
12. What would you improve first with two more weeks?


## Sources

Documentation pages opened or fetched on 2026-10-09 (content read in full or in summary unless marked "status only"):

- https://nextjs.org/docs/app/guides/upgrading/version-16
- https://nextjs.org/docs/app/getting-started/caching
- https://nextjs.org/docs/app/getting-started/mutating-data
- https://nextjs.org/docs/app/getting-started/installation
- https://nextjs.org/docs/app/getting-started/fetching-data
- https://nextjs.org/docs/app/guides/authentication
- https://nextjs.org/docs/app/getting-started/server-and-client-components
- https://nextjs.org/docs/app/api-reference/file-conventions/proxy
- https://nextjs.org/docs/app/guides/migrating-to-cache-components
- https://nextjs.org/docs/app/guides/testing (async Server Components section)
- https://react.dev/blog/2024/12/05/react-19
- https://react.dev/blog/2025/10/01/react-19-2
- https://react.dev/learn/you-might-not-need-an-effect
- https://react.dev/reference/react/memo
- https://react.dev/reference/react/useEffectEvent
- https://react.dev/learn/react-compiler
- https://dummyjson.com/docs (endpoints tested with curl: users search, sortBy, products limit/select)

Links checked for HTTP 200 only (status only, not read end to end):

- https://nextjs.org/docs/app, https://nextjs.org/docs/app/getting-started/project-structure, https://nextjs.org/docs/app/getting-started/layouts-and-pages, https://nextjs.org/docs/app/getting-started/revalidating, https://nextjs.org/docs/app/getting-started/route-handlers, https://nextjs.org/docs/app/getting-started/metadata-and-og-images, https://nextjs.org/docs/app/getting-started/images, https://nextjs.org/docs/app/getting-started/error-handling, https://nextjs.org/docs/app/getting-started/deploying, https://nextjs.org/docs/app/getting-started/linking-and-navigating
- https://nextjs.org/docs/app/guides/environment-variables, https://nextjs.org/docs/app/guides/production-checklist, https://nextjs.org/docs/app/guides/self-hosting, https://nextjs.org/docs/app/guides/server-actions, https://nextjs.org/docs/app/guides/forms, https://nextjs.org/docs/app/guides/data-security, https://nextjs.org/docs/app/guides/streaming, https://nextjs.org/docs/app/guides/instant-navigation, https://nextjs.org/docs/app/guides/caching-without-cache-components
- https://nextjs.org/docs/app/api-reference/directives/use-cache, https://nextjs.org/docs/app/api-reference/directives/use-client, https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents, https://nextjs.org/docs/app/api-reference/file-conventions/loading, https://nextjs.org/docs/app/api-reference/file-conventions/error, https://nextjs.org/docs/app/api-reference/file-conventions/not-found, https://nextjs.org/docs/app/api-reference/file-conventions/route, https://nextjs.org/docs/app/api-reference/functions/generate-metadata, https://nextjs.org/docs/app/api-reference/functions/use-search-params, https://nextjs.org/docs/app/api-reference/components/image
- https://react.dev/learn/render-and-commit, https://react.dev/learn/state-as-a-snapshot, https://react.dev/learn/queueing-a-series-of-state-updates, https://react.dev/learn/rendering-lists, https://react.dev/learn/preserving-and-resetting-state, https://react.dev/learn/synchronizing-with-effects, https://react.dev/learn/removing-effect-dependencies, https://react.dev/learn/separating-events-from-effects, https://react.dev/learn/passing-data-deeply-with-context, https://react.dev/learn/scaling-up-with-reducer-and-context, https://react.dev/learn/choosing-the-state-structure, https://react.dev/learn/react-developer-tools
- https://react.dev/reference/react/useEffect, https://react.dev/reference/react/useMemo, https://react.dev/reference/react/useCallback, https://react.dev/reference/react/use, https://react.dev/reference/react/useActionState, https://react.dev/reference/react/Suspense, https://react.dev/reference/react/cache, https://react.dev/reference/react/Profiler, https://react.dev/reference/react-dom/components/form, https://react.dev/reference/rsc/server-components, https://react.dev/reference/rsc/server-functions
- https://testing-library.com/docs/react-testing-library/intro/, https://testing-library.com/docs/queries/about, https://testing-library.com/docs/user-event/intro, https://vitest.dev/guide/, https://mswjs.io/docs/, https://playwright.dev/docs/intro, https://zod.dev/, https://tanstack.com/query/latest, https://tanstack.com/table/latest, https://ui.shadcn.com/docs, https://www.w3.org/WAI/ARIA/apg/, https://vercel.com/docs/frameworks/nextjs

YouTube items (title and channel confirmed through the noembed.com oEmbed mirror because youtube.com was unreachable from the authoring machine; durations not verified):

- https://www.youtube.com/watch?v=MTcPrTIBkpA (Delba)
- https://www.youtube.com/watch?v=WJn1rXesTtg (Clerk)
- https://www.youtube.com/watch?v=gqZLb6zDJaQ (Coder's Gyan)
- https://www.youtube.com/watch?v=dDpZfOQBMaU (leerob)
- https://www.youtube.com/watch?v=DJvM2lSPn6w (leerob)
- https://www.youtube.com/watch?v=dH6i3GurZW8 (Jack Herrington)
- https://www.youtube.com/watch?v=NZJUEzn10FI (Web Dev Simplified)
- https://www.youtube.com/watch?v=pu-FjumEY94 (Coding in Flow)
- https://www.youtube.com/watch?v=UKn4aVlnB9A (Coder Army)
- https://www.youtube.com/watch?v=uAmRtE52mYk (React Conf)
- https://www.youtube.com/watch?v=8Xwq35cPwYg (Programming with Mosh)
