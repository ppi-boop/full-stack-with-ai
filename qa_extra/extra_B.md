## 6. React

### Rendering and reconciliation

**Q: What triggers a component to re-render?**
A: A state update to a new value, its parent re-rendering, or a change in a context value it reads. Changing a normal variable or `ref.current` does not trigger a render.

**Q: When a parent re-renders, do all its children re-render?**
A: Yes by default, even if their props did not change. Wrapping a child in `React.memo` makes React skip it when its props are shallow-equal.

**Q: What are the render phase and the commit phase?**
A: In the render phase React calls your components to work out the new UI, and this must be pure. In the commit phase React applies the changes to the DOM and then runs layout effects and effects.

**Q: Why must a component be pure during render?**
A: React may call it more than once, pause it or throw the result away (StrictMode, concurrent rendering). Fetching, mutating outside variables or touching the DOM belongs in event handlers or effects.

**Q: What does React compare when it diffs two trees?**
A: The element type and the key at each position. A different type unmounts the old subtree and loses its state, while the same type keeps the state and only updates props.

**Q: What is wrong with defining a component inside another component?**
A: Every render creates a new function, so React sees a new component type, remounts it and loses its state and input focus. Define components at module level and pass data as props.

**Q: How do you reset a component's state when an id prop changes?**
A: Give it a `key` based on that id, like `<Profile key={userId} />`. A new key makes React discard the old instance and create a fresh one.

### State updates and snapshots

**Q: What is automatic batching?**
A: React groups several state updates from the same tick into one re-render. Since React 18 this also works inside timeouts, promises and native event handlers, not only React events.

**Q: Why does `console.log(count)` right after `setCount(count + 1)` print the old value?**
A: State is a snapshot for each render. `setCount` schedules the next render, so the new value only appears there.

**Q: Output: `count` is 0 and a click handler calls `setCount(count + 1)` three times. What is `count` after the click?**
A: 1, because all three calls read the same snapshot value 0. Calling `setCount(c => c + 1)` three times gives 3.

### Hooks rules and built-in hooks

**Q: Why can't hooks be called inside `if`, loops or after an early `return`?**
A: React identifies each hook by the order it is called in, so the order must be identical on every render. A conditional call shifts later hooks onto the wrong state.

**Q: What is lazy initial state and when should you use it?**
A: `useState(() => readFromStorage())` runs the function only on the first render. `useState(readFromStorage())` calls it on every render and throws the result away, which wastes time if it is expensive.

**Q: `useEffect` vs `useLayoutEffect`?**
A: `useLayoutEffect` runs synchronously after DOM changes but before the browser paints, so use it to measure or position elements without flicker. `useEffect` runs after paint and is the default choice.

**Q: What is `useId` for?**
A: It creates a unique, stable id for linking labels and ARIA attributes (`htmlFor`, `aria-describedby`) that matches between server and client rendering. Do not use it as a list key.

**Q: Do two components that call the same custom hook share state?**
A: No. Each call gets its own independent state, so a custom hook shares logic, not data. To share data use props, context or a store.

**Q: What does the `react-hooks/exhaustive-deps` lint rule check, and why not silence it?**
A: It warns when an effect or memo uses values that are missing from its dependency array. Ignoring it usually causes stale closures, so fix the code (move logic, use a functional update) instead.

**Q: When does an effect's cleanup function run?**
A: Before the effect runs again because a dependency changed, and when the component unmounts. Use it to remove listeners, clear timers and abort requests.

### Effects pitfalls

**Q: What is wrong with `useEffect(async () => { ... }, [])`?**
A: An effect must return nothing or a cleanup function, but an async function returns a promise. Define an async function inside the effect and call it, or use a data-fetching library.

**Q: Why can `useEffect(() => { setData({ a: 1 }); })` with no dependency array loop forever?**
A: With no array the effect runs after every render, and setting a new object causes another render. Add a dependency array, or remove the effect if the value can be computed during render.

**Q: Why does an effect with an object or array in its dependencies keep re-running?**
A: Objects and arrays created during render have a new identity each time, and React compares dependencies with `Object.is`. Depend on primitive values, or move the object outside the component or into `useMemo`.

**Q: How do you avoid a race condition when fetching in an effect?**
A: Requests can finish out of order, so an old response may overwrite a newer one. Abort the old request in cleanup with `AbortController`, or set an `ignore` flag in cleanup and skip `setState` when it is true.

**Q: What is wrong with `useEffect(() => { setInterval(() => setCount(count + 1), 1000); }, [])`?**
A: The callback captures `count` from the first render so the value stops at 1, and the interval is never cleared. Use `setCount(c => c + 1)` and return `() => clearInterval(id)`.

**Q: Why is copying props into state with an effect usually a mistake?**
A: The component renders once with stale state and then again after the effect runs. Compute the value during render, or use a `key` to reset state when the input identity changes.

**Q: How do you decide between an event handler and an effect?**
A: If code runs because the user did something (click, submit), put it in a handler. Use an effect only to synchronise with something outside React because the component is on screen, like a subscription or a timer.

**Q: Why must `removeEventListener` receive the same function reference as `addEventListener`?**
A: Listeners are matched by function identity, so `removeEventListener("resize", () => ...)` with a new arrow function removes nothing. Keep the handler in a variable inside the effect and use it in both places.

### State design

**Q: Why not store derived values in state?**
A: Duplicated state goes out of sync. If `total` or `fullName` can be calculated from props or other state, calculate it during render (use `useMemo` only if it is truly expensive).

**Q: Why does `useState(props.initial)` not update when the prop changes later?**
A: The prop only seeds the state on the first render, and after that the state is independent. Use the prop directly, lift the state up, or reset the component with a `key`.

**Q: Why is a `status` field better than `isLoading`, `isError` and `isSuccess` booleans?**
A: Several booleans can contradict each other (loading and error both true). One value like `"idle" | "loading" | "success" | "error"`, or a `useReducer`, makes impossible states impossible.

**Q: Why store a `selectedId` instead of a copy of the selected object?**
A: A copy goes stale when the list is updated. Store the id and look up the item during render so there is one source of truth.

**Q: How do you update a nested object in state without mutating it?**
A: Copy every level you change: `setUser(u => ({ ...u, address: { ...u.address, city } }))`. For arrays use `map`, `filter` or spread, and for deep structures Immer makes it easier.

**Q: What is the difference between server state and client state?**
A: Server state is remote data you only borrow, and it needs caching, refetching, deduping and invalidation, so use TanStack Query or SWR. Client state is UI-only (modal open, draft text) and fits `useState` or a small store.

**Q: How can you avoid prop drilling without a global store?**
A: Use composition first (pass components or `children` as props). Use context only for data that is truly shared widely, like theme or current user.

### Forms

**Q: How do you handle many inputs with one change handler?**
A: Give each input a `name` and keep one state object: `setForm(f => ({ ...f, [e.target.name]: e.target.value }))`.

**Q: What happens if you set `value` on an input without `onChange`?**
A: React warns and the field becomes read-only. Add `onChange`, or use `defaultValue` if you want an uncontrolled input with an initial value.

**Q: How do checkboxes and file inputs differ from text inputs in React?**
A: A checkbox uses `checked` and `e.target.checked`, not `value`. A file input is always uncontrolled because only the user can set its value, so read `e.target.files`.

**Q: Why use React Hook Form instead of plain controlled inputs?**
A: It keeps fields uncontrolled and subscribes selectively, so large forms re-render far less. It also gives validation, error and dirty state, and works with Zod through a resolver.

**Q: How should form validation errors be shown accessibly?**
A: Put the message next to the field, link it with `aria-describedby`, set `aria-invalid`, and move focus to the first invalid field on submit. Validate again on the server.

**Q: How do you prevent a double submit?**
A: Disable the button or ignore clicks while the request is pending. Also protect the server with an idempotency key or a unique constraint, because a UI guard alone is not enough.

### Refs

**Q: When should a value be a ref instead of state?**
A: When it does not affect what is rendered and changing it should not cause a re-render, such as a timer id, a previous value or a DOM node. If the screen depends on it, use state.

**Q: Why avoid reading or writing `ref.current` during render?**
A: Rendering must be pure and refs are mutable, so results become unpredictable and can break under concurrent rendering. Read and write refs in effects and event handlers.

**Q: What is a callback ref?**
A: A function passed as `ref={(node) => ...}`. React calls it with the DOM node when it attaches and with `null` when it detaches, which helps when measuring or when the node appears conditionally.

**Q: How do you pass a ref to a child component's DOM element?**
A: Older React uses `forwardRef`, while React 19 lets function components receive `ref` as a normal prop (check your version). To expose only a few methods instead of the whole node, use `useImperativeHandle`.

### Context

**Q: What is wrong with `<AuthContext.Provider value={{ user, login }}>` in a component that re-renders often?**
A: The object literal is new on every render, so every consumer re-renders each time. Wrap the value in `useMemo` (and `login` in `useCallback`), or keep the provider where it rarely re-renders.

**Q: When is the default value in `createContext(default)` used?**
A: Only when a component reads the context without a matching Provider above it. A common pattern is a `null` default and a `useAuth()` hook that throws a clear error when the provider is missing.

**Q: Does `React.memo` stop a component from re-rendering when its context changes?**
A: No. A component that reads a context re-renders when that context value changes, whatever memo says, because memo only compares props.

### Performance

**Q: How do you find out why a React app is slow?**
A: Use the React DevTools Profiler to see what renders and why, and measure on a production build. Also check the browser Performance tab for long tasks before adding any memoisation.

**Q: Why does `React.memo` sometimes not help?**
A: New object, array or function props are created on every render, so the shallow comparison fails. Stabilise them with `useMemo`/`useCallback` or restructure the component.

**Q: How do you stop fast-changing state from re-rendering a heavy subtree?**
A: Move the state down into a small component that uses it, or pass the heavy parts in as `children` from above. Elements created by the parent keep the same identity, so React skips them.

**Q: How do you render a list of 10,000 rows efficiently?**
A: Virtualise it (react-window or TanStack Virtual) so only visible rows exist in the DOM, or paginate. Memoising each row does not fix a huge DOM.

**Q: `useTransition` vs `useDeferredValue`?**
A: `useTransition` wraps a state update you control and marks it low priority, and gives you `isPending`. `useDeferredValue` takes a value you receive (like typed text or a prop) and returns a lagging copy so heavy rendering can wait.

**Q: How do you code-split in React?**
A: `const Chart = lazy(() => import("./Chart"))` rendered inside `<Suspense fallback={...}>`. Split by route first, then by heavy widgets such as charts and editors.

**Q: What is the React Compiler?**
A: A build-time tool that automatically memoises components and hooks, so you write fewer `useMemo` and `useCallback` calls. It assumes you follow the Rules of React, so check the current docs for status and setup.

### React 19 and concurrent features

**Q: What does Suspense do?**
A: It shows a fallback while something inside it is not ready, such as lazy-loaded code or data from a Suspense-enabled library or framework. It lets you place loading UI declaratively at chosen boundaries.

**Q: What is concurrent rendering?**
A: React can start rendering, pause, and switch to a more urgent update (like typing) before finishing. It is why render functions must be pure, and it powers transitions and `useDeferredValue`.

**Q: What does the `use` API do in recent React versions?**
A: `use(promise)` reads a promise's result and suspends until it is ready, and `use(Context)` reads context. Unlike other hooks it can be called inside conditions. Check the docs for where the promise should be created.

**Q: What is `useOptimistic`?**
A: A hook that shows the expected result immediately while an async action is still running, then goes back to the real state when it finishes. It suits like buttons and chat messages.

**Q: What do `useActionState` and `useFormStatus` give you?**
A: They work with form `action` functions. `useActionState` returns the latest result or error plus a pending flag, and `useFormStatus` lets a child such as a submit button read its parent form's pending state. Check the docs for exact signatures in your version.

### Testing with React Testing Library

**Q: What is the guiding principle of React Testing Library?**
A: Test the way users use the app: find elements by role, label or text and assert on what is visible, not on state, props or component internals. Then refactors do not break tests.

**Q: `getBy` vs `queryBy` vs `findBy`?**
A: `getBy` throws if nothing matches, `queryBy` returns `null` (use it to assert something is absent), and `findBy` returns a promise that waits and retries (use it for async UI).

**Q: Which queries should you prefer in RTL?**
A: `getByRole` (with `name`) first, then `getByLabelText`, `getByPlaceholderText` and `getByText`, and `getByTestId` only as a last resort. Role queries also check basic accessibility.

**Q: `userEvent` vs `fireEvent`?**
A: `userEvent` simulates real interaction (focus, key presses and pointer events in order) and is the recommended choice. `fireEvent` dispatches a single DOM event. Use `const user = userEvent.setup()` and `await user.click(button)`.

**Q: How do you test a component that fetches data?**
A: Mock the network (for example with MSW), render, and `await screen.findByText(...)` for the loaded content. Test loading, success and error states instead of mocking `fetch` internals.

**Q: What does the "not wrapped in act(...)" warning mean?**
A: A state update happened outside what the test was waiting for, so the test may assert before React finished. RTL already wraps most things in `act`, so fix it by awaiting the UI change with `findBy` or `waitFor`.

**Q: How do you test a custom hook or a component that needs providers?**
A: Use `renderHook` for hooks, and pass a `wrapper` (or a custom `render` helper) that adds the router, query client or context providers. If a hook is tied closely to UI, test it through a component.

### Accessibility in React

**Q: Why is `<div onClick={...}>` a bad button?**
A: It has no keyboard focus, no Enter or Space handling and no button role for screen readers. Use `<button type="button">`, which gives all of this for free.

**Q: Which JSX attribute names differ from HTML for classes and labels?**
A: `className` replaces `class` and `htmlFor` replaces `for`. Every input needs a label linked with `htmlFor` and `id` (or wrapping it), and `useId` can generate the id.

**Q: How should focus be managed in a modal?**
A: Move focus into the dialog when it opens, keep Tab inside it, close on Escape and return focus to the button that opened it. The native `<dialog>` element with `showModal()` handles much of this.

**Q: How do you announce dynamic updates, like toasts or form errors, to screen readers?**
A: Put them in an `aria-live` region (`role="status"` for polite, `role="alert"` for urgent) that already exists in the DOM before its text changes.

**Q: What alt text should images have?**
A: Describe meaningful images in a short phrase and use `alt=""` for decorative ones so screen readers skip them. `eslint-plugin-jsx-a11y` catches many mistakes like a missing alt.

### Component patterns

**Q: What is a higher-order component (HOC)?**
A: A function that takes a component and returns a new one with extra props or behaviour, such as `withAuth(Dashboard)`. Hooks replaced most uses. Downsides are wrapper nesting and prop name clashes, and never create the wrapped component inside render.

**Q: What is the render props pattern?**
A: A component receives a function (often as `children`) and calls it with data to decide what to render, like `<Mouse>{pos => <Cat pos={pos} />}</Mouse>`. Custom hooks cover most cases now, but libraries still use it.

**Q: What are compound components?**
A: A group of components that share implicit state through context, like `<Tabs><Tabs.List /><Tabs.Panel /></Tabs>`. The user composes the parts freely and the parent hides the wiring.

**Q: What does `createPortal` do and what happens to events?**
A: It renders children into another DOM node (such as `document.body`) so modals and tooltips escape `overflow` and `z-index` clipping. Events still bubble through the React tree, not the DOM tree.

**Q: How do you design a component that works both controlled and uncontrolled?**
A: Accept `value` and `onChange` for controlled use and `defaultValue` for uncontrolled use, and keep internal state only when `value` is undefined. Native inputs and many UI libraries work this way.

**Q: How is the container/presentational pattern done today?**
A: Keep UI components dumb (props in, JSX out) and move data and logic into a custom hook or the parent. This makes the UI easy to test and reuse.

### What is wrong with this code: JSX

**Q: What is wrong with `return <h1>Hi</h1><p>Bye</p>;`?**
A: A component must return a single root. Wrap the elements in a parent element or a fragment `<>...</>`.

**Q: What is wrong with `<button onClick={handleDelete(id)}>`?**
A: It calls `handleDelete` during render and passes its result to `onClick`. Pass a function instead: `onClick={() => handleDelete(id)}`.

**Q: What is wrong with `<div style="color: red">`?**
A: In JSX `style` takes an object with camelCase keys: `style={{ color: "red" }}`.

**Q: What is wrong with `items.map((i) => <li key={Math.random()}>{i}</li>)`?**
A: The key changes on every render, so React unmounts and remounts every item, losing state and hurting performance. Use a stable unique id from the data.

**Q: What does `{count && <Cart />}` render when `count` is 0?**
A: The number 0, because `0 && x` evaluates to `0` and React renders numbers. Use `{count > 0 && <Cart />}` or a ternary.

**Q: What is wrong with `<div dangerouslySetInnerHTML={{ __html: comment.body }} />`?**
A: If the HTML comes from users it is an XSS hole. Render it as plain text, or sanitise it first with a library such as DOMPurify.

**Q: Why does `{items.map(item => { <li key={item.id}>{item.name}</li> })}` render nothing?**
A: The braces make a function body with no `return`, so every call returns `undefined`. Use parentheses `=> (<li ...>)` or add `return`.

### What is wrong with this code: state and effects

**Q: What is wrong with `user.name = "Asha"; setUser(user);`?**
A: It mutates the existing object and passes the same reference, so React may skip the re-render. Create a copy: `setUser({ ...user, name: "Asha" })`.

**Q: What is wrong with `setItems(items.push(newItem))`?**
A: `push` mutates the array and returns its new length, so the state becomes a number. Use `setItems([...items, newItem])`.

**Q: What happens if you call `setCount(count + 1)` directly in the component body?**
A: Every render triggers a state update and another render, ending in a "Too many re-renders" error. Update state in event handlers or effects.

**Q: What is wrong with `useEffect(() => { loadUser(id); }, []);`?**
A: It reads `id` but does not list it, so it never reloads when `id` changes (a stale closure). Add `id` to the dependency array.

**Q: Output: a click runs `setCount(count + 1); setTimeout(() => alert(count), 1000);` with `count` at 0. What does the alert show?**
A: 0. The timeout callback captured `count` from that render, and state is a snapshot.

## 7. Next.js (App Router)

### Routing and layouts

**Q: How does file-based routing work in the App Router?**
A: Folders inside `app/` are URL segments, and a folder becomes a public route only when it contains a `page.js`. `route.js` makes an API endpoint, and `layout.js` wraps a segment and its children.

**Q: What are the dynamic route segment types?**
A: `[id]` matches one segment, `[...slug]` matches one or more segments, and `[[...slug]]` also matches the path with no segments.

**Q: What are route groups and private folders?**
A: A folder named `(marketing)` groups routes and layouts without adding to the URL, and lets you have different root layouts. A folder named `_components` is private and never becomes a route.

**Q: Layout vs template?**
A: A layout stays mounted when you navigate between its child routes, so its state is kept and it does not re-render. A `template.js` creates a new instance on each navigation, so state resets and effects run again.

**Q: What are parallel routes and intercepting routes?**
A: Parallel routes (`@slot` folders) render several pages in one layout at the same time. Intercepting routes (like `(.)photo`) show another route's UI inside the current layout, which is used for modals that still have a shareable URL.

**Q: Why use `next/link` instead of a plain `<a>`?**
A: `Link` navigates on the client without a full page reload and prefetches routes that appear in the viewport (in production). A plain `<a>` reloads the whole page.

**Q: Which module do `useRouter`, `usePathname` and `useSearchParams` come from in the App Router?**
A: `next/navigation`. The older `next/router` belongs to the Pages Router and does not work inside `app/`.

**Q: Why does `redirect()` inside a `try/catch` seem not to work?**
A: `redirect()` works by throwing a special error, so your `catch` swallows it. Call it outside the `try` block or rethrow the error. `notFound()` behaves the same way.

**Q: In recent Next.js versions, how do you read `params` and `searchParams`?**
A: They are promises in newer versions, so you `await params` in an async Server Component (or use `use(params)` in a Client Component). Older versions pass plain objects, so check the docs for your version.

### Server and Client Components

**Q: Can a Client Component import a Server Component?**
A: Not directly, because an imported module becomes part of the client bundle. But a Server Component can pass another Server Component into a Client Component as `children` or a prop.

**Q: What can you not do in a Server Component?**
A: Use `useState`, `useEffect` or other client hooks, attach event handlers like `onClick`, call `createContext`, or use browser APIs like `window`. Move those parts into a small Client Component.

**Q: What kinds of props can cross from a Server Component to a Client Component?**
A: Serializable values such as strings, numbers, plain objects, arrays and JSX. Normal functions and class instances cannot cross, with Server Actions as the exception.

**Q: What does the `server-only` package do?**
A: Importing it in a module makes the build fail if that module ends up in client code. It protects files that use secrets or talk directly to the database.

**Q: How do you use a context provider in the App Router?**
A: Put the provider in a file that starts with `"use client"` and render it in a Server Component layout, passing the rest of the tree as `children`. The children can still be Server Components.

**Q: Are Client Components rendered only in the browser?**
A: No. On the first load they are pre-rendered to HTML on the server and then hydrated. `"use client"` means they also ship JavaScript and can use state and effects.

**Q: A third-party component uses hooks but has no `"use client"`, and it fails in a Server Component. What do you do?**
A: Create your own file that starts with `"use client"`, import and re-export the component there, and use that wrapper.

**Q: What is the RSC payload?**
A: A compact description of the rendered Server Component tree (with placeholders for Client Components) that the server streams to the browser. React uses it to update the page on navigation without a full reload.

### Data fetching and caching

**Q: How do you fetch data in a Server Component?**
A: Make the component `async` and `await` a `fetch` call or a direct database query. No `useEffect` or API route is needed.

**Q: How do you avoid request waterfalls in Server Components?**
A: Start independent requests together with `Promise.all`, or split the page into components wrapped in `<Suspense>` so they fetch and stream in parallel. Awaiting one request after another is sequential.

**Q: How does Next.js dedupe the same request across components?**
A: Identical `fetch` GET calls during one render pass are memoised, and for database calls you wrap the function in React's `cache()`. Caching across requests is a separate topic that changed between versions.

**Q: `revalidatePath` vs `revalidateTag`?**
A: Both mark cached data stale after a mutation. `revalidatePath("/posts")` targets a route, and `revalidateTag("posts")` targets every cached fetch labelled with that tag. Check the docs for the exact behaviour in your version.

**Q: What makes a route dynamic instead of static?**
A: Reading request-specific data such as `cookies()`, `headers()` or `searchParams` makes it render per request. Other routes can be prerendered at build time, but check the docs for the exact rules in your version.

**Q: How do `loading.js` and Suspense help with streaming?**
A: The server sends the page shell and fallback immediately, then streams slower parts as they become ready. Users see content sooner instead of waiting for the slowest query.

**Q: Why is calling your own Route Handler from a Server Component a bad idea?**
A: It adds an unnecessary network hop and repeats auth work on the same server. Call the shared function (service or DB query) directly, and keep Route Handlers for external clients.

**Q: What does `generateStaticParams` do?**
A: It returns the param values for a dynamic route so those pages are prerendered at build time. Other values are rendered on demand, depending on your route configuration.

### Server Actions and forms

**Q: How do you create a Server Action?**
A: Write an `async` function with the `"use server"` directive (inside the function, or at the top of a file to mark all its exports), then pass it to `<form action={fn}>` or call it from a Client Component.

**Q: Are Server Actions secure by default?**
A: No. Each one is a public HTTP endpoint that anyone can call with any input. Check authentication and authorisation inside the action and validate the arguments, as you would for an API route.

**Q: Why can forms that use Server Actions work before JavaScript loads?**
A: A `<form action>` with a Server Action falls back to a normal form POST, which gives progressive enhancement. After hydration Next submits it without a full page reload.

**Q: After a mutation, how do you refresh the data shown on the page?**
A: Call `revalidatePath` or `revalidateTag` inside the action, then `redirect` if you want to navigate. Without revalidation, cached data may keep showing the old values.

**Q: How do you return validation errors from a Server Action?**
A: Return a plain object like `{ errors: { email: "Invalid" } }` and render it with `useActionState`. Throwing is for unexpected errors.

**Q: How do you show a pending state on a submit button?**
A: Use `useFormStatus` in a component rendered inside the `<form>`, or use the pending flag from `useActionState` or `useTransition`.

### Route Handlers and middleware

**Q: How do you write a Route Handler?**
A: Export functions named after HTTP methods (`GET`, `POST`) from a `route.js` file, taking a `Request` and returning a `Response` (or `NextResponse.json(...)`). A `route.js` cannot sit at the same segment as a `page.js`.

**Q: How do you handle a webhook in a Route Handler?**
A: Read the raw body with `await request.text()`, verify the provider's signature header against it, and only then parse the JSON. Return a 2xx response quickly and move heavy work to a queue.

**Q: What is middleware (called proxy in newer versions) good for?**
A: Cheap checks before a request reaches a route: redirects, rewrites, setting headers, locale detection and simple cookie checks. Do not make it your only auth check or run heavy work in it, and check the docs for the current file name and runtime limits.

**Q: Are `GET` Route Handlers cached by default?**
A: This has changed between major versions, so do not assume. Check the docs for your version and opt in or out explicitly.

### Metadata, rendering and hydration

**Q: `metadata` vs `generateMetadata`?**
A: Export a static `metadata` object for fixed titles and descriptions. Export an async `generateMetadata({ params })` when the title or Open Graph data depends on route params or fetched data.

**Q: How do you add sitemap, robots and share images in the App Router?**
A: Use file conventions: `sitemap.js`, `robots.js` and `opengraph-image` files inside the route folder. Next serves them at the correct URLs.

**Q: How can you tell if a route is static or dynamic?**
A: The `next build` output marks each route as static or dynamic, so read it instead of guessing. A route becomes dynamic when it uses request-time data.

**Q: Why does `useSearchParams` often need a `<Suspense>` boundary?**
A: On a statically rendered page the search params are not known at build time, so the component using the hook must be inside Suspense or the build can fail. Wrap only that component.

**Q: How do you fix a hydration mismatch caused by browser-only values?**
A: Render the same output on the server and on the first client render, then set the browser value in `useEffect` (for example a `mounted` flag). For harmless known differences such as timestamps, `suppressHydrationWarning` on that element works.

### Assets and performance

**Q: How does `next/font` help?**
A: It downloads fonts at build time and serves them from your own domain, avoiding an extra request to Google. It also reduces layout shift by using a size-adjusted fallback font.

**Q: What does `next/image` need for remote images?**
A: Allow the hostnames in `next.config.js` under `images.remotePatterns`, and give `width` and `height` (or `fill`) plus `sizes`. Mark the above-the-fold LCP image as high priority (the prop name has varied by version).

**Q: How do you load a browser-only library, like a chart or map?**
A: Use `next/dynamic` with `ssr: false` inside a Client Component, or import it inside an effect. This keeps it out of server rendering and out of the main bundle.

### Errors, auth and deployment

**Q: What are the rules for `error.js` and `global-error.js`?**
A: `error.js` must be a Client Component, receives `error` and a reset function, and catches errors from its children but not from the layout in the same segment. `global-error.js` replaces the root layout and must render its own `<html>` and `<body>`.

**Q: Why should you not do auth checks only in layouts?**
A: Layouts do not re-render on every navigation between their child routes, so the check can be skipped. Verify the session in each page, Server Action and data-access function that needs it.

**Q: When do `NEXT_PUBLIC_` variables get their value?**
A: At build time, when they are inlined into the JavaScript bundle. Changing one needs a rebuild, so one image cannot be reused across environments for those values.

**Q: How do you deploy Next.js in Docker?**
A: Set `output: "standalone"` to get a minimal server bundle, build with a multi-stage Dockerfile and run `node server.js`. If you run several instances, plan for the shared cache and image optimisation storage.

**Q: Edge runtime vs Node.js runtime?**
A: The Edge runtime starts fast and runs close to users but supports only a limited set of APIs, so many Node modules and native packages do not work. The Node.js runtime has the full API set, so choose it unless you need edge.

## 8. Node.js and Express

### Event loop and async behaviour

**Q: What are the phases of the Node.js event loop?**
A: Timers (`setTimeout` and `setInterval` callbacks), pending callbacks, idle/prepare (internal), poll (most I/O callbacks), check (`setImmediate`) and close callbacks. Between callbacks Node runs `process.nextTick` callbacks and then promise microtasks.

**Q: `setTimeout(fn, 0)` vs `setImmediate(fn)`: which runs first?**
A: From the main module the order is not guaranteed because it depends on process timing. Inside an I/O callback `setImmediate` always runs first.

**Q: In a CommonJS file you run `setTimeout` (T), `setImmediate` (I), `Promise.resolve().then` (P), `process.nextTick` (N) and a sync `console.log` (S). What is the output order?**
A: S, N, P, then T and I (their order can vary in the main module). Sync code runs first, then nextTick, then promise microtasks, then the timers and check phases.

**Q: If Node is single-threaded, how does it do work in parallel?**
A: Your JavaScript runs on one thread, but network I/O uses OS async mechanisms and libuv has a thread pool (default size 4, `UV_THREADPOOL_SIZE`) for file system, `crypto` (pbkdf2, scrypt), zlib and `dns.lookup`. Worker threads add real parallel JavaScript.

**Q: How do you find out that the event loop is being blocked?**
A: Measure event loop delay (for example `perf_hooks.monitorEventLoopDelay()`) or notice latency rising on all routes at once. Then profile with `--cpu-prof` or Clinic.js to find the slow synchronous function.

**Q: What happens on an unhandled promise rejection in modern Node?**
A: Since Node 15 the default is to throw, which crashes the process like an uncaught exception. Always `await` or `.catch` promises, and log with `process.on("unhandledRejection")` for visibility.

**Q: What should you do in an `uncaughtException` handler?**
A: Log the error and shut down, then let a supervisor (PM2, Docker, Kubernetes) restart the process. It may be in an inconsistent state, so do not keep serving traffic.

### Streams and buffers

**Q: What are the four types of streams?**
A: Readable (a source, like a file read), Writable (a destination, like an HTTP response), Duplex (both, like a TCP socket) and Transform (a duplex that changes data, like gzip).

**Q: What is backpressure in streams?**
A: A fast readable can fill memory if the writable is slow. `write()` returns `false` when its buffer is full, and you should wait for the `drain` event, which `pipe` and `pipeline` do for you.

**Q: `pipe()` vs `stream.pipeline()`?**
A: `pipe` does not forward errors or clean up the other streams, which can leak file descriptors. `pipeline` (or the promise version in `stream/promises`) propagates errors and destroys all streams.

**Q: `Buffer.alloc` vs `Buffer.allocUnsafe`?**
A: `alloc` returns zero-filled memory. `allocUnsafe` is faster but may contain old memory contents, so use it only when you immediately overwrite every byte.

**Q: How do you send a large file without loading it all into memory?**
A: Stream it: `pipeline(fs.createReadStream(path), res, cb)`. `readFile` would load the whole file into RAM for every request.

### Scaling and processes

**Q: `cluster` vs `worker_threads` vs `child_process`?**
A: `cluster` runs several Node processes sharing one port to use all CPU cores. `worker_threads` run JavaScript in threads inside one process for CPU-heavy work and can share memory. `child_process` launches separate programs or scripts.

**Q: Why must a Node service be stateless to scale horizontally?**
A: Each instance has its own memory, so in-memory sessions, caches and rate-limit counters are not shared and are lost on restart. Keep them in Redis or the database.

**Q: PM2 or containers for running Node in production?**
A: PM2 restarts crashed processes, runs cluster mode and manages logs on a VM. In Docker or Kubernetes, run one Node process per container and let the orchestrator handle restarts and scaling.

### Express fundamentals and Express 5

**Q: What changed in Express 5 that interviewers like to ask about?**
A: Rejected promises and errors in async handlers reach the error handler automatically, route path syntax is stricter (wildcards need names, like `/*splat`), and `req.body` is `undefined` if no body parser ran. Read the official migration guide for the full list.

**Q: `app.use` vs `app.get`?**
A: `app.use(path, fn)` matches every HTTP method and any URL that starts with the path. `app.get(path, fn)` matches only GET and the exact route.

**Q: What does `express.json()` do and what is its default size limit?**
A: It parses JSON request bodies into `req.body`. The default limit is 100kb, so set `limit` on purpose: small for most routes, bigger only where needed.

**Q: How do you organise routes with `express.Router`?**
A: Create a router per resource (`users`, `orders`), define its routes and middleware, and mount it with `app.use("/users", usersRouter)`. You can attach auth middleware to a whole router.

**Q: How do you return a JSON 404 for unknown routes?**
A: Add a middleware after all routes, like `app.use((req, res) => res.status(404).json({ error: "Not found" }))`, and put the error handler after that. Express's default 404 page is HTML.

**Q: What causes "Cannot set headers after they are sent to the client"?**
A: Sending a response twice, such as calling `res.json` and then continuing into code that also responds. Use `return res.status(400).json(...)` in early-exit branches.

**Q: `next()` vs `next(err)` vs `next("route")`?**
A: `next()` passes control to the next middleware. `next(err)` skips to the error-handling middleware. `next("route")` skips the remaining handlers of the current route.

**Q: When do you need `app.set("trust proxy", 1)`?**
A: When the app runs behind Nginx or a load balancer. Without it `req.ip` is the proxy's IP and `req.protocol` is http, which breaks rate limiting and secure cookies.

**Q: How do you design error handling for an Express API?**
A: Create an `AppError` with a status code and a safe message, throw it from services, and map every error in one error middleware. Log the full error, but for unexpected 500s send a generic message without the stack trace.

### Authentication and tokens

**Q: What is refresh token rotation?**
A: Each refresh issues a new refresh token and invalidates the old one. If an already-used token appears again, treat it as theft and revoke that whole token family.

**Q: Is the data inside a JWT secret?**
A: No. The payload is only base64url encoded, so anyone can decode it. The signature proves it was not changed, so never put passwords or sensitive data inside.

**Q: Why pass `algorithms` when verifying a JWT?**
A: So the verifier accepts only the algorithm you expect, e.g. `jwt.verify(token, key, { algorithms: ["HS256"] })`. This blocks attacks that use `alg: none` or confuse HMAC and RSA keys.

**Q: How do you log out a user who uses JWTs?**
A: A signed JWT stays valid until it expires, so use short-lived access tokens, clear the cookies, and revoke the refresh token in the database. For instant revocation keep a deny-list or a per-user token version.

**Q: HS256 vs RS256 for JWT signing?**
A: HS256 uses one shared secret to sign and verify. RS256 signs with a private key and verifies with a public key, so other services can verify tokens without being able to issue them.

**Q: Why not use the default `express-session` MemoryStore in production?**
A: It leaks memory, loses sessions on restart and does not work across several instances. Use a Redis or database store and set `httpOnly`, `secure` and `sameSite` on the cookie.

### Security hardening

**Q: What does `helmet` do?**
A: It sets protective response headers such as `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy` and a default `Content-Security-Policy`, and removes `X-Powered-By`. The CSP may need tuning for your frontend.

**Q: Why can't you use `origin: "*"` together with `credentials: true` in CORS?**
A: Browsers reject a wildcard origin on credentialed requests. Use an allow-list of origins, echo the matching one back, and send `Vary: Origin`.

**Q: Why does `express-rate-limit` need a shared store in production?**
A: The default memory store counts per process, so with several instances the real limit multiplies and resets on restart. Use a Redis store, and set `trust proxy` so it sees real client IPs.

**Q: What is NoSQL injection in a Node and MongoDB login?**
A: If `req.body.email` is `{ "$ne": null }`, a query like `User.findOne({ email })` matches any user. Validate that fields are strings with a schema and never pass raw `req.body` into a query.

**Q: How do you prevent path traversal when serving files by a user-supplied name?**
A: A name like `../../etc/passwd` escapes your folder. Resolve the final path with `path.resolve` and check that it starts with the allowed base directory, or use ids that map to stored file names.

**Q: How do you verify a webhook signature in Express?**
A: The provider signs the raw bytes, so use `express.raw({ type: "application/json" })` on that route before any JSON parser, compute the HMAC, and compare with `crypto.timingSafeEqual`.

**Q: What is prototype pollution?**
A: Untrusted JSON with keys like `__proto__` can change `Object.prototype` when merged unsafely, altering behaviour app-wide. Validate input shapes, avoid deep merges of raw input and keep dependencies updated.

### Testing Express apps

**Q: How do you test Express routes without starting a server?**
A: Export `app` from `app.js` and call `listen` only in `server.js`. Then use Supertest: `await request(app).get("/health").expect(200)`.

**Q: Should you mock the database in API tests?**
A: Prefer a real test database (Docker or Testcontainers) with migrations and cleanup between tests, because mocks hide SQL and constraint bugs. Mock only external services.

**Q: How do you mock outbound HTTP calls in tests?**
A: Intercept them with `nock` or MSW so tests are fast and deterministic, and also test timeouts and error responses from the third party.

**Q: Jest vs Vitest vs the built-in Node test runner?**
A: Node has `node --test` built in and needs no dependencies. Jest and Vitest add richer mocking and watch mode, and Vitest works well with ESM. Pick one and stay consistent.

**Q: How do you unit test an auth middleware?**
A: Call it with a fake `req`, a fake `res` (with spied `status` and `json`) and a spied `next`. Assert that it calls `next()` for a valid token and responds 401 otherwise.

### Logging and health checks

**Q: Why use a structured logger like `pino` instead of `console.log`?**
A: JSON logs with levels and fields are searchable and filterable in CloudWatch or ELK, and `pino` is fast. Log the request id, status and duration, but never passwords or tokens.

**Q: How do you trace one request across logs?**
A: Create or accept an `X-Request-Id` per request, add it to every log line and return it to the client. `AsyncLocalStorage` can carry it through async calls without passing it as an argument.

**Q: Liveness vs readiness checks?**
A: Liveness says the process is running (restart it if the check fails). Readiness says dependencies such as the database are reachable, so the instance can receive traffic.

### Graceful shutdown

**Q: How do you implement graceful shutdown in an Express server?**
A: On `SIGTERM` or `SIGINT` call `server.close()` to stop new connections, wait for in-flight requests, close DB and Redis connections, then exit. Add a timeout that forces exit if something hangs.

**Q: Why does shutdown handling matter in Docker or Kubernetes?**
A: The orchestrator sends `SIGTERM` and kills the container after a grace period, so Node must handle that signal. Running Node as PID 1 without an init process (such as `docker run --init` or tini) can mishandle signals.

**Q: Why do users sometimes see random 502 errors behind a load balancer?**
A: If Node closes an idle keep-alive connection before the load balancer does, a request can hit a closed socket. Set `server.keepAliveTimeout` higher than the load balancer's idle timeout, and keep `headersTimeout` above it.

### File uploads

**Q: How does `multer` store uploads?**
A: It parses `multipart/form-data`. `memoryStorage` keeps files in RAM (only for small files) and `diskStorage` writes them to disk. Always set `limits.fileSize`, a maximum file count and a `fileFilter`.

**Q: Why use presigned URLs for large uploads?**
A: The API returns a short-lived presigned S3 URL and the browser uploads straight to S3, so big files never pass through Node. Then the client sends the object key to your API, which verifies and records it.

**Q: How can you handle uploads without buffering the whole file?**
A: Use a streaming parser such as `busboy` (which multer is built on) and pipe the file stream to S3 or disk. Memory stays flat even for huge files.

### WebSockets and real-time

**Q: WebSocket vs SSE vs polling?**
A: WebSocket is a two-way persistent connection (chat, games). SSE is one-way server-to-client over normal HTTP with automatic reconnect, which fits streaming LLM tokens. Polling is the simplest but wastes requests.

**Q: `ws` vs Socket.IO?**
A: `ws` is a small, standard WebSocket library. Socket.IO adds rooms, acknowledgements, automatic reconnection and fallbacks, but uses its own protocol, so clients must use the Socket.IO client.

**Q: How do you scale WebSockets across several instances?**
A: A socket lives on one instance, so use a pub/sub adapter such as Redis so a message emitted on one instance reaches clients on the others. If a long-polling fallback is enabled, you also need sticky sessions.

**Q: How do you secure and maintain a WebSocket connection?**
A: Authenticate during the handshake (cookie or short-lived token) and reject before upgrading. Send periodic ping/pong and terminate sockets that do not answer, and avoid long-lived tokens in URLs because URLs get logged.

### Queues and background jobs

**Q: What does BullMQ give you for background jobs?**
A: A Redis-backed queue where the API adds jobs and separate worker processes run them, with retries, exponential backoff, delays, concurrency limits and a failed-job list.

**Q: Why must queue job handlers be idempotent?**
A: Queues usually deliver at least once, so a job can run twice after a crash or retry. Use unique keys or "already processed" checks so a repeat does not send a second email or charge twice.

**Q: How do you run a scheduled job when you have many app instances?**
A: A cron in every instance would run the job N times. Use the queue's repeatable jobs, a single scheduler process, or a distributed lock so only one instance runs it.

### Practical Node details

**Q: Why is `if (process.env.ENABLE_CACHE)` true even when the value is `"false"`?**
A: Environment variables are always strings, and the string `"false"` is truthy (a port is also a string). Parse and validate config once at startup, for example with Zod, and fail fast if something is missing.

**Q: How do you get `__dirname` in an ES module?**
A: It does not exist in ESM. Use `import.meta.dirname` in recent Node versions, or `path.dirname(fileURLToPath(import.meta.url))`.

**Q: Why create one `pg.Pool` at startup instead of a client per request?**
A: Opening a connection per request is slow and quickly exhausts the database connection limit. A shared pool reuses connections, and a checked-out client must always be released in `finally`.

**Q: What happens if an `EventEmitter` emits `"error"` and nobody is listening?**
A: Node throws the error, which can crash the process. Attach an `error` listener to emitters and streams, and remove listeners you add repeatedly to avoid the MaxListenersExceededWarning.

**Q: Does Node have a built-in `fetch`, and how do you set a timeout on it?**
A: Yes, since Node 18. Use `fetch(url, { signal: AbortSignal.timeout(5000) })` so a slow upstream cannot hang your request forever.

**Q: How does the `require` cache affect module-level state?**
A: A CommonJS module runs once and its exports are cached, so every `require` of that file returns the same object. That is why a module-level DB client behaves like a singleton, and ESM works similarly.
