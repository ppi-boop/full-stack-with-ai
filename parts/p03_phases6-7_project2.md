# Phase 6 — Backend with Node.js and Express

## Why this phase matters

You already know some Node, auth and API work. This phase is about depth: knowing why the code works, not only how to copy it. Most production bugs in backends come from five places: bad input handling, wrong status codes, broken auth and permission checks, unhandled async errors, and slow or unsafe database access. If you can reason about those on a plain Express server, every other backend framework (FastAPI in Phase 9, NestJS, Next.js Route Handlers) becomes easy to learn, because they all solve the same problems. Research date for this phase: 2026-10-09.

> **Honest note:** Many Express tutorials online were written for Express 4. As of 2026-10-09 the npm `latest` tag of `express` is **5.3.0** (the `latest-4` tag is 4.22.3, checked on the npm registry). Express 5 became the default on npm with 5.1.0 on 2025-03-31 ([announcement](https://expressjs.com/en/blog/2025-03-31-v5-1-latest-release)). So `npm install express` gives you v5 today. Old videos still teach v4 habits. The differences are listed below; read the [official migration guide](https://expressjs.com/en/guide/migrating-5.html) once.

## Prerequisites and "skip test"

You can skip a topic below only if you can demonstrate it, without looking at docs:

- Create a Node project with `npm init`, install a package, and explain `dependencies` vs `devDependencies` and what `package-lock.json` is for.
- Write a plain `node:http` server that returns JSON for two routes and a 404 for others.
- Explain in 60 seconds what the event loop does when your code awaits a database call.
- Build an Express route that reads a JSON body, validates it, and returns `201` with a created object.
- Explain the difference between 401 and 403, and between a cookie and a JWT.
- Hash a password and verify it, and explain why a fast hash like SHA-256 is wrong for passwords.

If you fail two or more, read the whole phase in order. If you pass all six, skim the concepts and spend your time on Project 2.

## Concepts explained

### Node runtime and the event-driven model

**[Must learn now]** Node.js runs your JavaScript on the V8 engine and adds things the browser does not have: files, network sockets, processes. It is single-threaded for your JavaScript code, but the operating system and a small thread pool (libuv) do slow I/O work in the background. When I/O finishes, a callback or promise continuation is queued for the event loop to run.

Analogy: a restaurant with one waiter (your JS thread) and a kitchen (the OS). The waiter takes an order, sends it to the kitchen, and serves other tables while waiting. If the waiter personally cooks a 5-minute dish (a heavy loop), every table waits.

Practical rule: never block the event loop. Avoid `fs.readFileSync` in request handlers, huge `JSON.parse` on big payloads, sync crypto, and long `for` loops. CPU-heavy work goes to worker threads or a separate service.

```js
// BAD: blocks every other request for the whole loop
app.get("/slow", (req, res) => {
  let n = 0;
  for (let i = 0; i < 5e9; i++) n += i;
  res.json({ n });
});
```

**Common mistake:** thinking "async" means "runs in parallel on many threads". It means "does not block while waiting". CPU work is still one at a time.

**Interview questions:** What is the event loop? What is the difference between `process.nextTick`, microtasks and `setImmediate`? Why is Node good for I/O-heavy APIs and weak for CPU-heavy ones? What is `libuv`? Read the official [event loop guide](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick).

### npm, scripts and project setup

**[Must learn now]** `package.json` is the project's ID card: name, scripts, dependencies, and `"type": "module"` (use ES modules, as you do in React). Use `npm ci` in CI (exact lockfile install) and `npm install` locally. Use a current Node LTS (on 2026-10-09 the nodejs.org index lists v24 "Krypton" as LTS). Keep a `.nvmrc` or `engines` field so your team and server use the same version. Run `npm audit` and keep dependencies updated; each dependency is code you are trusting.

**Common mistake:** committing `node_modules` or `.env`; using `npm install` in CI (it can change the lockfile).

**Interview questions:** What is semantic versioning (`^1.2.3` vs `~1.2.3`)? What is a lockfile for? What is a supply-chain attack?

### HTTP server basics (without Express)

**[Must learn now]** Express is a thin layer over Node's `http` module. Building one tiny server by hand shows you what Express hides: a request is a stream, a response is a stream, and you must set status, headers and body yourself.

```js
import { createServer } from "node:http";

createServer((req, res) => {
  if (req.method === "GET" && req.url === "/health") {
    res.writeHead(200, { "Content-Type": "application/json" });
    return res.end(JSON.stringify({ ok: true }));
  }
  res.writeHead(404).end();
}).listen(3000);
```

**Common mistake:** forgetting to end the response, so the client hangs until timeout.

**Interview questions:** What is in an HTTP request? What is a stream and why does it matter for large uploads? What does `keep-alive` do?

### Express installation, routing and Express 5 changes

**[Must learn now]** Express matches the request method and path to a handler. Routers (`express.Router()`) group related routes so `app.js` stays small. See [routing](https://expressjs.com/en/guide/routing.html).

Express 5 versus older tutorials (verified against the [migration guide](https://expressjs.com/en/guide/migrating-5.html)):

| Topic | Express 4 habit in old tutorials | Express 5 reality |
|---|---|---|
| Async errors | Needed `express-async-errors` or try/catch plus `next(err)` | A rejected promise or thrown error in an async handler goes to the error middleware automatically |
| Wildcards | `app.get("/*", ...)` | Must be named: `/*splat` (or `/{*splat}` to also match `/`) |
| Optional segment | `/:id?` | Use braces, for example `/:file{.:ext}` |
| `req.body` | Defaulted to `{}` | `undefined` if no body parser ran; check before use |
| Removed methods | `res.send(obj, status)`, `res.redirect(url, status)`, `app.del()`, `req.param()` | Use `res.status(s).json(obj)`, `res.redirect(s, url)`, `app.delete()` |
| `express.urlencoded` | `extended: true` default | `extended: false` default |
| Node version | Node 0.10+ | Node 18 or higher |

> **Outdated?:** If a tutorial uses `express-async-errors`, `body-parser` as a separate install, `app.del`, or `/*` wildcards, it is Express 4 style. `express.json()` is built in and is what you use now.

```js
import express from "express";
const app = express();
app.use(express.json());           // body parser: JSON
app.get("/health", (req, res) => res.json({ ok: true }));
app.get("/{*splat}", (req, res) => res.status(404).json({ error: "Not found" }));
app.listen(process.env.PORT ?? 3000);
```

**Common mistake:** putting the 404 handler before your routers; order matters in Express.

**Interview questions:** How does Express choose a handler? What changed in Express 5? What is a Router?

### Request, response and middleware

**[Must learn now]** Middleware is a function `(req, res, next)` that runs in order. It can read or change `req`/`res`, end the response, or call `next()` to pass on. Express itself is "a chain of middleware". Analogy: airport security: ID check, bag scan, gate check. Each stage can stop you or wave you on. See [using middleware](https://expressjs.com/en/guide/using-middleware.html) and [writing middleware](https://expressjs.com/en/guide/writing-middleware.html).

Typical global order: request id, logger, security headers, CORS, rate limit, body parser, routes, 404, error handler.

```js
function requestId(req, res, next) {
  req.id = crypto.randomUUID();
  res.setHeader("X-Request-Id", req.id);
  next();
}
```

**Common mistake:** calling `next()` and also sending a response (the "headers already sent" error); forgetting `next()` so the request hangs.

**Interview questions:** What is the difference between application, router and error middleware? Why is middleware order important?

### Project organization: routes, controllers, services, repositories

**[Must learn now]** Split by job so each file has one reason to change:

- **Route**: URL + method + which middleware. No logic.
- **Controller**: reads the HTTP request, calls a service, shapes the HTTP response. Knows about `req`/`res`.
- **Service**: business rules ("an order cannot ship if stock is 0"). Knows nothing about HTTP. Easy to unit test.
- **Repository**: all SQL (or database calls) for one entity. Nothing else touches the database.

Analogy: a shop. The door staff (route), the cashier (controller), the manager who knows the rules (service), the storeroom clerk (repository).

```text
src/modules/orders/
  orders.routes.js       // wiring only
  orders.controller.js   // req/res
  orders.service.js      // rules, transactions
  orders.repository.js   // SQL
  orders.schemas.js      // Zod schemas
  orders.test.js
```

**Common mistake:** "fat controllers" with SQL inside; services that import `req`; abstractions for a 3-route app (over-engineering). Folder-per-feature (above) scales better than folder-per-layer for most teams.

**Interview questions:** Why separate the service from the controller? Where do transactions belong? What is dependency injection and how do you do it in plain JS (pass dependencies as arguments)?

### Input validation and schemas

**[Must learn now]** Never trust anything from the client: body, query, params, headers, uploaded files. Validate shape, types, ranges and formats at the edge, and reject early with `400` or `422`. [Zod](https://zod.dev) is the popular choice (works with TypeScript and plain JS). Validate, then pass only the parsed result onward ("parse, don't validate").

```js
import { z } from "zod";
export const createOrderBody = z.object({
  customerId: z.number().int().positive(),
  items: z.array(z.object({
    productId: z.number().int().positive(),
    quantity: z.number().int().min(1).max(100),
  })).min(1),
});
// middleware: const parsed = schema.safeParse(req.body); if (!parsed.success) -> 422 with issues
```

Also validate business rules in the service (product exists, enough stock). Schema validation checks shape; it cannot know your data.

**Common mistake:** validating only the body and forgetting `req.query` and `req.params`; returning raw validation library errors that leak internals; allowing unexpected extra fields (mass assignment, for example a client sending `role: "admin"`).

**Interview questions:** Validation vs sanitization? What is mass assignment? 400 vs 422?

### Centralized error handling, async errors and cleanup

**[Must learn now]** Create one error type (for example `AppError(status, code, message)`) and one error middleware with four arguments `(err, req, res, next)`, registered last. Everything else throws. In Express 5 you do not need to wrap async handlers. The error middleware decides: known `AppError` goes to the client with its status; unknown error becomes `500` with a generic message, while full details go to the log only. See [error handling](https://expressjs.com/en/guide/error-handling.html).

```js
app.use((err, req, res, next) => {
  const known = err instanceof AppError;
  if (!known) req.log.error({ err }, "unhandled error");
  res.status(known ? err.status : 500).json({
    error: { code: known ? err.code : "INTERNAL", message: known ? err.message : "Something went wrong", requestId: req.id },
  });
});
```

Resource cleanup: close DB clients you check out (`client.release()` in `finally`), delete temp upload files on failure, and handle `unhandledRejection`/`uncaughtException` by logging then exiting (a process in unknown state should restart, supervised by Docker or a process manager). On `SIGTERM`, stop accepting connections, finish in-flight requests, close the DB pool, then exit (graceful shutdown).

**Common mistake:** sending stack traces to clients; swallowing errors with empty `catch`; leaking pool connections so the app freezes under load.

**Interview questions:** How do you handle errors in async Express handlers in v4 vs v5? What is graceful shutdown? What should the process do on an uncaught exception?

### Authentication vs authorization, and password hashing

**[Must learn now]** **Authentication (AuthN)** answers "who are you?". **Authorization (AuthZ)** answers "what may you do?". Mixing them is the root of many bugs. Analogy: a hotel key card. AuthN is getting the card at reception; AuthZ is which doors the card opens.

Passwords: never store them, store a slow salted hash. Use **argon2id** (for example the [`argon2`](https://github.com/ranisalt/node-argon2) package) or bcrypt, following the [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) for current parameters (read it; parameter advice changes). A "salt" is random data added per password so equal passwords hash differently; the libraries do this for you. Use the same error for "no such user" and "wrong password" to avoid revealing which emails exist.

**Common mistake:** MD5/SHA-1/SHA-256 for passwords; logging request bodies that contain passwords; no limit on login attempts.

**Interview questions:** Why hash instead of encrypt? What does a salt do? What does "slow hash" mean and why is it good?

### Sessions, cookies, JWT, refresh tokens and expiry

**[Must learn now]** Two main designs:

| Design | How it works | Good | Watch out |
|---|---|---|---|
| Server session | Server stores session data, browser holds only a random session id in a cookie | Easy to revoke (delete the row); simple | Needs a session store (Postgres or Redis) |
| JWT access token | Signed token carrying claims (user id, role, expiry); server verifies signature, no lookup | Stateless; works across services | Cannot be revoked before expiry unless you add a blocklist; claims go stale |

A good default for a first-party web app: short-lived access JWT (about 10 to 15 minutes) plus a long-lived **refresh token** stored in an `httpOnly`, `Secure`, `SameSite` cookie. The refresh token is random (not a JWT), stored **hashed** in the database, and **rotated** on every use: each refresh returns a new refresh token and invalidates the old one. If an old one is reused, assume theft and revoke the whole token family. Analogy: the access token is a day pass; the refresh token is your membership card kept at the front desk.

Rules: sign with a strong secret from env (or asymmetric keys), set `exp`, pin the allowed algorithm when verifying, never put secrets or personal data in the payload (it is only base64-encoded, not encrypted), and keep role checks reading the current role from the DB for sensitive actions if roles can change. Read the [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).

> **Honest note:** "JWT everywhere" is fashionable, not always right. For a single web app with its own backend, server sessions are simpler and safer. JWT earns its place with mobile clients, multiple services, or third-party API consumers. You will build the access+refresh pattern in Project 2 because you will meet it in jobs.

**Common mistake:** storing tokens in `localStorage` (readable by any XSS); non-expiring JWTs; accepting `alg: none` or not pinning the algorithm; storing refresh tokens in plaintext.

**Interview questions:** Cookies vs localStorage for tokens? How do you log a user out with JWT? What is refresh token rotation? What is CSRF and when does it apply (cookie-based auth)?

### RBAC and permissions

**[Must learn now]** Role-based access control: users have roles; roles allow actions. Two levels matter:

1. **Role check** (function level): only `admin` may delete a product.
2. **Ownership check** (object level): a `customer` may read only their own orders. This is the most commonly missed one; it is called BOLA/IDOR (broken object level authorization) and is number one on the OWASP API list.

```js
const requireRole = (...roles) => (req, res, next) =>
  roles.includes(req.user.role) ? next() : next(new AppError(403, "FORBIDDEN", "Not allowed"));
// ownership: in the service, order.customerId must equal req.user.customerId unless role is staff/admin
```

Default deny: a route without an explicit permission should be blocked in code review. Return `404` instead of `403` for objects the user should not even know exist.

**Common mistake:** checking the role in the frontend only; trusting `userId` sent in the body instead of the token.

**Interview questions:** RBAC vs ABAC? What is IDOR and how do you prevent it? Where does the permission check live (middleware vs service)?

### REST design and status codes

**[Must learn now]** Nouns for resources, HTTP verbs for actions, plural paths: `GET /orders`, `POST /orders`, `GET /orders/:id`, `PATCH /orders/:id`, `DELETE /orders/:id`. Actions that are not CRUD get a sub-resource: `POST /orders/:id/cancel`.

| Code | Use for |
|---|---|
| 200 / 201 / 204 | OK / created (add `Location`) / OK no body |
| 400 / 422 | Malformed request / valid shape but fails validation |
| 401 | Not authenticated (missing/invalid/expired token) |
| 403 | Authenticated but not allowed |
| 404 / 409 | Not found / conflict (duplicate email, state conflict) |
| 429 | Too many requests |
| 500 / 503 | Our bug / dependency down |

Idempotent methods (GET, PUT, DELETE) give the same result when repeated; POST does not, so for payments and orders support an `Idempotency-Key` header. Version the API (`/v1/`) before you have external users. Use one consistent error shape. See the [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html).

**Common mistake:** returning `200` with `{ success: false }`; using `GET` to change data; verbs in URLs like `/getOrders`.

**Interview questions:** PUT vs PATCH? What is idempotency and why does it matter for POST /orders? 401 vs 403?

### Pagination, filtering, sorting and search

**[Must learn now]** Never return an unbounded list. Two styles:

- **Offset/limit** (`?page=2&limit=20`): simple, supports "jump to page 7", but slow on deep pages and can skip or repeat rows when data changes. See [LIMIT and OFFSET](https://www.postgresql.org/docs/current/queries-limit.html).
- **Cursor/keyset** (`?after=<last id or created_at+id>`): fast at any depth and stable; no "jump to page". Use for feeds and large tables.

Filtering and sorting come from query params, but **whitelist** sortable and filterable fields (never put `req.query.sort` directly into SQL). Search: `ILIKE` for small data, PostgreSQL full-text search or a trigram index later. Return metadata: `{ data, page, limit, total }` or `{ data, nextCursor }`. Cap `limit` (for example max 100).

**Common mistake:** `ORDER BY` a column with no unique tie-breaker (rows jump between pages); SQL injection through sort field; counting total rows on a huge table on every request.

**Interview questions:** Offset vs keyset pagination trade-offs? How do you make sorting deterministic?

### File uploads and validation

**[Learn during projects]** Use [multer](https://github.com/expressjs/multer) for `multipart/form-data`. Always set a size limit, an allowed-types list, and check the real content (magic bytes), not just the filename or `Content-Type` header, both of which the client controls. Store files outside the web root with random names, never the user's filename. In production, put files in object storage (S3 compatible) and keep only the key in the database. Delete partial files on error. For Project 2, an optional product image upload is enough.

**Common mistake:** trusting the file extension; unlimited size (memory exhaustion); serving uploads from the same origin as your app without safe headers.

**Interview questions:** How do you stop a user uploading a 5 GB file? Why not trust `Content-Type`?

### Logging and environment configuration

**[Must learn now]** Use structured (JSON) logs with a logger like [pino](https://getpino.io): level, time, request id, user id, route, duration. Never log passwords, tokens, full card data or full request bodies. Config comes from environment variables ([12-factor config](https://12factor.net/config)): read and validate them once at startup in a `config.js` (use Zod) and crash early if something is missing. Commit `.env.example`, never `.env`.

**Common mistake:** `console.log` everywhere with no request id; reading `process.env.X` all over the code; a default fallback secret like `"secret"` that silently ships to production.

**Interview questions:** What are log levels for? Why JSON logs? How do you trace one request through many log lines?

### CORS and security headers

**[Must learn now]** CORS is a browser rule: a page on origin A may read responses from origin B only if B says so with `Access-Control-Allow-*` headers. It does not protect your API from curl or other servers; it protects users' browsers. Use the [cors](https://github.com/expressjs/cors) package with an explicit allow-list of origins (not `*` when you use cookies; with credentials `*` is not allowed at all). Use [Helmet](https://helmetjs.github.io) to set safe default headers (for example `X-Content-Type-Options`, `Strict-Transport-Security`). Turn off `x-powered-by`. Read the official [Express security best practices](https://expressjs.com/en/advanced/best-practice-security.html) and Node's [security best practices](https://nodejs.org/en/learn/getting-started/security-best-practices).

**Common mistake:** `origin: true` or `*` in production; thinking CORS blocks attackers.

**Interview questions:** What is a preflight request? Why can't you use `*` with credentials? Does CORS stop CSRF?

### Rate limiting and brute-force protection

**[Must learn now]** Limit how fast one client can call you. Use [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit): a general limit (for example 100 per minute per IP) and a much stricter one on `/auth/login` and `/auth/refresh`. Behind a proxy you must configure `trust proxy` correctly or every user shares the proxy's IP. For several app instances use a shared store (Redis) so counters are global. Add account-level protection: after N failed logins, add delay or temporary lock (careful: locks can be abused to lock out others, so prefer progressive delay plus alerting).

**Common mistake:** rate limiting by IP behind a load balancer without `trust proxy`; in-memory counters with multiple instances.

**Interview questions:** Fixed window vs sliding window vs token bucket? How do you stop credential stuffing?

### API tests and mocking

**[Must learn now]** Test the API at the HTTP edge with [supertest](https://github.com/ladjs/supertest) plus a test runner: [Vitest](https://vitest.dev) or the built-in [`node:test`](https://nodejs.org/api/test.html) runner. Three layers: unit tests for services (mock the repository), integration tests for routes against a real test PostgreSQL database (best value), and a few end-to-end flows (register, login, create order, cancel). Export `app` separately from `server.listen` so tests do not open ports. Each test starts from a known state (truncate tables or wrap in a rolled-back transaction). Mock only what you do not own (email, payment, clock); do not mock your own database for integration tests, or you test nothing real.

```js
const res = await request(app).post("/v1/orders").set("Authorization", `Bearer ${token}`).send(body);
expect(res.status).toBe(201);
```

**Common mistake:** tests that depend on each other's order; asserting only status codes; mocking so much that the test passes on broken code.

**Interview questions:** Unit vs integration test? What should you mock? How do you test auth-protected routes?

### WebSockets and Server-Sent Events (basics)

**[Learn later if needed]** Normal HTTP: client asks, server answers. **SSE** (server-sent events, see [MDN](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)) is a one-way stream from server to browser over plain HTTP; great for notifications, progress bars, and LLM token streaming (you will use this in Phase 11). **WebSockets** (library [ws](https://github.com/websockets/ws), or Socket.IO) are two-way; use for chat, live collaboration. Choose SSE first if data flows only server to client. Remember: authenticate the connection, limit connections per user, and clean up listeners on disconnect.

**Common mistake:** using WebSockets when polling or SSE is enough; never closing connections (memory leak).

**Interview questions:** SSE vs WebSocket vs long polling? How do you scale WebSockets to several servers (a pub/sub layer such as Redis)?

### Background tasks and queues (concepts)

**[Learn later if needed]** Do not make a user wait for slow work (sending email, generating PDFs, calling an AI model). Put a job in a **queue** and let a **worker** process it. Analogy: you drop an order slip at the kitchen window and get a buzzer. Libraries like [BullMQ](https://docs.bullmq.io) (needs Redis) do this in Node. Key ideas: at-least-once delivery means jobs may run twice, so make them **idempotent**; retries with backoff; a dead-letter queue for jobs that keep failing; the API returns `202 Accepted` plus a status URL. For Project 2 you only need to know the idea; a simple "send confirmation email after commit" can be a plain async call with logging.

**Common mistake:** doing background work inside the request after responding without error handling (silent failures); jobs that are not idempotent.

**Interview questions:** Why use a queue? What does "at-least-once" mean? What is a dead-letter queue?

### When a separate backend beats Next.js Route Handlers

**[Must learn now]** Next.js [Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers) and Server Actions are fine for a backend that exists only to serve one Next.js app: form posts, small CRUD, auth callbacks. Choose a **separate backend** (Express, FastAPI, NestJS) when:

- More than one client needs the API (web, mobile app, partner integrations, internal tools).
- You need long-running work, queues, cron jobs, WebSockets, or heavy CPU. Serverless/edge hosting of Next.js has time limits and no persistent connections.
- The team is split: backend engineers deploy and scale independently of the frontend.
- The domain is large (orders, payments, inventory) and you want clear module boundaries, strict layering and a versioned public API contract.
- You want Python for the AI side (Phase 9 onwards) and share one API between a Next.js frontend and AI workers.
- Database connection management matters: serverless functions can open too many connections.

Stay with Route Handlers when it is a small product, one team, one client, and speed of shipping matters most. A middle path: Next.js frontend calls a separate API through a thin server-side layer (BFF, backend-for-frontend).

**Interview questions:** When would you not use Next.js API routes? What is a BFF? What problems do serverless functions have with databases?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
|---|---|---|---|---|---|---|
| Node runtime | Event loop, async, streams | [Node intro](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs), [Event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) | [How Node.js Works (IT-Learners, Hindi/Urdu)](https://www.youtube.com/watch?v=3r4Ja7i763c) | Beginner | 2 h | Write a tiny `node:http` server, then explain the event loop aloud |
| Express basics | Routing, middleware, Router | [Routing](https://expressjs.com/en/guide/routing.html), [Middleware](https://expressjs.com/en/guide/using-middleware.html) | [Express Crash Course (Traversy Media, English)](https://www.youtube.com/watch?v=CnH3kAXSrmU) | Beginner | 2 h | Build a 5-route API with a logger middleware |
| Express 5 | Migration, async errors | [Migration guide](https://expressjs.com/en/guide/migrating-5.html), [5.1 announcement](https://expressjs.com/en/blog/2025-03-31-v5-1-latest-release) | No video verified for this topic; use the official documentation above. | Intermediate | 1 h | Convert one Express 4 snippet to v5 |
| Validation | Zod schemas, 400 vs 422 | [Zod](https://zod.dev) | No video verified for this topic; use the official documentation above. | Beginner | 1.5 h | Validate body, query and params for one route |
| Error handling | Central handler, cleanup | [Error handling](https://expressjs.com/en/guide/error-handling.html) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | One AppError class and one handler |
| Auth and hashing | Argon2, bcrypt, salts | [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [node-argon2](https://github.com/ranisalt/node-argon2) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Register and login with hashed passwords |
| JWT and sessions | Access, refresh, rotation | [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | [JWT Authentication Tutorial - Node.js (Web Dev Simplified, English)](https://www.youtube.com/watch?v=mbsmsi7l3r4); [Node Auth Tutorial (JWT) #10 - JSON Web Tokens (theory) (Net Ninja, English)](https://www.youtube.com/watch?v=LZq0G8WUaII) | Intermediate | 2.5 h | Add refresh rotation with hashed tokens in the DB |
| RBAC and REST | Roles, ownership, status codes | [OWASP REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Write the role x endpoint matrix for Project 2 |
| Security | CORS, Helmet, rate limit | [Express security](https://expressjs.com/en/advanced/best-practice-security.html), [Helmet](https://helmetjs.github.io), [express-rate-limit](https://github.com/express-rate-limit/express-rate-limit), [cors](https://github.com/expressjs/cors) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Limit login to 5 tries per minute and prove it with a test |
| Uploads, logs, config | multer, pino, 12-factor | [multer](https://github.com/expressjs/multer), [pino](https://getpino.io), [12-factor config](https://12factor.net/config) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Validated config module that crashes when a variable is missing |
| API testing | supertest, Vitest, node:test | [supertest](https://github.com/ladjs/supertest), [Vitest](https://vitest.dev), [node:test](https://nodejs.org/api/test.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Test register, login, protected route |
| Realtime and queues | SSE, ws, BullMQ | [MDN SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events), [ws](https://github.com/websockets/ws), [BullMQ](https://docs.bullmq.io) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | SSE endpoint that streams a counter for 10 seconds |
| Backend vs Route Handlers | Trade-offs | [Next.js Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers) | No video verified for this topic; use the official documentation above. | Beginner | 0.5 h | Write a half-page decision note for Project 2 |

## Verification notes

- **Network limitation (be aware):** from my machine `www.youtube.com` was unreachable (connection reset), so I could not run the `youtube.com/oembed` and `lengthSeconds` checks exactly as specified. Instead I verified every video through `noembed.com`, a third-party service that relays YouTube's oEmbed data. This confirmed the real **title and channel** of each video ID, which was found through web search (never guessed).
- Express Crash Course, channel Traversy Media: title and channel confirmed (video ID CnH3kAXSrmU). Duration NOT verified. Published date NOT verified; I could not confirm whether it uses Express 5, so treat any v4-only syntax as old and check against the table above. Language: English (from channel).
- JWT Authentication Tutorial - Node.js, channel Web Dev Simplified (ID mbsmsi7l3r4): title and channel confirmed. A search snippet showed an upload date of 2019-09-21, so it is Express 4 era. Duration NOT verified. Use for the concept only; follow the OWASP sheets for current practice (refresh rotation, httpOnly cookies).
- Node Auth Tutorial (JWT) #10 - JSON Web Tokens (theory), Net Ninja (ID LZq0G8WUaII): title and channel confirmed. Duration NOT verified. It belongs to a series that uses MongoDB; only the theory episode is recommended.
- How Node.js Works | Node.js Architecture, Event Loop | Node.js Tutorial for Beginners in Hindi/Urdu, channel IT-Learners (ID 3r4Ja7i763c): title and channel confirmed; language "Hindi/Urdu" comes from the title. Duration NOT verified, and I did not watch it, so I cannot vouch for its accuracy; cross-check with the official event loop guide.
- I did not watch any video in full. "Verified" means the link resolves to the stated title and channel.
- Official documentation pages were fetched and their page titles read. The Express migration guide, the Express 5.1 announcement and the PostgreSQL isolation page were read for content. Versions quoted (express 5.3.0, Node 24 LTS) come from the npm registry and the nodejs.org release index on 2026-10-09.
- The socket.io docs site and one OWASP JWT cheat sheet URL did not resolve for me, so they are not linked.

## Hands-on exercises

1. Write a bare `node:http` server with three routes. Then rewrite it with Express and list what Express did for you.
2. Create three middlewares: request id, timing logger, and a fake auth that sets `req.user`. Show the order in which they run using logs.
3. Make an endpoint that blocks the event loop with a loop, call it, and show that `/health` hangs. Then fix it with a worker thread or by removing the work.
4. Build register and login with argon2 hashing. Prove with a test that the database never contains the plaintext.
5. Implement access token + rotating refresh token. Write a test where reusing an old refresh token revokes the family.
6. Add Zod validation to one route for body, query and params, and a test that an extra field `role: "admin"` is rejected or ignored.
7. Write the role x endpoint matrix (table) for Project 2, then implement one ownership check and test that user A gets 404 for user B's order.
8. Add a rate limiter on login and a supertest that sends 6 requests and expects `429` on the last.
9. Implement graceful shutdown on `SIGTERM` and demonstrate it by sending the signal during a slow request.
10. Write a half-page note: "For this project, would I use Route Handlers or a separate backend, and why?"

## Checkpoint

**Explain (aloud, no notes):**
- What happens, step by step, from a request arriving at Express to the response leaving, including middleware and the error handler?
- Why does `await db.query()` not block other requests, but a 2-second `for` loop does?
- How is refresh token rotation different from a long-lived JWT, and what attack does reuse detection catch?
- Three situations where you would pick a separate backend over Route Handlers.

**Modify code:**
- Change an offset-paginated endpoint to keyset pagination.
- Add a new role `staff` that can read all orders but not delete products.

**Debug:**
- A route hangs forever: find that it calls neither `next()` nor `res.send()`.
- A user can read another user's order by changing the id in the URL: find the missing ownership check.
- `Cannot set headers after they are sent`: find the double response.

**Write tests:**
- Test 401 for a missing token, 401 for an expired token, 403 for a wrong role, 404 for another user's order, 422 for invalid body.

**Ready to move on when:** you can build register, login, refresh and a role-protected CRUD resource with validation, central errors and tests from an empty folder, without copying code, and explain every middleware you used.

## Week plan

### Week 7 — Node and Express in depth, and Project 2 kick-off  (estimated hours: 10)

**Learning objectives**
- Explain the Node event loop and why blocking is harmful.
- Build a layered Express 5 API (routes, controllers, services, repositories).
- Implement validation, central errors, password hashing, access and refresh tokens, and role checks.
- Start Project 2: repo, config, database connection, migrations, auth module.

**Topics and subtopics**
- **[Must learn now]** Node runtime and event loop (1 h)
- **[Must learn now]** Express 5 routing, middleware, errors, differences from Express 4 (1.5 h)
- **[Must learn now]** Layering, Zod validation, central error handler (1.5 h)
- **[Must learn now]** Password hashing, JWT access plus refresh rotation, RBAC (2.5 h)
- **[Must learn now]** SQL mini-primer: create tables and run CRUD in `psql` (see Phase 7 schema) (1 h)
- **[Learn during projects]** Logging with pino, config validation, CORS, Helmet, rate limit (1 h)
- **[Learn later if needed]** SSE, WebSockets, queues: read the concept sections only (30 min)
- Project 2 Milestones M0 to M2 (below)

**Small prerequisite concepts**
- Environment variables and `.env` loading (`node --env-file=.env` or `dotenv`).
- HTTP methods, status codes, headers (Phase 3).
- Promises and `async/await` (Phase 1).
- How to run PostgreSQL locally (Docker one-liner or a native install) and connect with `psql`.

**Reading**
- [Node intro](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs), [Event loop](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [Express migration guide](https://expressjs.com/en/guide/migrating-5.html), [Error handling](https://expressjs.com/en/guide/error-handling.html), [Security best practices](https://expressjs.com/en/advanced/best-practice-security.html)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [OWASP Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)

**Video**
- Express Crash Course, Traversy Media, English, duration not verified: [link](https://www.youtube.com/watch?v=CnH3kAXSrmU)
- JWT Authentication Tutorial - Node.js, Web Dev Simplified, English, duration not verified (2019, Express 4 era): [link](https://www.youtube.com/watch?v=mbsmsi7l3r4)
- Hindi option: How Node.js Works (IT-Learners, Hindi/Urdu per title), duration not verified: [link](https://www.youtube.com/watch?v=3r4Ja7i763c)

**Hands-on exercises**
1. Do Phase 6 exercises 1, 2, 3 and 4.
2. Do Phase 6 exercises 5 and 6.
3. Do Phase 6 exercise 7 on paper.
4. Execute Project 2 milestones M0, M1, M2.

**What you must build**
A running Express 5 API in a new Git repo with: validated config, pino logging with request ids, central error handler, PostgreSQL connection pool, first migration (users, refresh_tokens), and working `register`, `login`, `refresh`, `logout`, `me` endpoints with tests.

**Completion checklist**
- [ ] Server starts only if all required env vars are valid.
- [ ] Passwords stored as argon2 or bcrypt hashes.
- [ ] Refresh tokens stored hashed and rotated; reuse is rejected.
- [ ] Every error returns the same JSON shape with a request id.
- [ ] At least 8 passing integration tests for auth.
- [ ] `.env` ignored by Git and `.env.example` committed.
- [ ] Decision note on Route Handlers vs separate backend written.

**Self-test**
1. Why does Express 5 not need `express-async-errors`?
2. Where should a database transaction start and end: controller, service or repository? Why?
3. What is stored in your refresh token table and why hashed?
4. How is a 401 different from a 403 in your API?
5. What does `trust proxy` do for rate limiting?

**Common mistakes**
- Following an Express 4 tutorial and using `/*` wildcards or extra packages.
- Writing SQL in controllers.
- Skipping tests "until the end".
- Putting the JWT secret in code.
- Over-building: do not add queues or WebSockets to Project 2.

**Ready to continue when:** the auth module works end to end, tests pass from a clean database, and you can explain refresh token rotation without notes.

**Slower-track option:** Do Node/Express and layering this week, and move hashing plus JWT refresh into Week 8 (use a simple access-token-only login first). Skip logging polish and rate limiting until Week 8. Do not skip validation and central errors.

# Project 2 — Business Order Management API (Node.js + Express)

This project spans Week 7 (start) and Week 8 (finish). It is the backend twin of what you will rebuild in FastAPI in Project 4, so keep it clean and well documented. Do not copy full code from tutorials; build one milestone at a time.

## Problem statement and real-world use case

A small wholesale business (think a Surat textile trader or a local electronics distributor) takes orders from customers by phone and WhatsApp, tracks them in Excel, and loses track of stock, who changed what, and which orders are unpaid. You build the API that a future admin dashboard (your Project 1) and a customer app could use: manage products, customers and orders; keep stock correct; enforce who can do what; keep an audit trail.

## Requirements and user stories

- As an **admin**, I can create staff users and change roles, so I control access.
- As **staff**, I can create and edit customers and products, and create orders for a customer, so the business runs day to day.
- As **staff**, I can move an order through statuses (`pending` to `confirmed` to `shipped` to `delivered`, or `cancelled`), and I see the history.
- As a **customer**, I can log in and see only my own orders, and cancel a `pending` one.
- As any user, I can list orders with filters, sorting, search and pagination so I can find things fast.
- As the **business**, I need stock to never go negative, even when two orders arrive at the same moment.
- As a **developer**, I need clear errors, logs with request ids, tests, and API docs.

## MVP versus advanced features

| Level | Features |
|---|---|
| MVP | Auth (register, login, refresh, logout), roles (admin, staff, customer), products CRUD, customers CRUD, create order with items in one transaction, stock decrement, order list with filters and pagination, status changes, validation, central errors, tests, README |
| Advanced | Order status history table, idempotency key on create order, keyset pagination, soft delete, product image upload, CSV export, audit log, OpenAPI spec, Docker Compose, CI, rate limiting per user |
| Postpone | Payments gateway, queues, emails, multi-warehouse stock, real-time updates |

## Suggested architecture

A single modular monolith: Express 5 app, PostgreSQL (raw SQL with `pg` and a small migration tool such as [node-pg-migrate](https://github.com/salsita/node-pg-migrate), or an ORM such as Prisma or Drizzle if you want to compare, see Phase 7). Use raw SQL for the first pass: it teaches the fundamentals the roadmap is trying to build and mirrors what SQLAlchemy does later.

```text
Client -> Express app
          |- middleware: request-id, logger, helmet, cors, rate-limit, json
          |- routes -> controllers -> services -> repositories -> pg Pool -> PostgreSQL
          '- error middleware (last)
```

> **Honest note:** You know MongoDB, so the temptation is to use it here. Resist for this project: orders, stock and money are relational and need transactions. In Phase 7 you will build a small Mongo comparison so you learn when each fits.

## Folder structure

```text
order-api/
  package.json
  .env.example
  README.md
  migrations/            # numbered SQL migrations
  src/
    app.js               # builds Express app (exported for tests)
    server.js            # listen + graceful shutdown
    config/              # env parsing with Zod
    db/                  # pool, transaction helper
    middleware/          # auth, requireRole, validate, errorHandler, rateLimit
    lib/                 # AppError, logger, pagination helpers
    modules/
      auth/ users/ customers/ products/ orders/
        *.routes.js *.controller.js *.service.js *.repository.js *.schemas.js
  tests/                 # integration tests, helpers, seed
```

Why each folder exists: `app.js` vs `server.js` lets tests import the app without opening a port; `db/` is the only place that knows about `pg`; `modules/` keeps one feature's files together; `lib/` holds tiny shared pieces.

## Database schema and ERD (text form)

```text
users (id PK, email UNIQUE, password_hash, role CHECK in admin/staff/customer,
       customer_id FK -> customers.id NULL, is_active, created_at)
refresh_tokens (id PK, user_id FK, token_hash UNIQUE, family_id, expires_at,
                revoked_at NULL, replaced_by NULL, created_at)
customers (id PK, name, email UNIQUE, phone, city, created_at)
products (id PK, sku UNIQUE, name, price_cents CHECK >= 0,
          stock INT CHECK >= 0, is_active, created_at)
orders (id PK, customer_id FK, status CHECK in pending/confirmed/shipped/
        delivered/cancelled, total_cents, idempotency_key UNIQUE NULL,
        created_by FK -> users.id, created_at, updated_at)
order_items (order_id FK, product_id FK, quantity CHECK > 0,
             unit_price_cents, PRIMARY KEY (order_id, product_id))
order_status_history (id PK, order_id FK, from_status, to_status,
                      changed_by FK -> users.id, changed_at)

Relationships:
customers 1 --- N orders       orders 1 --- N order_items
products  1 --- N order_items  (orders M --- N products via order_items)
customers 1 --- 0..N users     orders 1 --- N order_status_history
users     1 --- N refresh_tokens
```

Design notes to be able to defend: money is stored as integer cents (never floats); `unit_price_cents` is copied into the item so later price changes do not rewrite history; `CHECK (stock >= 0)` is the last line of defence against overselling; indexes on `orders(customer_id, created_at DESC)`, `orders(status, created_at)`, and `order_items(product_id)`. Foreign keys use `ON DELETE RESTRICT` for business data.

## API endpoints

All under `/v1`. "Own" means ownership is checked.

| Method and path | Purpose | Access | Success |
|---|---|---|---|
| POST /auth/register | Create customer user | Public (rate limited) | 201 |
| POST /auth/login | Get access token and refresh cookie | Public (strict limit) | 200 |
| POST /auth/refresh | Rotate refresh token | Cookie | 200 |
| POST /auth/logout | Revoke token family | Authenticated | 204 |
| GET /me | Current user | Authenticated | 200 |
| PATCH /users/:id/role | Change role | Admin | 200 |
| GET /products | List, search, paginate | Authenticated | 200 |
| POST /products | Create | Staff, admin | 201 |
| PATCH /products/:id | Update price, stock | Staff, admin | 200 |
| DELETE /products/:id | Deactivate | Admin | 204 |
| GET /customers | List, search | Staff, admin | 200 |
| POST /customers | Create | Staff, admin | 201 |
| GET /customers/:id | Detail | Staff, admin; customer own | 200 |
| POST /orders | Create with items (transaction) | Staff, admin; customer own | 201 |
| GET /orders | List with filters: status, customerId, from, to, q, sort, page, limit | Staff, admin all; customer own only | 200 |
| GET /orders/:id | Detail with items | Staff, admin; customer own | 200 |
| PATCH /orders/:id/status | Move status | Staff, admin | 200 |
| POST /orders/:id/cancel | Cancel and restock | Staff, admin; customer own, pending only | 200 |
| GET /health | Liveness plus DB check | Public | 200 |

Error shape for every failure: `{ "error": { "code", "message", "details?", "requestId" } }`.

## Packages and setup

- Runtime: `express` (v5), `pg`, `zod`, `argon2` (or `bcrypt`), `jsonwebtoken` (or `jose`), `pino` and `pino-http`, `helmet`, `cors`, `express-rate-limit`, `cookie-parser`.
- Dev: `vitest` (or `node:test`), `supertest`, `node-pg-migrate`, `eslint`, `prettier`.
- Setup order: `git init`, `.gitignore` (with `.env`), `npm init`, set `"type": "module"`, add scripts (`dev`, `start`, `test`, `migrate`), `.env.example`, a PostgreSQL instance for dev and a separate database for tests.

## Implementation milestones

1. **M0 (Week 7, 1 h): Skeleton.** Repo, config with Zod, `/health`, logger, central error handler, first test.
2. **M1 (Week 7, 2 h): Database.** Pool, migrations for users and refresh_tokens, `db` transaction helper, test database setup and cleanup.
3. **M2 (Week 7, 3 h): Auth.** Register, login, refresh rotation, logout, `me`, auth middleware, tests including reuse detection.
4. **M3 (Week 8, 2 h): Authorization.** `requireRole`, role-change endpoint, role x endpoint matrix as a test table.
5. **M4 (Week 8, 2.5 h): Products and customers.** Migrations, CRUD, validation schemas, pagination and search.
6. **M5 (Week 8, 3 h): Orders.** Create order in one transaction (lock product rows, check stock, insert items, decrement stock, compute total, write history). Status machine, cancel with restock. Ownership checks.
7. **M6 (Week 8, 1.5 h): Listing.** Filters, whitelisted sorting, pagination (offset first, keyset as stretch), indexes verified with `EXPLAIN` (Phase 7 skills).
8. **M7 (Week 8, 1.5 h): Hardening and docs.** Helmet, CORS allow-list, rate limits, graceful shutdown, README, coverage of the security checklist.

Teaching hint for M5: write the failure test first ("two concurrent orders for the last item: exactly one succeeds"). Then use `SELECT ... FOR UPDATE` (or a conditional `UPDATE products SET stock = stock - $1 WHERE id = $2 AND stock >= $1` and check the row count). Learn why in Week 9.

## Test cases

- Auth: register duplicate email gives 409; weak password gives 422; wrong password and unknown email give the same 401; expired access token gives 401; refresh rotates and old token reuse gives 401 and revokes the family; logout revokes.
- Authorization: customer cannot call staff endpoints (403); customer gets 404 for another customer's order; staff can list all; only admin changes roles.
- Validation: missing fields, wrong types, negative quantity, empty items array, unknown extra field (`role`) ignored or rejected, huge `limit` capped.
- Orders: total equals sum of items at current prices; stock decremented; insufficient stock gives 409 and nothing is written (transaction rolled back); cancelling restocks once only; illegal status jump (`delivered` to `pending`) gives 409; concurrent creation never oversells; same idempotency key returns the same order.
- Lists: pagination metadata correct, sort whitelist enforced (unknown sort field gives 400), filters combine.
- Platform: `/health` reflects DB down; rate limit returns 429; error responses never contain stack traces.

## Security checklist (prioritized)

1. Passwords hashed with argon2id or bcrypt; no plaintext anywhere, including logs.
2. Parameterized queries only (`$1, $2`); no string-built SQL; sort/filter columns from a whitelist.
3. Every route has an explicit auth and role requirement; default deny.
4. Object-level ownership checks on customer data (BOLA/IDOR) with tests.
5. Short-lived access token; refresh token hashed in DB, rotated, httpOnly Secure SameSite cookie; JWT algorithm pinned; secrets from env.
6. Input validation for body, query, params; max body size; unknown fields stripped; `limit` capped.
7. Rate limiting: strict on auth routes, general limit elsewhere; `trust proxy` set correctly.
8. Helmet, explicit CORS allow-list, `x-powered-by` off, HTTPS only in production.
9. Generic error messages to clients; details only in logs; no secrets or tokens in logs.
10. `npm audit` clean or understood; lockfile committed; minimal dependencies.
11. DB user for the app has only needed privileges (no superuser); separate test database.
12. Backups configured and a restore tested once (Week 9).

## Deployment plan

Keep it simple; full cloud work comes in Phase 15.

1. Add a `start` script, a `/health` endpoint, and read `PORT` from env.
2. Create a managed PostgreSQL instance on a provider you choose (any managed Postgres works; compare free tiers yourself, pricing changes often and I did not verify any provider's current plan).
3. Run migrations as a separate step (`npm run migrate`), never automatically from many app instances at once.
4. Set env vars in the host's secret manager, not in Git.
5. Deploy the Node service (a PaaS or a container; a Dockerfile is a good stretch goal) and put HTTPS in front.
6. Smoke test: register, login, create product, create order, list orders.
7. Turn on logs and one uptime check on `/health`.

## README structure

1. Project title and one-paragraph purpose.
2. Features (MVP list) and tech stack.
3. Architecture diagram (text) and folder structure.
4. ERD (text) and the reasoning for key design choices.
5. Getting started: prerequisites, env vars table, commands (install, migrate, seed, dev, test).
6. API overview table plus a link to the OpenAPI file or Postman collection.
7. Auth and roles matrix.
8. Testing: how to run, what is covered.
9. Security notes (checklist).
10. Deployment steps.
11. Known limitations and next steps.

## Acceptance criteria

- [ ] All MVP endpoints work and match the table; statuses and error shape are consistent.
- [ ] A clean clone runs with: install, set `.env`, migrate, seed, dev, test, using only the README.
- [ ] At least 30 meaningful integration tests pass; concurrency and ownership tests included.
- [ ] No endpoint accessible without the intended role; verified by the matrix test.
- [ ] Two simultaneous orders for the last unit: exactly one succeeds.
- [ ] No plaintext passwords or tokens in DB or logs.
- [ ] You can explain the schema, a transaction, and the auth flow aloud in 10 minutes.
- [ ] Deployed (or deployable with a documented plan) and health check green.

## Common mistakes

- Using MongoDB or floats for money "because it is quicker".
- Checking stock with a `SELECT`, then updating in separate statements (race condition).
- Doing the transaction in the controller or forgetting `ROLLBACK` and `release()`.
- Trusting `customerId` from the request body for customer users.
- No `ORDER BY` tie-breaker, so pagination duplicates rows.
- Returning password hashes from user endpoints.
- Skipping tests for the 403/404/409 paths.
- Building features (queues, payments) before the core is tested.

## Interview questions

1. Walk me through creating an order. What happens if the server crashes in the middle?
2. How do you prevent overselling under concurrent requests? Compare `FOR UPDATE` with a conditional update.
3. Why store prices in cents and copy the price into `order_items`?
4. Explain your auth design. How do you revoke access? What if a refresh token is stolen?
5. How do you prevent one customer from reading another's orders?
6. Offset vs keyset pagination: which did you use and why?
7. What would you change to support 100x traffic? (Indexes, read replicas, caching, queue for side effects.)
8. How do you test code that touches the database?
9. What would you do differently if this were a Next.js-only project?

## Week plan

### Week 8 — Finish Project 2: authorization, orders, validation, tests  (estimated hours: 10)

**Learning objectives**
- Implement object-level authorization and role checks with tests.
- Write a correct multi-table transaction for order creation.
- Build list endpoints with filters, whitelisted sorting and pagination.
- Reach a test suite you trust and write a professional README.

**Topics and subtopics**
- **[Must learn now]** Authorization middleware and ownership checks (1.5 h)
- **[Must learn now]** Transactions in `pg` (BEGIN, COMMIT, ROLLBACK, release in `finally`) and row locking, first look (2 h)
- **[Must learn now]** Pagination, filtering, sorting, search (1.5 h)
- **[Must learn now]** Integration testing against a real test database (2 h)
- **[Learn during projects]** Rate limiting, Helmet, CORS allow-list, graceful shutdown (1 h)
- **[Learn during projects]** Optional file upload for a product image (45 min, skip if behind)
- **[Learn later if needed]** Idempotency keys, keyset pagination, OpenAPI file (stretch)

**Small prerequisite concepts**
- SQL joins and `GROUP BY` basics (read Phase 7 first sections if unfamiliar).
- What a database transaction is: all steps happen or none.
- Connection pool: connections are borrowed and must be returned.

**Reading**
- [node-postgres pooling](https://node-postgres.com/features/pooling), [PostgreSQL transactions tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html), [LIMIT and OFFSET](https://www.postgresql.org/docs/current/queries-limit.html)
- [OWASP REST Security](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html), [supertest](https://github.com/ladjs/supertest)

**Video**
- Optional refresher: Net Ninja JWT theory (English, duration not verified): [Node Auth Tutorial (JWT) #10](https://www.youtube.com/watch?v=LZq0G8WUaII)
- No video verified for transactions in `pg`; use the official documentation above.

**Hands-on exercises**
1. Implement milestones M3 to M7 in order, committing after each.
2. Write the failing concurrency test first, then make it pass.
3. Run the role x endpoint matrix as a table-driven test.
4. Add `EXPLAIN` output for your orders list query before and after adding an index (use notes from Phase 7; return to this in Week 9).
5. Write the README using the structure above and let a friend (or Claude, with the review prompt from the AI workflow chapter) try to run it from scratch.

**What you must build**
The complete Project 2 MVP: auth, roles, products, customers, orders with transactional stock handling, filtered and paginated list, tests, and README. Deployed or with a written deployment plan.

**Completion checklist**
- [ ] All MVP endpoints implemented.
- [ ] 30 or more integration tests pass from a fresh database.
- [ ] Concurrency test proves no overselling.
- [ ] Ownership test: customer A cannot see customer B's order.
- [ ] Security checklist items 1 to 9 ticked.
- [ ] README complete and tested from a clean clone.
- [ ] Retrospective note: three things you would change.

**Self-test**
1. Why do you release the client in a `finally` block?
2. What stops two concurrent orders from both taking the last item?
3. Why is `ORDER BY created_at` alone not safe for pagination?
4. Which layer should decide "a customer can cancel only pending orders", and why?
5. What does your API return when a customer asks for someone else's order, and why?

**Common mistakes**
- Leaking pool clients on error paths.
- Putting authorization only in the frontend or only at the route level.
- Tests that share state and pass only in a certain order.
- Leaving README for the end and skipping the clean-clone test.
- Adding payment, queue or WebSocket features instead of finishing tests.

**Ready to continue when:** a clean clone passes all tests, you can explain the order transaction and the auth flow without notes, and the concurrency and ownership tests exist and pass.

**Slower-track option:** Cut file upload, the status history table and keyset pagination. Keep auth, roles, orders-in-a-transaction, and at least 20 tests. Move README polish and deployment to the weekend after Week 9; Phase 7 gives you the knowledge to finish the concurrency part properly.

# Phase 7 — Databases and Data Modeling (PostgreSQL main, MongoDB second)

## Why this phase matters

Most of the bugs and slowdowns you will meet in real backends live in the database: missing constraints, wrong relationships, slow queries, race conditions on money or stock, and migrations that break production. You have used MongoDB, which is a good start, but the jobs you are aiming at (backend, full-stack, AI application engineer) mostly use PostgreSQL, and later phases (FastAPI, pgvector for RAG) build on it. So PostgreSQL is the main tool here and MongoDB is the comparison. This phase is fundamentals plus judgement. It is Week 9, and you will keep returning to it. Research date: 2026-10-09; the PostgreSQL docs fetched today are for version 18.

## Prerequisites and "skip test"

Skip a topic only if you can demonstrate it:

- Create a table with a primary key, a foreign key, a `NOT NULL`, a `UNIQUE` and a `CHECK` constraint, and explain what each protects.
- Write, without help, a query with `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY` and `LIMIT`.
- Explain `LEFT JOIN` vs `INNER JOIN` using a customer who has no orders.
- Run `EXPLAIN ANALYZE` and say whether the plan uses an index and why.
- Describe what happens to two transactions that update the same row at the same time.
- In Mongo, explain when you would embed vs reference with one example.

## Concepts explained

### SQL and PostgreSQL basics: tables, rows, columns, schemas, types

**[Must learn now]** A relational database stores data in **tables** (like a spreadsheet tab) made of **columns** (fields with a fixed type) and **rows** (records). A **schema** is a namespace inside a database (default `public`). Pick types carefully:

| Need | Use | Avoid |
|---|---|---|
| Ids | `bigint GENERATED ALWAYS AS IDENTITY` or `uuid` | `serial` in new code (older style) |
| Money | `integer`/`bigint` cents, or `numeric(12,2)` | `float`/`real` (rounding errors) |
| Text | `text` (with `CHECK` for limits if needed) | `char(n)` |
| Time | `timestamptz` | `timestamp` without zone |
| Flags | `boolean` | strings like "yes"/"no" |
| Flexible extras | `jsonb` (sparingly) | JSON for everything |
| Enum-like | `text` + `CHECK`, or a lookup table | Magic numbers |

```sql
CREATE TABLE customers (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email      text NOT NULL UNIQUE,
  name       text NOT NULL,
  city       text,
  created_at timestamptz NOT NULL DEFAULT now()
);
```

Use the `psql` terminal client or a GUI such as [pgAdmin](https://www.pgadmin.org). Learn `\dt`, `\d table`, `\x`, `\timing` in `psql`.

**Common mistake:** using `timestamp` without time zone, then getting wrong times across regions; floats for money.

**Interview questions:** Why `timestamptz`? Why not float for money? What is a schema in PostgreSQL?

### Primary keys, foreign keys, constraints

**[Must learn now]** A **primary key** (PK) uniquely identifies a row. A **foreign key** (FK) says "this column must match an existing row in another table", so you cannot create an order for a customer who does not exist. Constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY ... ON DELETE`) let the database defend data even when application code has a bug. Analogy: the application is the shop assistant, constraints are the safe lock; both should exist. See [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).

```sql
CREATE TABLE products (
  id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku         text NOT NULL UNIQUE,
  name        text NOT NULL,
  price_cents integer NOT NULL CHECK (price_cents >= 0),
  stock       integer NOT NULL DEFAULT 0 CHECK (stock >= 0)
);
```

`ON DELETE RESTRICT` (default behavior) blocks deleting a parent that has children; `CASCADE` deletes the children too (use with care); `SET NULL` clears the reference.

**Common mistake:** no FK "for speed" and then orphan rows; `CASCADE` on business data that should be kept.

**Interview questions:** Natural vs surrogate keys? What does `ON DELETE CASCADE` do and when is it dangerous?

### Normalization and relationships (1-1, 1-N, M-N)

**[Must learn now]** **Normalization** means storing each fact once. If a customer's city is repeated on every order, changing it means updating many rows and some will be missed. Rules of thumb (1NF to 3NF): one value per cell; every column depends on the key; no column depends on a non-key column. Denormalize only on purpose, for measured performance reasons.

- **One-to-one**: `users` and `user_profiles` (rare; often just one table).
- **One-to-many**: one customer has many orders; the FK sits on the "many" side (`orders.customer_id`).
- **Many-to-many**: orders and products. Use a **join table** (`order_items`) with two FKs, usually a composite PK, and extra columns that belong to the relationship (`quantity`, `unit_price_cents`).

**Common mistake:** storing comma-separated ids in one column; forgetting that the item price must be copied at order time.

**Interview questions:** Explain 3NF in plain words. How do you model M-N? When would you denormalize?

### CRUD, filtering, sorting, grouping, aggregates

**[Must learn now]** `INSERT`, `SELECT`, `UPDATE`, `DELETE`; always use `WHERE` on updates and deletes (run it as a `SELECT` first). `WHERE` filters rows before grouping; `HAVING` filters groups after. Aggregates: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `NULL` is "unknown", so `x = NULL` is never true; use `IS NULL`. See [Aggregate functions](https://www.postgresql.org/docs/current/tutorial-agg.html).

```sql
SELECT status, count(*) AS orders, sum(total_cents) / 100.0 AS revenue
FROM orders
WHERE created_at >= now() - interval '30 days'
GROUP BY status
HAVING count(*) > 5
ORDER BY revenue DESC;
```

**Common mistake:** `UPDATE` without `WHERE`; `COUNT(column)` vs `COUNT(*)` (the first ignores NULLs); selecting non-grouped columns.

**Interview questions:** `WHERE` vs `HAVING`? What does `COUNT(*)` vs `COUNT(col)` do? How does `NULL` behave in comparisons?

### Joins

**[Must learn now]** A join combines rows from tables by a condition. `INNER JOIN` keeps only matches. `LEFT JOIN` keeps all left rows, with NULLs where nothing matches (use it for "customers with no orders"). See [Joins Between Tables](https://www.postgresql.org/docs/current/tutorial-join.html). A trap: joining orders to order_items multiplies order rows, so `SUM(orders.total_cents)` after that join is wrong; aggregate in a subquery or CTE first.

**Common mistake:** a `WHERE` on the right table of a `LEFT JOIN` which silently turns it into an inner join (put the condition in `ON`); fan-out double counting.

**Interview questions:** Inner vs left vs full join with an example? What is a self join? Why can a join inflate a sum?

### Subqueries, CTEs, and window functions at the right level

**[Must learn now]** A subquery is a query inside a query. A **CTE** (`WITH name AS (...)`) names a step so complex queries read top-down; see [WITH Queries](https://www.postgresql.org/docs/current/queries-with.html). Learn `EXISTS` / `NOT EXISTS`, `IN`, and scalar subqueries. **[Learn during projects]** Window functions (`ROW_NUMBER()`, `SUM() OVER (PARTITION BY ...)`; see [Window functions tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)) for "top order per customer" and running totals. **[Learn later if needed]** recursive CTEs.

```sql
WITH customer_totals AS (
  SELECT customer_id, sum(total_cents) AS spent
  FROM orders WHERE status <> 'cancelled' GROUP BY customer_id
)
SELECT c.name, t.spent
FROM customer_totals t JOIN customers c ON c.id = t.customer_id
ORDER BY t.spent DESC LIMIT 10;
```

**Common mistake:** assuming a CTE is always a performance trick (in modern PostgreSQL they are usually inlined; use them for readability).

**Interview questions:** `IN` vs `EXISTS`? What is a CTE for? What does `ROW_NUMBER() OVER (PARTITION BY ...)` give you?

### SQL practice schema and queries you should write

**[Must learn now]** Create this schema in a scratch database, then write every query below yourself before looking at any solution (ask Claude for hints only; see the AI workflow chapter).

```sql
CREATE TABLE customers (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email text NOT NULL UNIQUE, name text NOT NULL, city text,
  created_at timestamptz NOT NULL DEFAULT now());

CREATE TABLE products (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  sku text NOT NULL UNIQUE, name text NOT NULL, category text NOT NULL,
  price_cents integer NOT NULL CHECK (price_cents >= 0),
  stock integer NOT NULL DEFAULT 0 CHECK (stock >= 0));

CREATE TABLE orders (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id bigint NOT NULL REFERENCES customers(id),
  status text NOT NULL CHECK (status IN ('pending','confirmed','shipped','delivered','cancelled')),
  total_cents integer NOT NULL DEFAULT 0,
  created_at timestamptz NOT NULL DEFAULT now());

CREATE TABLE order_items (
  order_id bigint NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id bigint NOT NULL REFERENCES products(id),
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price_cents integer NOT NULL CHECK (unit_price_cents >= 0),
  PRIMARY KEY (order_id, product_id));
```

Seed hint: use `generate_series(1, 1000)` with `random()` and modulo arithmetic to insert 1,000 customers, 200 products, 100,000 orders and about 300,000 items so that indexes and `EXPLAIN` become interesting. Look up `generate_series` in the PostgreSQL docs yourself.

Queries to write (increasing difficulty):

1. All customers in Surat, newest first.
2. Products with stock under 10, cheapest first, top 5.
3. Orders in the last 7 days with the customer name (join).
4. Customers who have never placed an order (`LEFT JOIN ... IS NULL`, then again with `NOT EXISTS`).
5. Number of orders and total revenue per status.
6. Revenue per month for the last 12 months, excluding cancelled orders (`date_trunc`).
7. Top 5 customers by total spend (CTE).
8. For each order, recompute the total from `order_items` and list orders where it does not match `orders.total_cents`.
9. Best-selling product per category (window function `ROW_NUMBER`).
10. Products never sold.
11. Average order value per city, only cities with at least 20 orders (`HAVING`).
12. The 20 latest orders after a cursor (keyset pagination on `(created_at, id)`).
13. In a transaction: create an order with two items and decrement stock, failing cleanly when stock is short.
14. An `UPDATE ... RETURNING` that marks stale `pending` orders (older than 30 days) as `cancelled`, run first as a `SELECT` to preview.
15. Add an index that speeds up query 3, and prove it with `EXPLAIN ANALYZE` before and after.

### Indexes, query plans, and reading EXPLAIN

**[Must learn now]** An **index** is a separate sorted structure (usually a B-tree) that lets the database find rows without reading the whole table. Analogy: the index at the back of a book. Costs: extra disk space and slower writes, since every insert/update also updates the indexes. Rules of thumb:

- Index columns used in `WHERE`, `JOIN ... ON`, and `ORDER BY` on large tables. FK columns are not indexed automatically in PostgreSQL; add them when you join or delete on them.
- A composite index `(customer_id, created_at DESC)` serves "this customer's latest orders"; column order matters (leftmost columns first).
- `UNIQUE` constraints create an index for you; primary keys too.
- Low-selectivity columns (a boolean) are poor index candidates alone; **partial indexes** (`WHERE status = 'pending'`) help.
- `LIKE '%abc'` and functions on the column (`lower(email)`) cannot use a plain index; use an expression index or trigram/full-text index.
- Do not guess: measure. Read [Indexes](https://www.postgresql.org/docs/current/indexes.html) and [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html).

**Reading EXPLAIN.** `EXPLAIN` shows the plan the planner chose without running the query. `EXPLAIN ANALYZE` actually runs it and adds real timings and row counts. Because it executes the statement, wrap `INSERT/UPDATE/DELETE` in a transaction and `ROLLBACK`. Official guide: [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html). The plan is a tree; read it from the innermost (most indented) node outward.

> **Honest note:** the output below is an illustrative example written by me to teach the format, not copied from a real run on your machine. Your numbers will differ.

```text
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE customer_id = 42 ORDER BY created_at DESC LIMIT 20;

Limit  (cost=0.42..9.81 rows=20 width=40) (actual time=0.03..0.09 rows=20 loops=1)
  ->  Index Scan using orders_customer_created_idx on orders
        (cost=0.42..48.9 rows=104 width=40) (actual time=0.03..0.08 rows=20 loops=1)
        Index Cond: (customer_id = 42)
Planning Time: 0.15 ms
Execution Time: 0.12 ms
```

What to look at:

| Item | Meaning | Red flag |
|---|---|---|
| Node type | `Seq Scan` reads the whole table; `Index Scan`/`Index Only Scan`/`Bitmap Heap Scan` use an index | `Seq Scan` on a big table with a selective filter |
| `cost=a..b` | The planner's guess (arbitrary units): startup cost..total cost | Compare plans of the same query; not milliseconds |
| `rows=` estimated vs `actual rows=` | How good the planner's guess was | Estimate off by 10x or more: stale stats, run `ANALYZE` |
| `actual time=a..b` | Real ms per loop for first row..all rows | Multiply by `loops` for the true total |
| `loops` | How many times the node ran | Large loops on an inner node (nested loop on many rows) |
| `Rows Removed by Filter` | Rows read then thrown away | Millions removed means a missing or unusable index |
| `Buffers: shared hit/read` | Pages from cache vs disk | Many `read` means disk I/O |
| Join type | Nested Loop, Hash Join, Merge Join | Nested Loop with big outer side and no inner index |
| `Sort Method: external merge` | Sorted on disk | Sort too big for `work_mem`, or add an index matching `ORDER BY` |
| `Planning Time` / `Execution Time` | Totals | Planning is usually small |

A routine for slow queries: run `EXPLAIN (ANALYZE, BUFFERS)`, find the node with the most actual time, check estimate vs actual rows, check whether a suitable index exists and is usable, add or fix the index, re-run. For tiny tables PostgreSQL will correctly choose `Seq Scan` even with an index; test with realistic data volume.

**Common mistake:** indexing every column; testing on 50 rows and concluding the index is useless; wrapping an indexed column in a function.

**Interview questions:** How does a B-tree index work in simple terms? Why can an index make writes slower? What does `Seq Scan` mean and is it always bad? What is a composite index and why does column order matter? How do you find a slow query in production (`pg_stat_statements`, slow query log)?

### Transactions, ACID, isolation, and concurrent updates

**[Must learn now]** A **transaction** groups statements so they all succeed or all fail (`BEGIN` ... `COMMIT` / `ROLLBACK`). **ACID**: Atomicity (all or nothing), Consistency (constraints always hold), Isolation (transactions do not see each other's half-done work), Durability (committed data survives a crash). See [Transactions tutorial](https://www.postgresql.org/docs/current/tutorial-transactions.html).

**Isolation levels** in PostgreSQL (verified from the [official page](https://www.postgresql.org/docs/current/transaction-iso.html)): the default is **Read Committed**, where each statement sees data committed before that statement began. **Repeatable Read** gives one snapshot per transaction. **Serializable** guarantees results as if transactions ran one at a time, but you must be ready to retry on serialization failure (SQLSTATE `40001`). Read Uncommitted behaves like Read Committed in PostgreSQL.

**The classic bug: lost update / overselling.**

```sql
-- UNSAFE: two requests both read stock = 1, both pass the check
SELECT stock FROM products WHERE id = 7;           -- app checks stock >= 1
UPDATE products SET stock = stock - 1 WHERE id = 7;

-- SAFE option 1: lock the row for the transaction
BEGIN;
SELECT stock FROM products WHERE id = 7 FOR UPDATE; -- second request waits here
-- check, insert items, then:
UPDATE products SET stock = stock - 1 WHERE id = 7;
COMMIT;

-- SAFE option 2: one atomic conditional update; check rows affected = 1
UPDATE products SET stock = stock - 1 WHERE id = 7 AND stock >= 1;
```

Lock products in a consistent order (for example by id) to avoid **deadlocks**; PostgreSQL will abort one transaction on a deadlock and you retry. Keep transactions short: never call a slow external API while holding row locks. See [Explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) for later study.

**Common mistake:** check-then-act without a lock or constraint; long transactions holding locks; forgetting to roll back on error in application code.

**Interview questions:** Explain ACID with an example. What is a dirty read, non-repeatable read, phantom read? What does `SELECT ... FOR UPDATE` do? How would you retry on serialization failure? What is a deadlock and how do you avoid it?

### Migrations

**[Must learn now]** A **migration** is a versioned, reviewed script that changes the schema (like Git for the database). Never edit the production schema by hand. Rules: one change per migration; each has "up" (and ideally "down"); migrations are committed; they run in CI and deploy; make changes backward compatible (add a nullable column, deploy code, backfill, then add `NOT NULL`) so old and new app versions can run together during deploy (expand/contract). Tools for Node: [node-pg-migrate](https://github.com/salsita/node-pg-migrate) (plain SQL or JS), or the migrations of Prisma/Drizzle. In Python you will use Alembic (Phase 9).

**Common mistake:** editing an already-applied migration; destructive migrations without a backup; adding an index on a huge table in a way that locks writes (look up `CREATE INDEX CONCURRENTLY`).

**Interview questions:** Why migrations instead of manual SQL? How do you change a column type with zero downtime? What is expand/contract?

### Connection pooling

**[Must learn now]** Opening a database connection is expensive and each PostgreSQL connection uses real memory, so a server allows only a limited number (`max_connections`). A **pool** keeps a few connections open and lends them out. With `pg`, use one `Pool` per process, run simple queries with `pool.query`, and for transactions check out a client with `pool.connect()` and always `release()` in `finally`. See [node-postgres pooling](https://node-postgres.com/features/pooling). Pool size times number of app instances must stay below the database limit. With serverless functions or many instances, put an external pooler (such as PgBouncer or a managed pooler) in front. Pool timeouts matter: set a connection timeout so requests fail fast instead of hanging.

**Common mistake:** creating a new `Client` per request; forgetting `release()`; huge pool sizes ("more is faster" is false).

**Interview questions:** Why do we need a pool? What happens when the pool is exhausted? How does pooling interact with serverless?

### Pagination in SQL

**[Must learn now]** Offset: `ORDER BY created_at DESC, id DESC LIMIT 20 OFFSET 40`; the database still reads and discards the first 40 rows, so deep pages get slow. Keyset: `WHERE (created_at, id) < ($1, $2) ORDER BY created_at DESC, id DESC LIMIT 20` with an index on `(created_at DESC, id DESC)`; cost is constant. Always include a unique tie-breaker (`id`).

**Common mistake:** unstable ordering; `COUNT(*)` of millions on every request (cache it or return "has more").

**Interview questions:** Why is large OFFSET slow? How do you build a cursor?

### Backups and restores

**[Must learn now]** A backup you have not restored is a hope, not a backup. Know two kinds: **logical** (`pg_dump`/`pg_restore`, portable, good for small to medium databases) and **physical/continuous** (base backups plus WAL archiving for point-in-time recovery). Read [Backup and Restore](https://www.postgresql.org/docs/current/backup.html), [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html), [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html) and [continuous archiving](https://www.postgresql.org/docs/current/continuous-archiving.html). Managed databases do automated backups, but you must still know retention, how to restore to a new instance, and how long it takes (RPO = how much data you can lose; RTO = how long you can be down).

```bash
pg_dump --format=custom --file=orders.dump "$DATABASE_URL"
createdb orders_restore_test
pg_restore --dbname=orders_restore_test --no-owner orders.dump
```

**Common mistake:** storing backups on the same disk as the database; never testing a restore.

**Interview questions:** Logical vs physical backup? What are RPO and RTO? How would you recover from an accidental `DELETE` without `WHERE`?

### MongoDB: documents, collections, BSON, CRUD

**[Must learn now]** You know the basics, so focus on the model. MongoDB stores **documents** (JSON-like, stored as **BSON**, a binary format with extra types such as `ObjectId`, `Date`, `Decimal128`) in **collections** (like tables without a fixed schema). CRUD: `insertOne/insertMany`, `find`, `updateOne` with operators (`$set`, `$inc`, `$push`), `deleteOne`. See the manual: [CRUD](https://www.mongodb.com/docs/manual/crud/). Use `Decimal128` or integer cents for money, never doubles.

**Common mistake:** replacing whole documents with `replaceOne` by accident (use `$set`); unbounded growing arrays.

**Interview questions:** What is BSON? What is `_id`? How do `updateOne` and `replaceOne` differ?

### MongoDB schema design, validation, embedding vs referencing

**[Must learn now]** "Schemaless" does not mean "no schema". Decide your schema from **how the data is read**. [Data modeling](https://www.mongodb.com/docs/manual/data-modeling/):

| Embed when | Reference when |
|---|---|
| Data is read together, "contains" relationship | The related data is large, shared or changes independently |
| Child belongs to one parent only | Many parents share a child (M-N) |
| Bounded size (a few addresses) | Unbounded growth (all comments on a post) |
| You need atomic single-document updates | You need to query the child on its own often |

Example: an order document can embed its line items (with price snapshot) because they are read with the order and never shared; the customer is referenced by id (maybe with a small copy of the name). Add **schema validation** with `$jsonSchema` ([Schema Validation](https://www.mongodb.com/docs/manual/core/schema-validation/)) or use Mongoose schemas ([guide](https://mongoosejs.com/docs/guide.html)) for app-level validation. Read about one-to-many embedding in [this pattern page](https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/).

**Common mistake:** copying relational design into Mongo (references everywhere then manual joins), or embedding unbounded arrays until the document hits its size limit (16 MB).

**Interview questions:** Embed or reference for comments? Why is the 16 MB limit relevant? How do you keep denormalized copies consistent?

### MongoDB indexes, aggregation, relationships and consistency

**[Must learn now]** Indexes work like in SQL (B-tree): single field, compound (order matters), unique, TTL (auto-expire), text. Use `explain("executionStats")` to see `COLLSCAN` vs `IXSCAN` (the Mongo equivalent of Seq Scan vs Index Scan). See [Indexes](https://www.mongodb.com/docs/manual/core/indexes/). The **aggregation pipeline** ([docs](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)) passes documents through stages: `$match` (filter early so indexes help), `$group`, `$sort`, `$project`, `$lookup` (a left outer join; expensive, so do not design around it), `$unwind`.

```js
db.orders.aggregate([
  { $match: { status: { $ne: "cancelled" }, createdAt: { $gte: since } } },
  { $group: { _id: "$customerId", spent: { $sum: "$totalCents" } } },
  { $sort: { spent: -1 } }, { $limit: 10 },
]);
```

Consistency: single-document writes are atomic. Multi-document [transactions](https://www.mongodb.com/docs/manual/core/transactions/) exist (they need a replica set) but are slower and signal that the model may need rethinking; if you need them everywhere, PostgreSQL is probably the better tool.

**Common mistake:** `$match` after `$group` (no index use); `$lookup` on large unindexed collections.

**Interview questions:** What does `COLLSCAN` mean? When is a compound index order important? How do you keep two collections consistent without joins?

### MongoDB vs PostgreSQL: suitability

**[Must learn now]** Decide with facts, not fashion.

| Question | Lean PostgreSQL | Lean MongoDB |
|---|---|---|
| Data shape | Well-defined, relational (orders, payments, inventory) | Varied, nested, evolving (content, events, catalogs with different attributes) |
| Integrity | Strong constraints, FKs, multi-row transactions | Documents mostly self-contained |
| Queries | Ad hoc joins, reporting, aggregates | Fetch whole aggregate by key or simple filters |
| Team skill | SQL known | JS/JSON-first team |
| AI/RAG | pgvector keeps vectors next to data (Phase 12) | Atlas vector search exists; separate service |

> **Honest note:** PostgreSQL with `jsonb` can cover many "flexible data" cases, and Mongo can do transactions, so the line is blurry. For money, stock and strict relations, choose PostgreSQL. Default for new projects in this roadmap: PostgreSQL.

**Interview questions:** When would you choose MongoDB over PostgreSQL, honestly? Can PostgreSQL store JSON?

### ORM concepts

**[Must learn now]** An **ORM** (Object-Relational Mapper) lets you work with rows as objects and generates SQL. Analogy: a translator; handy, but you must still understand the language. Benefits: less boilerplate, type help, migrations (in some). Costs: hidden queries, **N+1 problem** (1 query for orders, then 1 query per order for items; fix with a join/eager load/batch), leaky abstractions, and slow complex reports. Related ideas: **identity map** and **unit of work** (a session tracks changed objects and flushes them together), **lazy vs eager loading**, **active record vs data mapper**. In Node, compare raw `pg` + SQL, a query builder (Knex, Kysely), and ORMs ([Prisma](https://www.prisma.io/docs), [Drizzle](https://orm.drizzle.team/docs/overview)). Recommendation: raw SQL for Project 2 to learn fundamentals; try Drizzle or Prisma for one module to compare, only after the raw version works. Always log generated SQL in development.

**Common mistake:** letting the ORM hide an N+1 for months; fetching whole rows when you need two columns.

**Interview questions:** What is the N+1 problem and how do you fix it? ORM vs query builder vs raw SQL trade-offs? What is lazy loading?

### SQLAlchemy introduction (preview for Phase 9)

**[Learn during projects]** SQLAlchemy is Python's main database toolkit and ORM; you will use it in Phase 9 with FastAPI. Key vocabulary now, so Phase 9 is easier: **Engine** (connection pool plus dialect), **Session** (unit of work: holds objects, one transaction at a time), **declarative models** (`DeclarativeBase`, `Mapped[...]`, `mapped_column`), **relationships** (`relationship()`), `select()` statements (2.0 style), and **Alembic** for migrations. SQLAlchemy 2.0 style differs from many old tutorials (which use the legacy `session.query`), so follow the [2.0 ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) and [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html). In Week 9 only read the quickstart and map your four practice tables on paper; real coding comes after you learn Python (Phase 8).

**Interview questions:** Engine vs Session? What is a unit of work? Why is `session.query` considered legacy style in 2.0?

### Database access patterns and data-access testing

**[Must learn now]** Patterns: **repository** (one module per entity owns all queries), **transaction helper** (`withTransaction(fn)` that begins, commits, rolls back and releases), **service-level transactions** (the service decides what is atomic, repositories accept a client), and **read models** for reports (dedicated SQL views/queries rather than forcing them through the ORM). Add timeouts (`statement_timeout`), and retry only idempotent operations or serialization failures.

Data-access testing: test repositories against a **real PostgreSQL** (a local container or a separate test database), not a mock. Apply migrations once, then isolate each test: truncate tables between tests, or run each test inside a transaction you roll back. Build small **factories** (`makeCustomer()`) rather than large fixtures. Test constraints too: inserting a negative stock must fail; deleting a product used by an order must fail. Test the concurrency case with `Promise.all` of two order creations. In-memory fake databases (SQLite instead of Postgres) hide real behavior differences; avoid them for anything with locking, types, or JSON.

```js
test("cannot oversell the last unit", async () => {
  await seedProduct({ id: 1, stock: 1 });
  const results = await Promise.allSettled([createOrder(1), createOrder(1)]);
  expect(results.filter((r) => r.status === "fulfilled")).toHaveLength(1);
  expect(await getStock(1)).toBe(0);
});
```

**Common mistake:** tests that pass only because the mock returns what you told it; shared state between tests; ignoring constraint tests.

**Interview questions:** How do you test code that talks to the database? Why not mock the database? How do you isolate tests?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
|---|---|---|---|---|---|---|
| SQL fundamentals | Tables, types, CRUD, filters, aggregates | [PostgreSQL tutorial: SQL](https://www.postgresql.org/docs/current/tutorial-sql.html), [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html) | [Learn PostgreSQL Tutorial - Full Course for Beginners (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=qw--VYLpxG4) | Beginner | 3 h (watch selected parts) | Create practice schema, queries 1 to 5 |
| Joins and CTEs | Joins, subqueries, CTEs, windows | [Joins](https://www.postgresql.org/docs/current/tutorial-join.html), [WITH queries](https://www.postgresql.org/docs/current/queries-with.html), [Window functions](https://www.postgresql.org/docs/current/tutorial-window.html) | [Learn SQL Joins (Decomplexify, English)](https://www.youtube.com/watch?v=nivyaiCeWjs) | Beginner to intermediate | 2 h | Practice queries 3 to 11 |
| Indexes and EXPLAIN | B-tree, composite, partial, plans | [Indexes](https://www.postgresql.org/docs/current/indexes.html), [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) | [A beginners guide to EXPLAIN ANALYZE - Michael Christofides (Tiger Data channel, English)](https://www.youtube.com/watch?v=31EmOKBP1PY) | Intermediate | 2 h | Query 15: before/after index with plans |
| Transactions and isolation | ACID, locks, retries | [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html), [Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [Explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Overselling test with two sessions in `psql` |
| Migrations and pooling | node-pg-migrate, Pool | [node-pg-migrate](https://github.com/salsita/node-pg-migrate), [node-postgres pooling](https://node-postgres.com/features/pooling) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Add a migration with a safe backfill |
| Backup and restore | pg_dump, restore, PITR idea | [Backup and Restore](https://www.postgresql.org/docs/current/backup.html), [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) | No video verified for this topic; use the official documentation above. | Intermediate | 1 h | Dump, restore to a new DB, compare row counts |
| MongoDB core | CRUD, BSON, indexes, aggregation | [CRUD](https://www.mongodb.com/docs/manual/crud/), [Indexes](https://www.mongodb.com/docs/manual/core/indexes/), [Aggregation](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/) | [MongoDB Crash Course (Traversy Media, English)](https://www.youtube.com/watch?v=-56x56UppqQ); Hindi option: [MongoDB Crash Course (Hindi) (Geeky Shows)](https://www.youtube.com/watch?v=02Y1Bciz8jk) | Beginner to intermediate | 2 h | Rebuild the revenue-per-customer query as a pipeline |
| MongoDB modeling | Embed vs reference, validation | [Data modeling](https://www.mongodb.com/docs/manual/data-modeling/), [Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/) | [MongoDB Crash Course - Schemas and Relationships (The Full Stack Junkie, English)](https://www.youtube.com/watch?v=DdvhZj7SsEM) | Intermediate | 1.5 h | Model the same orders domain in Mongo and compare |
| ORM and SQLAlchemy | N+1, Session, Engine | [SQLAlchemy 2.0 quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [Prisma](https://www.prisma.io/docs), [Drizzle](https://orm.drizzle.team/docs/overview) | [SQLAlchemy: The BEST SQL Database Library in Python (ArjanCodes, English)](https://www.youtube.com/watch?v=aAy-B6KPld8) (introductory, see notes) | Intermediate | 1.5 h | Sketch the four tables as SQLAlchemy models on paper |
| Data-access testing | Real DB, isolation, factories | [Vitest](https://vitest.dev), [node:test](https://nodejs.org/api/test.html) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Constraint and concurrency tests for Project 2 |

## Verification notes

- **Network limitation:** `www.youtube.com` was unreachable from my machine, so I checked each video with `noembed.com` (a relay of YouTube oEmbed) to confirm real title and channel for each ID. I did not run the `lengthSeconds` check. **All durations are NOT verified.** I did not watch the videos.
- Learn PostgreSQL Tutorial - Full Course for Beginners, freeCodeCamp.org (ID qw--VYLpxG4): title and channel confirmed. A search summary suggested this course is several hours long; exact length NOT verified, so watch only the sections on tables, SELECT, joins and constraints.
- Learn SQL Joins, channel Decomplexify (ID nivyaiCeWjs): title and channel confirmed; language English assumed from title, NOT verified.
- A beginners guide to EXPLAIN ANALYZE - Michael Christofides, channel shown as "Tiger Data (creators of TimescaleDB)" (ID 31EmOKBP1PY): title and channel confirmed. It is a conference-style talk (5 years old according to a search snippet); PostgreSQL's EXPLAIN output has been stable, but check details against the current official page.
- MongoDB Crash Course, Traversy Media (ID -56x56UppqQ): title and channel confirmed; its upload year is NOT verified (a similarly titled 2021 or 2022 version exists on the channel, so I did not rely on the date). Mongo concepts are stable; ignore any installation steps that look old.
- MongoDB Crash Course (Hindi), channel Geeky Shows (ID 02Y1Bciz8jk): title and channel confirmed; language "Hindi" is from the title. Quality and depth NOT verified.
- MongoDB Crash Course - Schemas and Relationships, channel The Full Stack Junkie (ID DdvhZj7SsEM): title and channel confirmed; I did not check its content beyond the title, so treat it as optional and prefer the official data modeling page.
- SQLAlchemy: The BEST SQL Database Library in Python, ArjanCodes (ID aAy-B6KPld8): title and channel confirmed. A search snippet said it is sponsored and broad; I could NOT confirm it uses the 2.0 style. Use it only for orientation and rely on the official 2.0 docs. No better verified SQLAlchemy video was found.
- Playlists were not verified (the relay did not support them), so none are recommended.
- Official docs: every page linked was fetched and its title read. The PostgreSQL isolation page was read for content. The EXPLAIN example in this file is illustrative and not from a real run.

## Hands-on exercises

1. Run PostgreSQL locally, create the practice schema, and seed 100,000 orders with `generate_series`.
2. Write practice queries 1 to 15 from the list above, saving them in a `queries.sql` file with comments.
3. For query 3 and query 12, run `EXPLAIN (ANALYZE, BUFFERS)` before and after adding an index. Write three sentences about what changed (node types, actual time, rows removed by filter).
4. Open two `psql` sessions and reproduce the overselling bug, then fix it with `FOR UPDATE`, then with the conditional `UPDATE`.
5. Force a deadlock in two sessions by locking two rows in opposite order, read the error, and fix the order.
6. Write two migrations with node-pg-migrate: one adds a nullable column, one backfills and sets `NOT NULL`.
7. Take a `pg_dump`, restore into a new database, and compare row counts.
8. Model the same orders domain in MongoDB (embedded items), insert 1,000 documents, and write the revenue-per-customer aggregation. List two things that were easier and two that were harder than in SQL.
9. Write repository tests for Project 2: a constraint test, a concurrency test, and a rollback test.
10. Demonstrate an N+1 pattern with a loop of queries, then replace it with a single join; compare timing.

## Checkpoint

**Explain:**
- Why is `price_cents` copied into `order_items`?
- What does `Rows Removed by Filter: 99952` tell you about a plan?
- Why can two concurrent requests oversell stock, and what are two ways to prevent it?
- Embed vs reference: give one example of each from the orders domain.

**Modify code:**
- Convert the offset list query to keyset pagination and add the right composite index.
- Change a migration so that adding a `NOT NULL` column does not break the running app version.

**Debug:**
- A query is slow only in production: use `EXPLAIN ANALYZE` to find the estimate-versus-actual row mismatch and run `ANALYZE`.
- `could not serialize access due to concurrent update`: explain why and how the code should retry.
- The app freezes under load: find a pool client that is never released.

**Write tests:**
- A repository test that proves a negative stock insert fails.
- A concurrency test for the last unit of stock.
- A test that deleting a customer with orders is blocked.

**Ready to move on when:** you can design a normalized schema for a small business domain from a text description, write the joins and aggregates for typical reports, read an `EXPLAIN ANALYZE` plan and fix a slow query with an index, write a safe stock-decrement transaction, and describe when you would pick Mongo instead of PostgreSQL.

## Week plan

### Week 9 — PostgreSQL and MongoDB data modeling  (estimated hours: 10)

**Learning objectives**
- Design a normalized relational schema with proper constraints.
- Write confident SQL: joins, aggregates, CTEs, a window function.
- Use indexes and read `EXPLAIN ANALYZE` plans.
- Explain transactions, isolation and fix a concurrency bug.
- Model the same domain in MongoDB and justify when to use each.
- Understand ORM ideas and SQLAlchemy vocabulary; know how to test data access.

**Topics and subtopics**
- **[Must learn now]** Tables, types, PK/FK, constraints, normalization, relationships (1.5 h)
- **[Must learn now]** CRUD, joins, aggregates, subqueries, CTEs: practice queries 1 to 12 (2.5 h)
- **[Must learn now]** Indexes and EXPLAIN reading (1.5 h)
- **[Must learn now]** Transactions, ACID, isolation, locking, deadlocks (1.5 h)
- **[Must learn now]** Migrations, pooling, pagination, backup and restore (1 h)
- **[Must learn now]** MongoDB modeling, indexes, aggregation, comparison (1.5 h)
- **[Learn during projects]** ORM concepts, N+1, SQLAlchemy vocabulary, data-access testing (1 h; connect back to Project 2)
- **[Learn later if needed]** Recursive CTEs, partitioning, replication, advanced locking

**Small prerequisite concepts**
- Set theory feel: rows in, rows out; a join is a filtered product.
- Reading a terminal client (`psql`) and running a `.sql` file.
- Basic big-O intuition: scanning vs searching a sorted structure.

**Reading**
- [PostgreSQL tutorial: SQL language](https://www.postgresql.org/docs/current/tutorial-sql.html), [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), [Transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [MongoDB data modeling](https://www.mongodb.com/docs/manual/data-modeling/), [SQLAlchemy 2.0 ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)

**Video**
- Learn PostgreSQL Tutorial - Full Course for Beginners, freeCodeCamp.org, English, duration not verified (watch selected parts): [link](https://www.youtube.com/watch?v=qw--VYLpxG4)
- Learn SQL Joins, Decomplexify, language not verified (title is English), duration not verified: [link](https://www.youtube.com/watch?v=nivyaiCeWjs)
- A beginners guide to EXPLAIN ANALYZE, Michael Christofides (Tiger Data channel), English, duration not verified: [link](https://www.youtube.com/watch?v=31EmOKBP1PY)
- MongoDB Crash Course, Traversy Media, English, duration not verified: [link](https://www.youtube.com/watch?v=-56x56UppqQ). Hindi option: MongoDB Crash Course (Hindi), Geeky Shows, duration not verified: [link](https://www.youtube.com/watch?v=02Y1Bciz8jk)

**Hands-on exercises**
1. Hands-on exercises 1 and 2 above (schema, seed, queries).
2. Exercises 3 and 4 (EXPLAIN before/after, overselling in two sessions).
3. Exercises 6 and 7 (migrations, dump and restore).
4. Exercise 8 (Mongo modeling and aggregation).
5. Exercise 9 (data-access tests added to Project 2), then fix any real bug they reveal.

**What you must build**
A `queries.sql` file with answers to all 15 practice queries plus before/after EXPLAIN notes, a short written comparison "Orders in PostgreSQL vs MongoDB" (half a page), and new data-access tests in Project 2 (constraint, rollback, concurrency).

**Completion checklist**
- [ ] Practice schema created with 100,000+ orders seeded.
- [ ] Queries 1 to 15 written by you; hints, not answers, from AI.
- [ ] One query sped up with an index and proven by EXPLAIN ANALYZE.
- [ ] Overselling bug reproduced and fixed two ways.
- [ ] Backup restored into a new database and verified.
- [ ] Orders domain modeled in MongoDB; comparison note written.
- [ ] Project 2 has repository tests including a concurrency test.

**Self-test**
1. What is the difference between `WHERE` and `HAVING`?
2. Why might PostgreSQL ignore your index and do a `Seq Scan`?
3. Which isolation level is the default in PostgreSQL, and what anomaly can still happen?
4. What is the N+1 problem?
5. Give one case where you would embed in Mongo and one where you would reference.

**Common mistakes**
- Learning only by watching; not typing queries.
- Testing indexes on tiny tables.
- Using floats for money.
- Using `OFFSET` for deep pagination.
- Treating ORMs as magic, or mocking the database in tests.
- Never testing a restore.

**Ready to continue when:** you can produce the schema, the report queries and a safe order transaction from a one-page requirement, and explain an EXPLAIN ANALYZE output line by line.

**Slower-track option:** Do PostgreSQL fully and cut MongoDB to modeling plus one aggregation (skip the video). Do queries 1 to 10 and 15 only, skip window functions, recursive CTEs, deadlock exercise, and SQLAlchemy reading (it returns in Phase 9). Spend the saved time on the concurrency test in Project 2. Revisit the rest in the weekly revision slots.

## Sources

All URLs below were opened (HTTP 200 and page title read) on 2026-10-09 unless noted. YouTube items were checked via noembed.com (title and channel), not on youtube.com directly.

- https://nodejs.org/en/learn/getting-started/introduction-to-nodejs
- https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick
- https://nodejs.org/en/learn/getting-started/security-best-practices
- https://nodejs.org/api/test.html
- https://expressjs.com/en/guide/routing.html
- https://expressjs.com/en/guide/using-middleware.html
- https://expressjs.com/en/guide/writing-middleware.html
- https://expressjs.com/en/guide/error-handling.html
- https://expressjs.com/en/guide/migrating-5.html (content read)
- https://expressjs.com/en/blog/2025-03-31-v5-1-latest-release (content read)
- https://expressjs.com/en/advanced/best-practice-security.html
- https://registry.npmjs.org/express/latest and https://registry.npmjs.org/-/package/express/dist-tags (express 5.3.0, latest-4 4.22.3)
- https://nodejs.org/dist/index.json (Node v24 LTS)
- https://zod.dev
- https://github.com/ranisalt/node-argon2
- https://github.com/ladjs/supertest
- https://github.com/express-rate-limit/express-rate-limit
- https://github.com/expressjs/multer
- https://github.com/expressjs/cors
- https://github.com/websockets/ws
- https://github.com/salsita/node-pg-migrate
- https://helmetjs.github.io
- https://getpino.io
- https://vitest.dev
- https://docs.bullmq.io
- https://12factor.net/config
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
- https://nextjs.org/docs/app/getting-started/route-handlers
- https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events
- https://node-postgres.com/features/pooling
- https://www.pgadmin.org
- https://www.postgresql.org/docs/current/tutorial-sql.html
- https://www.postgresql.org/docs/current/tutorial-join.html
- https://www.postgresql.org/docs/current/tutorial-agg.html
- https://www.postgresql.org/docs/current/tutorial-window.html
- https://www.postgresql.org/docs/current/tutorial-transactions.html
- https://www.postgresql.org/docs/current/ddl-constraints.html
- https://www.postgresql.org/docs/current/queries-with.html
- https://www.postgresql.org/docs/current/queries-limit.html
- https://www.postgresql.org/docs/current/indexes.html
- https://www.postgresql.org/docs/current/sql-createindex.html
- https://www.postgresql.org/docs/current/using-explain.html
- https://www.postgresql.org/docs/current/transaction-iso.html (content read)
- https://www.postgresql.org/docs/current/explicit-locking.html
- https://www.postgresql.org/docs/current/backup.html
- https://www.postgresql.org/docs/current/app-pgdump.html
- https://www.postgresql.org/docs/current/app-pgrestore.html
- https://www.postgresql.org/docs/current/continuous-archiving.html
- https://www.mongodb.com/docs/manual/crud/
- https://www.mongodb.com/docs/manual/data-modeling/
- https://www.mongodb.com/docs/manual/tutorial/model-embedded-one-to-many-relationships-between-documents/
- https://www.mongodb.com/docs/manual/core/schema-validation/
- https://www.mongodb.com/docs/manual/core/indexes/
- https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
- https://www.mongodb.com/docs/manual/core/transactions/
- https://mongoosejs.com/docs/guide.html
- https://www.prisma.io/docs
- https://orm.drizzle.team/docs/overview
- https://docs.sqlalchemy.org/en/20/orm/quickstart.html (HTTP 200; title not extracted)
- https://docs.sqlalchemy.org/en/20/orm/session_basics.html (HTTP 200; title not extracted)
- Videos (title and channel via noembed): https://www.youtube.com/watch?v=CnH3kAXSrmU , https://www.youtube.com/watch?v=mbsmsi7l3r4 , https://www.youtube.com/watch?v=LZq0G8WUaII , https://www.youtube.com/watch?v=3r4Ja7i763c , https://www.youtube.com/watch?v=qw--VYLpxG4 , https://www.youtube.com/watch?v=nivyaiCeWjs , https://www.youtube.com/watch?v=31EmOKBP1PY , https://www.youtube.com/watch?v=-56x56UppqQ , https://www.youtube.com/watch?v=02Y1Bciz8jk , https://www.youtube.com/watch?v=DdvhZj7SsEM , https://www.youtube.com/watch?v=aAy-B6KPld8
