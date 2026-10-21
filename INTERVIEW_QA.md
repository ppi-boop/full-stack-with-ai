# Interview Questions and Topics (short answers)

Quick revision sheet for the 24-week roadmap. Each section has **Topics to know** and **Q&A**. Answers are deliberately short: say them out loud in your own words, then add one example from your own work.

> Rule: if you can't explain an answer without reading it, you don't know it yet. Mark it and revisit.
> Version-sensitive areas (Next.js caching, LLM APIs, AWS services) change often. Check the official docs before an interview.

Contents: 1 Web/HTTP, 2 Git, 3 JavaScript, 4 TypeScript, 5 HTML/CSS, 6 React, 7 Next.js, 8 Node/Express, 9 SQL/MongoDB, 10 Python, 11 FastAPI, 12 LLM basics, 13 RAG, 14 Agents, 15 Security, 16 Docker/Cloud/CI, 17 System design, 18 DSA, 19 Behavioural and project questions.

---

## 1. Web and HTTP

**Topics to know:** URL journey, DNS, TCP, TLS, HTTP methods, status codes, headers, cookies, caching, CORS, REST, HTTPS.

**Q: What happens when you type a URL and press Enter?**
A: DNS resolves the name to an IP, TCP connects, TLS encrypts, the browser sends an HTTP request, the server replies, and the browser parses HTML, loads CSS/JS/images and renders.

**Q: 401 vs 403?**
A: 401 means not authenticated (missing or invalid credentials). 403 means authenticated but not allowed.

**Q: GET vs POST vs PUT vs PATCH vs DELETE?**
A: GET reads, POST creates or triggers an action, PUT replaces a whole resource, PATCH updates part of it, DELETE removes it.

**Q: What is idempotency?**
A: Repeating the same request gives the same end state. GET, PUT and DELETE are idempotent. POST usually isn't, so payments use idempotency keys.

**Q: Which status codes should you know?**
A: 200 OK, 201 Created, 204 No Content, 301/302 redirects, 304 Not Modified, 400 Bad Request, 401, 403, 404, 409 Conflict, 422 Unprocessable, 429 Too Many Requests, 500, 502, 503.

**Q: What is CORS?**
A: A browser rule that blocks a page from reading responses from another origin unless the server sends `Access-Control-Allow-Origin` (and related headers). The fix is on the server. It is not a security control for your API.

**Q: Cookies vs localStorage vs sessionStorage?**
A: Cookies are sent with every request and can be `HttpOnly`, `Secure`, `SameSite`. localStorage persists but any script can read it (XSS risk). sessionStorage lasts one tab.

**Q: How does HTTP caching work?**
A: `Cache-Control` (`max-age`, `no-cache` = revalidate, `no-store` = never store), plus `ETag`/`If-None-Match` for 304 responses.

**Q: HTTP/1.1 vs HTTP/2?**
A: HTTP/2 multiplexes many requests on one connection and compresses headers.

**Q: REST vs GraphQL?**
A: REST has many resource URLs. GraphQL has one endpoint where the client picks fields. GraphQL avoids over-fetching but adds caching and complexity costs.

**Q: What does the "S" in HTTPS do?**
A: TLS encrypts traffic, proves the server's identity with a certificate and prevents tampering.

---

## 2. Git

**Topics to know:** commit, branch, merge, rebase, conflicts, stash, reset vs revert, `.gitignore`, pull requests, leaked secrets.

**Q: merge vs rebase?**
A: Merge keeps history and adds a merge commit. Rebase replays your commits on top of another branch for a linear history. Never rebase shared branches.

**Q: reset vs revert?**
A: `reset` moves the branch pointer and rewrites history (local use). `revert` adds a new commit that undoes a change (safe for shared branches).

**Q: fetch vs pull?**
A: `fetch` downloads remote changes only. `pull` = fetch + merge (or rebase).

**Q: How do you resolve a merge conflict?**
A: Open the conflicted files, choose or combine the right code, remove the markers, `git add`, then commit or continue the merge.

**Q: What is `git stash`?**
A: It shelves uncommitted changes so you can switch branches, and you restore them later with `stash pop`.

**Q: You committed an API key. What now?**
A: Revoke and rotate the key first. Then remove it from the code and, if needed, from history. Assume it is already compromised.

**Q: What does `.gitignore` do?**
A: It stops Git tracking listed files such as `node_modules` and `.env`. It does not untrack files already committed (use `git rm --cached`).

---

## 3. JavaScript

**Topics to know:** scope, hoisting, closures, `this`, prototypes, event loop, promises, async/await, array methods, immutability, modules, error handling, debounce/throttle.

**Q: `var` vs `let` vs `const`?**
A: `var` is function-scoped and hoisted as undefined. `let` and `const` are block-scoped with a temporal dead zone. `const` can't be reassigned, but objects it holds can still change.

**Q: `==` vs `===`?**
A: `==` coerces types, `===` doesn't. Use `===`.

**Q: What is a closure?**
A: A function that remembers variables from the scope where it was created, even after that scope has finished.

**Q: How does `this` work?**
A: In a normal function it depends on how the function is called. Arrow functions take `this` from where they are defined. `call`, `apply` and `bind` set it explicitly.

**Q: Explain the event loop.**
A: JS runs one call stack. Async work is handed off, and callbacks queue up. After each task, all microtasks (promises) run before the next macrotask (`setTimeout`).

**Q: Output order: `console.log(1); setTimeout(()=>console.log(2),0); Promise.resolve().then(()=>console.log(3)); console.log(4);`**
A: 1, 4, 3, 2. Sync first, then the microtask, then the timer.

**Q: Promise vs async/await?**
A: async/await is syntax over promises. It reads like sync code, and errors are caught with `try/catch`.

**Q: `Promise.all` vs `allSettled` vs `race` vs `any`?**
A: `all` rejects on the first failure. `allSettled` waits for everything and reports each result. `race` takes the first to settle. `any` takes the first to succeed.

**Q: Does `fetch` reject on a 404?**
A: No. It only rejects on network failure. Check `response.ok` yourself.

**Q: `map` vs `filter` vs `reduce` vs `forEach`?**
A: `map` transforms each item, `filter` keeps some, `reduce` folds into one value, `forEach` just runs a side effect and returns nothing.

**Q: Shallow vs deep copy?**
A: Spread and `Object.assign` copy one level only. `structuredClone` makes a deep copy.

**Q: Primitive vs reference types?**
A: Primitives are copied by value. Objects, arrays and functions are copied by reference.

**Q: What is prototypal inheritance?**
A: Objects link to a prototype and look up missing properties along that chain. `class` is syntax over it.

**Q: Debounce vs throttle?**
A: Debounce waits until activity stops (search box). Throttle runs at most once per interval (scroll handler).

**Q: ES modules vs CommonJS?**
A: ESM uses `import`/`export` and is statically analysable. CommonJS uses `require` and `module.exports` and loads synchronously.

**Q: `null` vs `undefined`?**
A: `undefined` means a value was never assigned. `null` means an intentional empty value.

**Q: What is event delegation?**
A: One listener on a parent handles events from many children by using bubbling and `event.target`.

**Q: What causes memory leaks in JS?**
A: Forgotten listeners or timers, long-lived references and closures holding large objects.

**Q: `??` vs `||`, and `?.`?**
A: `??` falls back only for null/undefined, `||` falls back for any falsy value (0, ""). `?.` safely reads through null/undefined.

---

## 4. TypeScript

**Topics to know:** inference, interfaces vs types, unions, narrowing, generics, utility types, `unknown`, discriminated unions, strict mode, typing React.

**Q: Why TypeScript?**
A: It catches type errors at compile time, improves editor help and documents intent. Types are erased at runtime.

**Q: `interface` vs `type`?**
A: Both describe shapes. Interfaces can be extended and merged. Types can also express unions, tuples and mapped types.

**Q: `any` vs `unknown`?**
A: `any` turns checking off. `unknown` is safe: you must narrow it before use.

**Q: What are `never` and `void`?**
A: `void` is "returns nothing". `never` is "never returns" (throws) or an impossible case, useful for exhaustive checks.

**Q: What are generics?**
A: Type parameters that let one function or type work with many types while staying type-safe, e.g. `function first<T>(a: T[]): T`.

**Q: Union, intersection, narrowing?**
A: `A | B` is either, `A & B` is both. Narrowing uses `typeof`, `in`, `instanceof` or a discriminant field to pick the exact type.

**Q: What is a discriminated union?**
A: A union where each member has a shared literal field (e.g. `status: "ok" | "error"`) that lets TS narrow safely.

**Q: Common utility types?**
A: `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `ReturnType`.

**Q: Does TypeScript validate API data at runtime?**
A: No. Use a runtime validator (e.g. Zod) at the boundary.

**Q: Why enable `strict`?**
A: It turns on null checks and other rules that catch real bugs.

---

## 5. HTML and CSS

**Topics to know:** semantic HTML, forms, accessibility, box model, specificity, flexbox, grid, positioning, responsive design, Core Web Vitals.

**Q: Why semantic HTML?**
A: Screen readers, SEO and maintainability. `nav`, `main`, `button` carry meaning that `div` doesn't.

**Q: Explain the box model.**
A: content + padding + border + margin. `box-sizing: border-box` makes `width` include padding and border.

**Q: How does CSS specificity work?**
A: Inline > ID > class/attribute/pseudo-class > element. Equal specificity: the later rule wins. `!important` overrides, so avoid it.

**Q: Flexbox vs Grid?**
A: Flexbox lays out in one dimension (row or column). Grid does two dimensions (rows and columns).

**Q: `position` values?**
A: `static` (default), `relative`, `absolute` (to nearest positioned ancestor), `fixed` (to the viewport), `sticky` (sticks after a scroll threshold).

**Q: `display: none` vs `visibility: hidden`?**
A: `none` removes the element from layout. `hidden` keeps the space.

**Q: `rem` vs `em` vs `px`?**
A: `rem` scales with the root font size, `em` with the parent's, `px` is fixed.

**Q: What is a stacking context?**
A: A group that `z-index` is compared within. Created by `position` + `z-index`, `opacity < 1`, `transform` and more.

**Q: How do you make a site responsive?**
A: Mobile-first CSS, flexible units, Grid/Flex, `min()`/`clamp()`, and media queries for breakpoints.

**Q: Accessibility basics?**
A: Labels on inputs, alt text, keyboard focus and visible focus styles, sufficient contrast, correct ARIA only when native HTML can't do it.

**Q: What are Core Web Vitals?**
A: LCP (loading), INP (responsiveness), CLS (layout stability).

**Q: How to improve page speed?**
A: Optimise images, lazy-load below the fold, code-split, cache, reduce JS and avoid layout shifts.

---

## 6. React

**Topics to know:** rendering, state/props, keys, hooks, effects, context, memoization, forms, error boundaries, data fetching, testing.

**Q: What is the virtual DOM and reconciliation?**
A: React builds a lightweight tree of your UI, diffs it with the previous one and updates only the real DOM parts that changed.

**Q: Why do lists need `key`?**
A: Keys let React match items between renders. Index keys break state when items reorder, insert or delete.

**Q: State vs props?**
A: Props are inputs from the parent (read-only). State is data owned by the component that changes over time.

**Q: Why not mutate state directly?**
A: React detects changes by reference, so mutation may not re-render and breaks predictable updates. Create new objects/arrays.

**Q: Controlled vs uncontrolled inputs?**
A: Controlled inputs get their value from React state. Uncontrolled ones keep it in the DOM, read via a ref.

**Q: How does `useEffect` work, and what does the dependency array do?**
A: It runs after render. It re-runs when a listed dependency changes. `[]` runs once on mount. The returned function is cleanup.

**Q: When should you NOT use `useEffect`?**
A: For derived data (compute it during render) and for responding to user events (use handlers).

**Q: What is a stale closure?**
A: A callback that captured old state or props. Fix it with correct dependencies or functional updates (`setN(n => n + 1)`).

**Q: `useMemo` vs `useCallback` vs `React.memo`?**
A: `useMemo` caches a computed value, `useCallback` caches a function, `React.memo` skips re-rendering when props are unchanged. Use them after measuring, not by default.

**Q: `useRef`?**
A: A mutable box that survives renders without causing re-renders. It's used for DOM nodes and timers.

**Q: `useState` vs `useReducer`?**
A: `useReducer` fits complex state with many related transitions.

**Q: Context API drawbacks?**
A: Every consumer re-renders when the value changes. Split contexts or use a state library for frequently changing data.

**Q: What is lifting state up?**
A: Moving shared state to the nearest common parent and passing it down.

**Q: What are error boundaries?**
A: Components that catch render errors in their children and show a fallback. They don't catch event-handler or async errors.

**Q: Why does StrictMode run effects twice in development?**
A: To expose missing cleanup and impure code. It doesn't happen in production.

**Q: How do you fetch data safely in a component?**
A: Handle loading, error and empty states, and cancel or ignore stale requests with `AbortController` or a cleanup flag. Or use a data library.

**Q: What is a custom hook?**
A: A function starting with `use` that reuses stateful logic between components.

**Q: Server Components vs Client Components?**
A: Server Components render on the server and send no JS for themselves. Client Components run in the browser for interactivity and state.

---

## 7. Next.js (App Router)

**Topics to know:** routing, layouts, Server vs Client Components, rendering modes, data fetching and caching, Server Actions, Route Handlers, auth, metadata, env vars.

**Q: SSR vs SSG vs CSR vs ISR?**
A: SSR renders per request on the server. SSG renders at build time. CSR renders in the browser. ISR re-generates static pages after a time or on demand.

**Q: What does `"use client"` do?**
A: It marks a module as the client boundary: that component and what it imports run in the browser.

**Q: Server Actions vs Route Handlers?**
A: Server Actions are server functions called from forms and components for mutations. Route Handlers are HTTP endpoints (`route.js`) for external clients and webhooks.

**Q: Why are secrets safe in Server Components but not in `NEXT_PUBLIC_` variables?**
A: `NEXT_PUBLIC_` values are inlined into browser JS, so anyone can read them. Server-only variables stay on the server.

**Q: What is a hydration mismatch?**
A: Server HTML differs from what the client renders first (e.g. dates, `Math.random`, `window` checks).

**Q: How is caching handled in current Next.js?**
A: It has changed between major versions. Check the current docs for the version you use, because older tutorials describe different defaults.

**Q: What are `layout`, `loading`, `error` and `not-found` files?**
A: Special files: shared shell, Suspense fallback, error boundary and 404 UI for a route segment.

**Q: How do you protect pages?**
A: Verify the session on the server (in the data layer and Server Actions), and use redirects or the proxy/middleware only as a first check.

**Q: Why use `next/image`?**
A: Automatic resizing, modern formats, lazy loading and layout-shift prevention.

**Q: Where should filters, search and pagination state live?**
A: In URL query parameters, so pages are shareable and work with refresh and back/forward.

---

## 8. Node.js and Express

**Topics to know:** event loop, middleware, REST design, auth (sessions, JWT), validation, error handling, rate limiting, security headers, file uploads, testing.

**Q: Why is Node good for I/O-heavy apps?**
A: A single-threaded event loop with non-blocking I/O handles many connections cheaply.

**Q: What blocks the event loop?**
A: CPU-heavy synchronous work (big loops, JSON on huge payloads, sync fs calls). Use worker threads or a queue.

**Q: What is middleware?**
A: A function `(req, res, next)` in a chain. Order matters: logging, parsing, auth, routes, then error handler.

**Q: How does Express error handling work?**
A: An error middleware has four arguments `(err, req, res, next)` and is registered last. In Express 5, rejected promises from async handlers are forwarded automatically.

**Q: Sessions vs JWT?**
A: Sessions store state on the server and use a cookie ID (easy to revoke). JWTs are signed, self-contained tokens (stateless, but revocation is hard).

**Q: JWT access vs refresh tokens?**
A: A short-lived access token calls the API. A longer-lived refresh token gets new access tokens and should be stored safely and rotated.

**Q: Authentication vs authorization?**
A: Authentication is who you are. Authorization is what you may do.

**Q: How do you store passwords?**
A: Hash with a slow, salted algorithm (argon2 or bcrypt). Never encrypt or store them in plain text.

**Q: What is RBAC?**
A: Role-based access control: permissions are granted to roles, and users get roles. Add resource-level checks too (owner-only data).

**Q: Offset vs cursor pagination?**
A: Offset (`page`, `limit`) is simple but slow and unstable on large or changing data. Cursor pagination uses the last seen key and is faster and stable.

**Q: How do you validate input?**
A: With a schema library (Zod/Joi) at the edge, and reject bad data with 400/422.

**Q: How do you prevent abuse?**
A: Rate limiting, request size limits, auth, brute-force protection on login and CAPTCHA where needed.

**Q: `process.nextTick` vs `setImmediate`?**
A: `nextTick` runs right after the current operation, before promise microtasks. `setImmediate` runs in the check phase after I/O.

**Q: What are streams?**
A: Process data in chunks instead of loading it all into memory (large files, uploads).

**Q: What belongs in a controller vs a service?**
A: Controller: HTTP in/out. Service: business logic. Repository: database access.

**Q: When use a separate backend instead of Next.js Route Handlers?**
A: Multiple clients, long-running jobs, heavy business logic, independent scaling or a different language team.

---

## 9. SQL and MongoDB

**Topics to know:** keys, joins, grouping, indexes, query plans, transactions, isolation, normalisation, migrations, pooling, Mongo schema design.

**Q: Primary key vs foreign key?**
A: A primary key uniquely identifies a row. A foreign key references another table's key and enforces the relationship.

**Q: Types of JOIN?**
A: INNER (matches only), LEFT (all left rows plus matches), RIGHT, FULL, and CROSS (all combinations).

**Q: `WHERE` vs `HAVING`?**
A: `WHERE` filters rows before grouping. `HAVING` filters groups after aggregation.

**Q: What is an index, and its cost?**
A: A structure (usually a B-tree) that speeds up lookups. It costs extra storage and slower writes.

**Q: How do you debug a slow query?**
A: Run `EXPLAIN ANALYZE`, look for sequential scans on big tables, add or fix indexes, and avoid selecting unneeded columns.

**Q: What is ACID?**
A: Atomicity, Consistency, Isolation, Durability: the guarantees of a transaction.

**Q: Isolation levels?**
A: Read Committed (PostgreSQL default), Repeatable Read and Serializable. Higher levels prevent more anomalies (dirty, non-repeatable and phantom reads) with more cost.

**Q: What is the N+1 problem?**
A: One query for a list plus one extra query per item. Fix with a join, eager loading or batching.

**Q: Normalisation?**
A: Structure data so each fact is stored once, to avoid anomalies. Denormalise deliberately for read speed.

**Q: `UNION` vs `UNION ALL`?**
A: `UNION` removes duplicates. `UNION ALL` keeps them and is faster.

**Q: `DELETE` vs `TRUNCATE`?**
A: `DELETE` removes chosen rows (logged, can use `WHERE`). `TRUNCATE` empties the whole table fast.

**Q: What is a CTE?**
A: A named temporary result (`WITH x AS (...)`) that makes complex queries readable.

**Q: What is a deadlock?**
A: Two transactions wait for each other's locks. The DB aborts one. Reduce risk by locking in a consistent order and keeping transactions short.

**Q: What is connection pooling?**
A: Reusing a limited set of DB connections instead of opening one per request.

**Q: Why use migrations?**
A: They version schema changes so every environment can be upgraded and reproduced.

**Q: SQL vs MongoDB: when each?**
A: Relational, consistent, relationship-heavy data (orders, payments) fits PostgreSQL. Flexible, document-shaped data with simple access patterns fits MongoDB.

**Q: Embed vs reference in MongoDB?**
A: Embed data read together and bounded in size. Reference data that is large, shared or grows without limit.

**Q: What is a MongoDB aggregation pipeline?**
A: A sequence of stages (`$match`, `$group`, `$sort`, `$lookup`…) that transforms documents.

---

## 10. Python

**Topics to know:** data types, comprehensions, functions, OOP, dataclasses, generators, decorators, exceptions, context managers, typing, venv/pip/uv, asyncio, pytest.

**Q: List vs tuple vs set vs dict?**
A: List is ordered and mutable. Tuple is ordered and immutable. Set is unique and unordered. Dict maps keys to values.

**Q: Mutable default argument pitfall?**
A: `def f(x=[])` shares one list across calls. Use `None` and create the list inside.

**Q: `is` vs `==`?**
A: `==` compares values. `is` compares identity (same object).

**Q: What are `*args` and `**kwargs`?**
A: Collect extra positional arguments into a tuple and keyword arguments into a dict.

**Q: List comprehension?**
A: A compact loop: `[x*x for x in nums if x > 0]`.

**Q: Generator vs list?**
A: A generator (`yield`) produces values lazily, one at a time, saving memory.

**Q: What is a decorator?**
A: A function that wraps another function to add behaviour (logging, caching, auth).

**Q: What is a context manager?**
A: An object used with `with` that sets up and cleans up (files, locks). It is implemented by `__enter__/__exit__` or `@contextmanager`.

**Q: What is the GIL?**
A: In standard CPython, a lock lets only one thread run Python bytecode at a time. Threads help I/O work, not CPU work (use processes). A free-threaded build exists in newer versions.

**Q: Shallow vs deep copy?**
A: `copy.copy` copies the outer object. `copy.deepcopy` copies nested objects too.

**Q: What are type hints?**
A: Optional annotations (`def f(x: int) -> str`) checked by tools like mypy or pyright, not enforced at runtime.

**Q: `dataclass`?**
A: A decorator that generates `__init__`, `__repr__` and `__eq__` for data-holding classes.

**Q: How do you manage dependencies?**
A: A virtual environment per project plus `pip` or `uv`, with dependencies in `pyproject.toml` or a lock file.

**Q: `async def` and `await`?**
A: Coroutines run on an event loop (`asyncio`) and yield while waiting for I/O, so one thread can handle many tasks.

**Q: Composition vs inheritance?**
A: Prefer composition ("has a") for flexibility. Use inheritance for a true "is a" relationship.

**Q: How do you test in Python?**
A: `pytest` with fixtures, parametrised tests and mocks for external calls.

**Q: JavaScript vs Python quick differences?**
A: Python uses indentation, `None`, `True/False`, no `++`, dict/list literals, and 2 things to watch: truthiness of empty containers and mutable defaults.

---

## 11. FastAPI

**Topics to know:** routes, Pydantic, dependency injection, async vs sync, SQLAlchemy/SQLModel, Alembic, auth, background tasks, testing, project structure, deployment.

**Q: What is FastAPI built on?**
A: Starlette (web layer) and Pydantic (validation), served by an ASGI server like Uvicorn.

**Q: ASGI vs WSGI?**
A: ASGI supports async, WebSockets and streaming. WSGI is the older synchronous standard.

**Q: What does Pydantic do?**
A: It validates and converts request/response data from type hints, and produces clear errors (FastAPI returns 422).

**Q: How does dependency injection work?**
A: `Depends(func)` runs a function and passes its result into your route: DB sessions, current user, settings. It is easy to override in tests.

**Q: `def` vs `async def` routes?**
A: `async def` runs on the event loop, so never block it with sync I/O. Plain `def` runs in a thread pool.

**Q: What is `response_model` for?**
A: It filters and documents the output (e.g. hide the password hash).

**Q: Path vs query vs body parameters?**
A: Path identifies the resource (`/orders/5`), query filters (`?status=paid`), body carries the data (JSON).

**Q: How do you handle auth?**
A: OAuth2 password flow or bearer tokens with JWT, password hashing (argon2/bcrypt), and a dependency that returns the current user and checks roles.

**Q: SQLAlchemy vs SQLModel?**
A: SQLAlchemy is the mature, full ORM. SQLModel combines SQLAlchemy and Pydantic for simpler small projects.

**Q: What does Alembic do?**
A: Database migrations for SQLAlchemy models: generate, review, apply and roll back schema changes.

**Q: How do you test FastAPI?**
A: `TestClient` (or `httpx`) with `pytest`, a test database and `app.dependency_overrides` for the DB and auth.

**Q: `BackgroundTasks` vs a task queue?**
A: Background tasks run after the response inside the same process. For reliable, retryable or heavy jobs, use a queue (Celery, ARQ, etc.).

**Q: How do you structure a project?**
A: `routers/` (HTTP), `schemas/` (Pydantic), `models/` (DB), `services/` (logic), `core/` (config, security), `db/` (session), `tests/`.

**Q: Production checklist?**
A: Env-based settings, migrations, logging, health check, CORS config, timeouts, workers, HTTPS and a non-root container.

---

## 12. LLM basics

**Topics to know:** tokens, context window, temperature, embeddings, hallucination, prompting, structured output, tool calling, streaming, cost/latency, evals.

**Q: What is an LLM?**
A: A neural network trained on lots of text to predict the next token. It generates text one token at a time.

**Q: What is a token?**
A: A chunk of text (word piece). Pricing and limits are counted in tokens.

**Q: What is the context window?**
A: The maximum tokens (prompt + history + output) the model can consider at once.

**Q: What does temperature do?**
A: It controls randomness. Low gives more deterministic output, high gives more varied output. Some newer models restrict it, so check the docs.

**Q: What are embeddings?**
A: Vectors that represent meaning, so similar texts are close together. Used for search and RAG.

**Q: What is a hallucination, and how do you reduce it?**
A: A confident but wrong answer. Reduce it by grounding with retrieved sources, requiring citations, allowing "I don't know", and evaluating outputs.

**Q: Prompting vs RAG vs fine-tuning?**
A: Prompting steers behaviour. RAG adds fresh or private knowledge at query time. Fine-tuning changes model behaviour or style and is rarely the first step.

**Q: What is a system prompt?**
A: Top-level instructions that set role, rules and format for the conversation.

**Q: How do you get reliable structured output?**
A: Use the provider's structured-output or JSON-schema feature, and validate the result with Pydantic/Zod before using it.

**Q: What is tool (function) calling?**
A: The model returns a request to call a tool with arguments. Your code runs it and sends back the result.

**Q: Why stream responses?**
A: Users see text sooner, so the app feels faster, though total time is similar.

**Q: How do you control cost and latency?**
A: Choose a smaller model where possible, trim context, cache, set max output tokens, batch and monitor usage.

**Q: How do you handle rate limits and failures?**
A: Timeouts, retries with exponential backoff and jitter, fallbacks and clear errors.

**Q: How do you evaluate an LLM feature?**
A: Build a test set of real examples with expected outcomes, score automatically plus human spot checks, and re-run after prompt/model changes.

**Q: Hosted vs local models?**
A: Hosted: best quality, easy, data leaves your system. Local: privacy and control, but you run and scale it.

---

## 13. RAG

**Topics to know:** ingestion, chunking, embeddings, vector search, pgvector, hybrid search, reranking, citations, access control, evaluation, prompt injection.

**Q: What is RAG?**
A: Retrieval-Augmented Generation: retrieve relevant passages from your data, add them to the prompt, and have the model answer from them.

**Q: Describe the RAG pipeline.**
A: Ingest (extract text) → chunk → embed → store with metadata → at query time embed the question → retrieve top-k → build prompt → generate with citations.

**Q: How do you choose chunk size and overlap?**
A: Test on your data. Smaller chunks are more precise, larger keep context. Overlap stops ideas being cut at boundaries.

**Q: Why not just keyword search?**
A: Keywords miss synonyms and meaning. Semantic search matches meaning. Hybrid (both) is often best.

**Q: What is cosine similarity?**
A: A measure of how close two vectors' directions are, used to rank similar chunks.

**Q: What is reranking?**
A: A second model re-scores the top retrieved chunks for relevance before generation.

**Q: pgvector vs a dedicated vector DB?**
A: pgvector keeps vectors with your relational data (simple, transactional). Dedicated DBs can scale and tune further at the cost of another system.

**Q: How do you enforce per-user document access?**
A: Store owner/permission metadata and filter in the retrieval query itself, never only in the prompt.

**Q: How do you evaluate RAG?**
A: Retrieval: recall@k, MRR. Answers: groundedness, citation correctness and answer quality on a labelled question set.

**Q: What is prompt injection in documents?**
A: Text inside a retrieved document tries to give the model new instructions. Treat retrieved text as untrusted data and limit tool permissions.

**Q: What if retrieval finds nothing relevant?**
A: Use a similarity threshold and answer "I don't have that information" instead of guessing.

**Q: Common RAG failures?**
A: Bad chunking, missing metadata, wrong top-k, stale index, and no evaluation.

---

## 14. Agents (and LangGraph)

**Topics to know:** workflow vs agent, tool loop, state, memory, guardrails, human approval, idempotency, budgets, tracing, LangGraph basics.

**Q: Workflow vs agent?**
A: A workflow follows code-defined steps. An agent lets the model choose the next action in a loop. Use the simplest one that works.

**Q: How does a basic agent loop work?**
A: Send messages and tools → model asks for a tool → run it → return the result → repeat until a final answer or a step limit.

**Q: How do you keep agents safe?**
A: Least-privilege tools, argument validation, step/time/cost budgets, human approval for risky actions, audit logs and permission checks outside the model.

**Q: Why does idempotency matter for agents?**
A: Retries or repeated tool calls must not duplicate actions like refunds. Use idempotency keys.

**Q: What is human-in-the-loop?**
A: Pausing before consequential actions so a person approves, edits or rejects.

**Q: What are LangGraph's core ideas?**
A: A graph of nodes (functions) and edges (including conditional ones) over shared state, with checkpointing, interrupts, streaming and persistence.

**Q: When is LangGraph worth it vs a plain loop?**
A: When you need durable state, branching, pauses for approval or resumable runs. A simple tool loop is enough for small cases.

**Q: Do you need multi-agent systems?**
A: Usually not. Add agents only when one agent's context or responsibilities clearly become too much.

**Q: How do you debug and evaluate agents?**
A: Trace every step (inputs, tool calls, results), build scenario tests, and track success rate, cost and failure modes.

**Q: What is memory in an agent?**
A: Short-term is conversation/state in context. Long-term is stored facts retrieved when needed.

---

## 15. Security

**Topics to know:** OWASP Top 10, injection, XSS, CSRF, auth, secrets, rate limiting, uploads, logging, dependency risks, LLM-specific risks.

**Q: SQL injection and prevention?**
A: Attacker input becomes part of a query. Prevent it with parameterised queries or an ORM, never string concatenation.

**Q: XSS and prevention?**
A: Injected script runs in a user's browser. Escape output, avoid `dangerouslySetInnerHTML`, use a CSP and sanitise any HTML you must allow.

**Q: CSRF and prevention?**
A: A malicious site makes the browser send an authenticated request. Use `SameSite` cookies, CSRF tokens and check the origin.

**Q: Where should tokens be stored?**
A: Prefer `HttpOnly`, `Secure`, `SameSite` cookies. localStorage is readable by any XSS.

**Q: How do you handle secrets?**
A: Environment variables or a secrets manager, never in Git, rotate on leak, least-privilege keys.

**Q: Is CORS a security feature?**
A: No. It only controls what browsers let pages read. Server-side auth is what protects the API.

**Q: What is SSRF?**
A: Tricking your server into requesting internal or arbitrary URLs. Validate and allow-list outbound targets.

**Q: How do you secure file uploads?**
A: Limit size and type, check content not just extension, store outside the web root or in object storage, rename files and scan if needed.

**Q: What should you not log?**
A: Passwords, tokens, API keys and sensitive personal data.

**Q: What is least privilege?**
A: Every user, service and key gets only the permissions it needs.

**Q: AI-specific risks?**
A: Prompt injection, data leakage across users, unsafe tool calls and over-trusting model output. Validate outputs and gate actions.

**Q: How do you manage dependency risk?**
A: Lock files, regular updates, `npm audit`/`pip-audit`, and review new packages.

---

## 16. Docker, Cloud and CI/CD

**Topics to know:** images, containers, Dockerfile, volumes, Compose, CI/CD, GitHub Actions, AWS core services (IAM, EC2, S3, RDS, CloudWatch), HTTPS, monitoring, rollback.

**Q: Image vs container?**
A: An image is a read-only template. A container is a running instance of it.

**Q: Why order Dockerfile steps carefully?**
A: Layers are cached. Copy dependency files and install first, then copy source, so code changes don't reinstall everything.

**Q: What is a multi-stage build?**
A: Build in one stage and copy only the output into a small final image.

**Q: Volumes?**
A: Persist data outside the container's life.

**Q: What is Docker Compose?**
A: A file that defines and runs several containers (app, DB) together.

**Q: What is CI/CD?**
A: CI automatically builds and tests every change. CD automatically (or with approval) deploys it.

**Q: What does a basic GitHub Actions pipeline do?**
A: On push or PR: install, lint, test, build, and optionally deploy.

**Q: AWS services to know first?**
A: IAM (permissions), EC2 (servers), S3 (object storage), RDS (managed DB), CloudWatch (logs/metrics), plus Route 53 and certificates for domains and HTTPS.

**Q: What is IAM best practice?**
A: Least privilege, roles instead of long-lived keys, MFA, and no root account use.

**Q: How do you avoid surprise cloud bills?**
A: Budgets and alerts, tag resources, delete unused ones and watch data-transfer costs.

**Q: What is a health check?**
A: An endpoint (e.g. `/health`) that tells the load balancer or orchestrator the app is alive.

**Q: How do you roll back a bad deploy?**
A: Keep previous versioned images and redeploy the last good one. Make migrations backward-compatible.

**Q: Dev vs production config?**
A: Same code, different environment variables, secrets, logging level and resources.

---

## 17. System design

**Topics to know:** requirements, APIs, schema, indexes, caching, queues, scaling, rate limiting, idempotency, reliability, observability, monolith vs microservices.

**Q: How do you approach a design question?**
A: Clarify requirements (functional and non-functional), estimate scale, sketch the API and data model, draw the components, then discuss bottlenecks and trade-offs.

**Q: Vertical vs horizontal scaling?**
A: Vertical = bigger machine. Horizontal = more machines behind a load balancer (needs stateless services).

**Q: Where do you add caching?**
A: Browser/CDN, application (Redis) and the database layer. Handle invalidation and TTLs.

**Q: When use a queue?**
A: For slow or retryable work (emails, document processing, AI jobs) so requests return fast and spikes are smoothed.

**Q: Replication vs sharding?**
A: Replication copies data for reads and availability. Sharding splits data across nodes to scale writes and size.

**Q: What is CAP, in short?**
A: In a network partition you must choose between consistency and availability.

**Q: Monolith vs microservices?**
A: Start with a modular monolith. Move to microservices only for independent scaling or team boundaries, since they add operational cost.

**Q: How do you make an API reliable?**
A: Timeouts, retries with backoff, idempotency, rate limits, health checks and graceful degradation.

**Q: How do you observe a system?**
A: Logs, metrics and traces, with alerts on user-facing symptoms.

**Q: Design an AI document assistant (outline).**
A: Upload to object storage → queue extraction/chunking/embedding → store vectors with owner metadata → retrieve with access filters → generate with citations → log cost and run evals.

**Q: Design an order management system (outline).**
A: Users, products, orders, order_items, payments tables. Auth + RBAC, idempotent order creation, transactions for stock and payment, indexed queries and pagination.

**Q: Design an AI support assistant with approvals (outline).**
A: Retrieval for policy, tools for order lookup, a state machine for refund steps, human approval before money moves, audit logs and idempotency keys.

---

## 18. Data structures and algorithms (realistic scope)

**Topics to know:** Big-O, arrays, hash maps/sets, strings, two pointers, sliding window, stack/queue, linked list basics, binary search, recursion, trees (BFS/DFS), sorting basics, simple dynamic programming.

**Q: What is Big-O?**
A: How time or space grows as input grows (O(1), O(log n), O(n), O(n log n), O(n²)).

**Q: Why are hash maps useful?**
A: Average O(1) lookup, insert and delete. They're the first tool for counting, grouping and "seen before" problems.

**Q: Two pointers vs sliding window?**
A: Two pointers moves from both ends or at different speeds. Sliding window keeps a moving range over a sequence.

**Q: Stack vs queue?**
A: Stack is LIFO (undo, matching brackets). Queue is FIFO (task order, BFS).

**Q: BFS vs DFS?**
A: BFS explores level by level with a queue (shortest path in unweighted graphs). DFS goes deep with recursion or a stack.

**Q: When does binary search apply?**
A: On sorted data (or a monotonic condition), halving the range each step for O(log n).

**Q: Practice plan?**
A: About 5 problems a week on arrays/hash maps, then pointers/windows, then trees. Explain your approach before coding.

---

## 19. Behavioural and project questions

**Topics to know:** STAR method, explaining projects, trade-offs, failures and learning, working with AI tools.

**Q: Walk me through a project.**
A: Problem → your role → architecture → one hard decision and why → result → what you'd change.

**Q: Tell me about a bug you debugged.**
A: Use STAR: situation, task, action (how you isolated it), result (fix plus how you prevented a repeat).

**Q: How do you work with AI tools?**
A: AI drafts boilerplate and suggestions. I write and understand the core logic, verify against official docs, test everything and review for security.

**Q: How do you handle disagreement?**
A: Listen, state trade-offs with evidence, decide by the goal, then commit to the decision.

**Q: Why are you moving toward AI engineering?**
A: Be honest and specific: your React/Node base, what you built in the projects, and what problem you want to solve.

**Q: What would you improve in your own project?**
A: Name real gaps (tests, monitoring, security, cost) and how you would fix them. This shows maturity.

**Q: How do you learn a new technology quickly?**
A: Official docs first, a tiny project, then compare with what I already know and note the pitfalls.

---

## Interview-day checklist

- [ ] Can explain the URL journey, the event loop and a closure without notes
- [ ] Can write a SQL join with GROUP BY from memory
- [ ] Can explain one project end to end, with one trade-off and one failure
- [ ] Can describe a RAG pipeline and an agent loop in 2 minutes each
- [ ] Have a short "why this role" answer and two questions for the interviewer
