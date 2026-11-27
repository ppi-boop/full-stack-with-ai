# Phase 05 — Next.js App Router & Vercel AI SDK Master Handbook

> **Version note:** Based on the roadmap's docs check dated 2026-10-09 (Next.js 16.x). Next.js changes fast; if something here disagrees with nextjs.org, the docs win.

---

# Topic 1: Setup, Project Structure & Routing

### 1. Simple Definitions
* **App Router:** Next.js's current routing system. The `app/` folder IS the URL map.
* **Route:** A URL path that shows a page (e.g. `/dashboard/orders`).
* **Layout:** A wrapper shared by every page under it; it persists while child pages change.
* **Dynamic segment:** A varying URL part written `[id]` (`/orders/123` and `/orders/456` share one file).
* **Route group:** A folder in `(parentheses)`. Organises files; NOT part of the URL.

### 2. The Essentials
1. **Create:** `npx create-next-app@latest my-app`, then `npm run dev`. Needs Node 20.9+ and TypeScript 5.1+. Defaults: TypeScript, ESLint, Tailwind, App Router, Turbopack (default bundler). `next build` no longer runs the linter in v16, so run ESLint separately.
2. **Folder tree = URL map.** Only `page.tsx` (or `route.ts`) makes a folder reachable. A folder without `page.tsx` is not a page. Only `(parentheses)` folders vanish from the URL; normal folders (like `settings`) stay.
3. **Special files:** `page.tsx` (UI), `layout.tsx` (persistent wrapper; root layout must contain `<html>` and `<body>`), `loading.tsx` (automatic Suspense fallback), `error.tsx` (error boundary; must be `"use client"`), `not-found.tsx` (404 UI via `notFound()`), `route.ts` (API endpoint).
4. **Layouts persist** across child navigation (no re-render, state kept). `template.tsx` remounts each time. Security trap: an auth check only in a layout doesn't re-run on every navigation; also check in the page / data layer.
5. **Next.js 16: `params`, `searchParams`, `cookies()`, `headers()` are async only.** Type `params` as a Promise and `await` it.
6. **Navigation:** `<Link>` (prefetches), `useRouter()` from `next/navigation` (Client Components only), `redirect()` / `notFound()` on the server. Don't use `<a>` for internal links (full reload).
7. **Loading:** `loading.tsx` wraps the page in Suspense; for precision wrap just the slow component in `<Suspense fallback>`.
8. **Private folders** start with `_` (e.g. `_components`) and are never routes.
9. **Old vs new:** Pages Router (`pages/`, `getServerSideProps`) is legacy for new apps. `middleware.ts` is now `proxy.ts`.

### 3. Code Example
```text
app/
  layout.tsx            root layout (<html> + <body>)
  page.tsx              "/"
  dashboard/
    layout.tsx          wraps /dashboard/*
    loading.tsx
    error.tsx
    not-found.tsx
    page.tsx            "/dashboard"
    orders/
      page.tsx          "/dashboard/orders"
      [id]/page.tsx     "/dashboard/orders/123"
  (marketing)/about/page.tsx   "/about"  (group not in URL)
  api/health/route.ts   GET /api/health
```
```tsx
// app/dashboard/orders/[id]/page.tsx (Next.js 16)
export default async function OrderPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const order = await getOrder(id);
  if (!order) notFound();
  return <OrderDetails order={order} />;
}
```

### 4. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `params.id` without `await` | Hard error in Next.js 16 |
| Folder without `page.tsx` expected to be a page | No `page.tsx` = no route (404) |
| `<a href>` for internal links | Full page reload, state lost |
| `useRouter` in a Server Component | It's a hook; needs `"use client"` |
| Auth check only in `layout.tsx` | Layouts don't re-run on every navigation |
| Following a Pages Router tutorial | Different, legacy system |
| Slow read in the layout, expecting `loading.tsx` to cover it | Put slow reads in the page or its own `<Suspense>` |
| Treating every folder like a route group | Only `(parentheses)` folders disappear from the URL |

### 5. Practice Checks (passed)
* Tree reading: `(shop)/products/[id]` gives `/products/123` (group dropped); `dashboard/` with no `page.tsx` has no `/dashboard` route; `_components` is private.
* Retry: `(blog)/posts`, `(blog)/posts/[slug]`, `settings/profile` give `/posts`, `/posts/hello`, `/settings/profile`. **Slip to recheck in Project 1:** `settings` is a normal folder, so it stays in the URL (I answered `/profile`).
* `params.id` fix (not self-solved, explained): type as `Promise<{ id: string }>` and `const { id } = await params;`.

### 6. Optional / Later (not needed now)
* Parallel routes (`@slot`; v16 requires `default.tsx`) and intercepting routes (modals).
* `npx next typegen` for `PageProps<'/route'>` helper types.
* Catch-all routes (`[...slug]`), `generateStaticParams`.

---

# Topic 2: Server Components vs Client Components

### 1. Real-Time Example: Opening `/products` on an online shop
```text
 YOU (browser)                              SERVER (Next.js)
 1. Type the URL, press Enter  ──────────▶  2. Receives the request
                                            3. Runs ProductsPage (Server Component):
                                               asks the database for products
                                               (DB password stays here, safe)
                                            4. Builds the finished HTML
 6. Shows the page IMMEDIATELY  ◀─────────  5. Sends that HTML to the browser
 7. Downloads a tiny JS file for just
    the Like button
 8. Like button now works
```
* The browser gets the **finished result**, never the component's code, the DB query or the password.
* Analogy: the server is the **kitchen**, the browser is the **table**. The kitchen prepares the heavy dishes; only interactive things (a pepper grinder) go to the table.
* **When does step 3 run?** At **build time** (`next build`, once, for pages that don't change per user) or at **request time** (each visit, for live data). Topic 3 covers how Next.js chooses.

### 2. Simple Definitions
* **Server Component:** Runs only on the server; can be `async`, read the DB/secrets; sends no component JS to the browser. Default in the App Router.
* **Client Component:** Needs its code in the browser (state, effects, clicks). Still pre-rendered to HTML on the server first, then hydrated.
* **`"use client"`:** "This file must also travel to the browser, because it reacts to the user." It marks the boundary; that file and everything it imports goes into the browser bundle.
* **Hydration:** The browser attaching JavaScript to the server-rendered HTML.

### 3. The Essentials
1. **Default to Server.** Switch to Client only for a piece that reacts to clicks/typing (`onClick`, `onChange`), remembers things (`useState`, `useEffect`, `useRef`, custom hooks), or uses the browser (`window`, `localStorage`).
2. **Keep Client Components small, at the leaves.** Never put `"use client"` on a whole `page.tsx`. Extract just the interactive piece (button + the state it shares, e.g. `HelpToggle` containing the toggle button and the panel).
3. **Why Server Components can't use `useState`/`onClick`:** after the server sends HTML, the component function doesn't exist in the browser; nothing there can run state or react to clicks.
4. Server to client props must be serializable (plain data; no functions except Server Actions, no class instances).
5. A Server Component can sit inside a Client Component if passed as `children` (e.g. `<Modal><CartContents /></Modal>`).
6. Context doesn't work in Server Components: create a client `Providers` that takes `{children}` and render it as deep as possible.
7. Third-party hook-using libs without `"use client"` need your own client wrapper file.
8. **Secrets:** anything a Client Component imports ships to the browser. Env vars without `NEXT_PUBLIC_` become empty strings in client code; `NEXT_PUBLIC_` ones are visible to everyone. Use `import "server-only"` in DB/secret modules so the build fails if a client file imports them.
9. **Hydration mismatch:** if the first client render differs from server HTML (`Date.now()`, `Math.random()`, `localStorage` in render), React warns. Same purity rule as Phase 4 Topic 3.

### 4. Code Example
```tsx
// app/products/page.tsx  (Server Component, no directive)
import { LikeButton } from "./LikeButton";

export default async function ProductsPage() {
  const products = await db.product.findMany();   // runs on the server only
  return (
    <ul>
      {products.map(p => (
        <li key={p.id}>
          {p.name}
          <LikeButton productId={p.id} />          {/* small client island */}
        </li>
      ))}
    </ul>
  );
}

// app/products/LikeButton.tsx
"use client";
import { useState } from "react";

export function LikeButton({ productId }: { productId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(l => !l)}>{liked ? "Liked" : "Like"}</button>;
}
```

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| `useState` / `onClick` in a Server Component | Error: needs a Client Component |
| `"use client"` at the top of `page.tsx` | Pulls the whole page and its imports into the browser bundle |
| Importing DB code or a secret into a client file | Leaks to the browser (or fails the build with `server-only`) |
| Passing a function prop from server to client | Not serializable |
| `NEXT_PUBLIC_` on a secret key | Visible to every visitor |
| `useContext` in a Server Component | Context isn't available; use a client Provider |
| `window` / `localStorage` during render | Crashes on the server or causes a hydration mismatch |
| Client Provider that doesn't take `children` | Everything under it becomes client-side |

### 6. Practice Checks (passed)
* Server or Client: DB product list = Server; Like button with counter = Client; search box filtering as you type = Client; code reading `process.env.DB_PASSWORD` = Server.
* A page with a help toggle using `useState`: move the toggle button AND the panel (shared `open` state) into one new `"use client"` component; keep the page a Server Component.
* Note: the first, rule-heavy version of this lesson wasn't clear. The real-time example version worked. Use that style going forward.

### 7. Optional / Later (not needed now)
* `React.cache` and `use cache` to share data between server components (Topic 3).
* Streaming with Suspense; `use()` to pass promises to client components.
* How the RSC payload works under the hood.

---

# Topic 3: Rendering Modes & Data Fetching / Caching

### 1. Real-Time Example: `myshop.com/products`
```text
+---------------------------------------------+
| Products (heading)          <- same for everyone, never changes      -> STATIC
| List of 20 products         <- changes a few times a day             -> CACHED (1 hour)
| "Your cart has 2 items"     <- different per user, comes from cookie -> DYNAMIC
+---------------------------------------------+
```
1. **Before deploy (build time):** Next.js builds the HTML for everything that can be known in advance. This is the **static shell**.
2. **User opens the page:** the shell arrives immediately (heading + products). The page is never blank.
3. **Then, at request time:** the server reads the cookie, finds the cart count, and that part is **streamed** in afterwards.
* Analogy: printed menu (static), today's special on the whiteboard (cached, changes once a day), "is a table free right now?" (dynamic, ask the kitchen every time).

### 2. Simple Definitions
* **Static:** HTML built once, everyone gets the same.
* **Dynamic:** built on every request (depends on the user or on time).
* **Streaming:** send the ready parts first, the rest later.
* **Cache:** remember an old result instead of rebuilding it.
* **Suspense:** "this part isn't ready yet, show this fallback meanwhile."

### 3. The Essentials (Next.js 16, Cache Components)
1. Next.js prerenders everything it can at build time. Anything that cannot be known at build time must sit inside `<Suspense>`.
2. These make a part dynamic: `cookies()`, `headers()`, `searchParams`, uncached `fetch`, DB queries, `Math.random()`, `Date.now()`.
3. **`fetch` is NOT cached by default in Next.js 16.** Old tutorials (Next 13/14) say it is. That is the old model.
4. **Cache on purpose with `"use cache"`:** `cacheLife("hours")` sets how long the data stays valid; `cacheTag("products")` names it so it can be refreshed later. Needs `cacheComponents: true` (`create-next-app` turns it on by default; confirmed in the roadmap).
5. The same `fetch` called twice in one render runs once (deduplicated). For DB/ORM calls use `React.cache`.
6. **Parallel fetching:** independent data goes in `Promise.all`. Sequential `await`s create a waterfall (2 x 1 sec = 2 sec instead of 1 sec).
7. Cache key = the function's arguments. Never put one user's private data in a shared `use cache` function; pass the user id as an argument, or use `use cache: private`.

### 4. Code Example
```tsx
// lib/products.ts
import { cacheLife, cacheTag } from "next/cache";

export async function getProducts() {
  "use cache";
  cacheLife("hours");          // same data for 1 hour
  cacheTag("products");        // refresh later using this name
  const res = await fetch("https://dummyjson.com/products?limit=20");
  if (!res.ok) throw new Error("Failed to load products");
  return res.json();
}
```
```tsx
// app/products/page.tsx
export default async function ProductsPage() {
  const { products } = await getProducts();        // cached, part of the static shell
  return (
    <>
      <h1>Products</h1>                             {/* static */}
      <ProductList products={products} />           {/* cached 1 hour */}
      <Suspense fallback={<p>Loading cart...</p>}>
        <CartCount />                                {/* dynamic: reads cookies() */}
      </Suspense>
    </>
  );
}

// Waterfall (slow) vs parallel (fast)
const products = await getProducts();
const categories = await getCategories();                         // waits for the first one
const [p, c] = await Promise.all([getProducts(), getCategories()]); // both together
```

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Assuming `fetch` is cached because a 2023 article said so | Next.js 16 default is uncached |
| `cookies()` or a DB query outside `<Suspense>` | Blocking route: build error/warning |
| User's private data inside a shared `use cache` function | One user's data can leak to another |
| Sequential `await`s for independent data | Waterfall; page is slower than needed |
| Making the whole page dynamic | Loses the static shell benefit |
| Old config (`export const dynamic`, `revalidate`) with Cache Components on | Errors; replaced by `use cache` + `cacheLife` |

> Cache Components is new. Turning it on in an existing app can surface new build errors (uncached data outside Suspense). Docs win if they disagree.

### 6. Practice Checks (passed)
* **R1** (Static / Cached / Dynamic): footer = static; blog list updated twice a day = cached; "Welcome back, Asha" = answered "Welcome back is static, Asha is dynamic", which is the more precise answer (the text is in the shell, the name streams in from the cookie); live stock count = dynamic. No one-line reasons were written (they were asked for); not a problem here but worth giving next time.
* **R2** (two sequential `await`s = 2 sec): correctly named it a waterfall and said both calls are independent so they should run in parallel. Did not write the `Promise.all` code, but the concept is right.

### 7. Optional / Later (not needed now)
* `use cache: private` and `use cache: remote`; `unstable_cache` (still works).
* `revalidateTag` vs `updateTag` (comes with Server Actions in Topic 4).
* Partial Prerendering internals, migrating an old app to Cache Components.

---

# Topic 4: Server Actions, Forms & Mutations

### 1. Real-Time Example: "Add new order" in the admin dashboard
```text
 ADMIN (browser)                               SERVER (Next.js)
 1. Opens /orders: sees 5 orders (cached, tag "orders")
 2. Fills the form: "Pen", qty 3
 3. Clicks Save  ─────────────────────────▶  4. createOrder() runs on the server:
    (Next.js sends the POST itself)             a. Who is logged in? Is it an admin?
                                                b. Is the data valid? (Zod)
                                                c. Save to the database
                                                d. updateTag("orders"): expire the cached list
                                                e. redirect("/orders")
 6. Page shows 6 orders  ◀──────────────────  5. Fresh list comes back
```
* Analogy: the form is an **order slip** going from the table to the kitchen counter. The counter must check who sent it and whether they may order that, before cooking.
* No separate `/api/orders` route, no hand-written `fetch`, no manual loading state: Next.js does the plumbing.

### 2. Simple Definitions
* **Server Function:** async function that runs on the server and is called from the client over the network (always POST).
* **Server Action:** a Server Function used as a form `action` or for a mutation.
* **Mutation:** changing data (add, edit, delete), as opposed to reading it.
* **`"use server"`:** marker saying the function runs only on the server.

### 3. The Essentials
1. `"use server"` at the top of a function or a file. Inline functions only inside Server Components; a Client Component must import the action from a `"use server"` file.
2. Form flow: `<form action={createOrder}>` receives `FormData`. On the server do **auth check, validate (Zod), save, refresh**.
3. **Security: a Server Action is a public POST endpoint.** Hiding the button is not protection. Inside every action check: authentication (is someone logged in?), authorization (may this user do this, and does this user own THIS record?), and validate all input.
4. Refreshing the cache after a mutation:
   * `updateTag("orders")`: Server Actions only; the user sees fresh data immediately (read-your-own-writes). Use when the user just changed the data themselves.
   * `revalidateTag("orders", "max")`: stale-while-revalidate; old data may show once, then updates in the background. The 2nd argument is now required. Use when slightly old data is fine.
   * `revalidatePath("/orders")`: refresh a whole route.
5. **Revalidate first, `redirect` last.** `redirect()` throws, so code after it never runs.
6. UI: `useActionState(action, initial)` gives `[state, formAction, pending]` for validation errors and "Saving..."; `useOptimistic` for instant feedback (Phase 4 Topic 8).
7. Don't use Server Actions to read data (the client runs them one at a time). Reads belong in Server Components.

### 4. Code Example
```ts
// app/orders/actions.ts
"use server";
import { z } from "zod";
import { updateTag } from "next/cache";
import { redirect } from "next/navigation";
import { requireRole } from "@/lib/dal";

const Schema = z.object({
  name: z.string().min(2),
  qty: z.coerce.number().int().min(1),     // form values are always strings
});

export async function createOrder(prev: unknown, formData: FormData) {
  await requireRole("admin");                                      // auth inside the function
  const parsed = Schema.safeParse(Object.fromEntries(formData));  // validate
  if (!parsed.success) return { errors: parsed.error.flatten().fieldErrors };
  await db.orders.create(parsed.data);                             // save
  updateTag("orders");                                             // refresh first
  redirect("/orders");                                             // redirect last
}
```
```tsx
// app/orders/OrderForm.tsx
"use client";
import { useActionState } from "react";
import { createOrder } from "./actions";

export function OrderForm() {
  const [state, formAction, pending] = useActionState(createOrder, null);
  return (
    <form action={formAction}>
      <input name="name" />
      <input name="qty" type="number" />
      {state?.errors?.qty && <p>{state.errors.qty[0]}</p>}
      <button disabled={pending}>{pending ? "Saving..." : "Save"}</button>
    </form>
  );
}
```
`createOrder` takes `(prev, formData)` because `useActionState` passes the previous state as the first argument.

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Hiding the button and assuming the action is safe | The action is a public endpoint; anyone can POST to it directly |
| Using a client-sent `id` without checking ownership | IDOR: one user deletes another user's order |
| Trusting only frontend validation | Frontend checks can be removed in DevTools |
| Forgetting `updateTag`/`revalidate` | Data saved, but the list looks stale |
| `revalidatePath` after `redirect` | `redirect` throws; it never runs |
| Returning raw error objects | Leaks internal details |
| Inline `"use server"` in a Client Component | Only Server Components can define inline actions |

### 6. Practice Checks (passed)
* **S1:** (a) own new order must show immediately = `updateTag`; (b) slightly old view count is fine = `revalidateTag("x", "max")`. Both correct. **No one-line reasons written** (this is the second time; practise giving a "why", interviews ask for it).
* **S2** (bug-hunt on `deleteOrder`): found 3 of 4: missing login check, missing permission check, and `revalidatePath` must come before `redirect`. **Missed:** the `id` from `formData.get("id")` is unvalidated input (it can be `null`, a `File`, or someone else's id). Fix: validate with Zod, and check that this order belongs to this user.
* Vocabulary to use in interviews: "is logged in?" = **authentication**; "is allowed to do this / owns this record?" = **authorization**.
```ts
"use server";
export async function deleteOrder(formData: FormData) {
  const user = await requireUser();                                  // authentication
  const { id } = z.object({ id: z.string().uuid() }).parse(Object.fromEntries(formData)); // validate
  const order = await db.orders.findById(id);
  if (!order || order.ownerId !== user.id) throw new Error("Not allowed");   // authorization
  await db.orders.delete(id);
  updateTag("orders");
  redirect("/orders");
}
```

### 7. Optional / Later (not needed now)
* Progressive enhancement (Server Component forms work before JS loads).
* `refresh()`, `useFormStatus` for nested submit buttons, file uploads.
* Passing Server Actions as props.

---

# Topic 5: Route Handlers & When to Use a Separate Backend

### 1. Real-Time Example: Razorpay tells your server "payment done"
```text
 CUSTOMER           RAZORPAY (another company's server)      YOUR SERVER (Next.js)
 1. Clicks Pay on /checkout
 2. Pays on Razorpay's page ──▶ 3. Payment succeeds
                                4. Razorpay calls your URL:
                                   POST myshop.com/api/webhooks/razorpay  ──▶  5. route.ts runs:
                                   (JSON body + signature header)                 a. Is the signature genuine?
                                                                                  b. Mark the order "paid" in the DB
                                                                                  c. revalidateTag("orders", "max")
                                6. Razorpay gets 200 OK  ◀────────────────────  quick 200 response
 7. Admin dashboard shows "Paid"
```
* Why not a Server Action? A Server Action is for **your own app's forms**; Next.js generates its address internally. An outsider needs a **plain, fixed URL**.
* Analogy: Server Action = intercom inside the house (only your own form uses it). Route Handler = gate with an address (Razorpay, a mobile app or any server can come); so the gate needs a **guard**.

### 2. Simple Definitions
* **Route Handler:** a `route.ts` file exporting `GET`, `POST`, `PUT`, `PATCH`, `DELETE` functions using the standard web `Request`/`Response`.
* **Webhook:** another service calls your URL with a POST saying "something happened".
* **Idempotent:** doing the same thing once or five times gives the same result. Lift button = idempotent; "one more tea" = not.
* **Signature:** a stamp made with a shared secret; proves the message came from the real sender.

### 3. The Essentials
1. The folder makes the URL (`app/api/orders/route.ts` is `/api/orders`). `page.tsx` and `route.ts` cannot live in the same folder.
2. **Use a Route Handler for:** webhooks (Stripe, Razorpay), endpoints for non-React clients (mobile app), file download/streaming, OAuth callbacks, a proxy that hides a third-party API key.
3. **Do NOT use one for:** data for your own Server Components (call the function directly) or your own form mutations (Server Action).
4. **Treat every handler as a public API:** authenticate, authorize, validate input, return correct status codes (200, 201, 400, 401, 403, 404, 500).
5. **Webhook rules:** (1) verify the **signature first** (webhooks have no logged-in user or cookie, so a "user check" is the wrong tool); (2) return 200 quickly (slow = provider retries); (3) keep the handler **idempotent** (events can arrive twice).
6. `updateTag` works only in Server Actions. In a Route Handler use `revalidateTag("orders", "max")`.
7. `params` in dynamic route handlers is also a Promise: `await` it.

### 4. Code Example
```ts
// app/api/webhooks/razorpay/route.ts
import crypto from "node:crypto";
import { revalidateTag } from "next/cache";

export async function POST(req: Request) {
  const body = await req.text();                              // signature is made on the raw text
  const signature = req.headers.get("x-razorpay-signature");
  const expected = crypto
    .createHmac("sha256", process.env.RAZORPAY_WEBHOOK_SECRET!)   // secret in .env, never NEXT_PUBLIC_
    .update(body)
    .digest("hex");

  if (!signature || signature !== expected) {
    return new Response("Invalid signature", { status: 401 });    // guard first
  }

  const event = JSON.parse(body);
  if (event.event === "payment.captured") {
    await markOrderPaid(event.payload.payment.entity.order_id);   // must be idempotent
    revalidateTag("orders", "max");
  }
  return Response.json({ ok: true });                             // quick 200
}
```
> Razorpay's exact header/field names are from memory here; check their docs in a real project. In production compare signatures with `crypto.timingSafeEqual`.

### 5. When to Use What
| Situation | Use |
|---|---|
| Add/edit/delete from your own page | **Server Action** |
| Show data on your own page | **Server Component** calling the function directly |
| Razorpay/Stripe webhook | **Route Handler** |
| Mobile app needs an API | **Route Handler** (or a separate backend) |
| File download / stream | **Route Handler** |
| Hide a third-party API key | **Route Handler** proxy (or call it from a Server Component) |

**Read vs write rule:** a Server Component function call runs **while the page renders** and is for **reading**. A Server Action runs **when the user does something** (click, submit) and is for **changing** data. Putting a delete inside a Server Component would delete on page open or refresh.

### 6. Separate Backend? (my judgement, not from the roadmap; the roadmap only points to Phase 6)
* **Next.js alone is enough:** one web app, mostly CRUD, small team. Project 1 is like this.
* **Consider Express/FastAPI when:** web + mobile + partners share one API; long-running work (jobs, queues, cron, big AI pipelines; serverless has time limits); Python work (RAG, LangGraph, so the AI projects use FastAPI); separate team or scaling needs.
* Then Next.js just talks to that backend like any other frontend (Projects 2 and 4).

### 7. Common Mistakes
| Mistake | Why it fails |
|---|---|
| No signature check on a webhook | Anyone can fake "payment done" |
| Fetching your own `/api/...` from your own Server Component | Pointless network hop; call the function |
| No auth on a Route Handler | It is a public API |
| Slow webhook handler | Provider times out and retries |
| Non-idempotent webhook (`balance + 500`) | A retry applies it twice |
| Secret in `NEXT_PUBLIC_` | Visible to every visitor |
| Returning 200 even on errors | The caller never knows it failed |

### 8. Practice Checks (passed)
* **T1:** (b) page list = Server Component call, (c) Android app = Route Handler, (d) Razorpay = Route Handler, all correct. **(a) "Delete order" was first answered "Server Component call" (wrong)**; after the read-vs-write explanation: Server Action. **No one-line reasons written** (third time in a row: Topics 3, 4, 5).
* **T2** (fake webhook): "the POST will succeed" is right; the order would be marked paid with no payment. Idea "check who sent it and from where" is right, but a webhook has no logged-in user: the check is the **signature** (HMAC with the shared secret). Right idea, wrong word ("user check"); the concept was correct.
* Doubts asked and explained: Server Component call vs Server Action (read vs write, render time vs click time); idempotent (`status = "paid"` is safe on a retry, `balance + 500` is not; for "add" style work store the event id and skip repeats).

### 9. Optional / Later (not needed now)
* Caching a `GET` handler: call a `use cache` helper inside it (the directive can't go on the `GET` export).
* CSRF when a POST handler uses cookie auth (Phase 14); streaming responses; CORS headers.

---
