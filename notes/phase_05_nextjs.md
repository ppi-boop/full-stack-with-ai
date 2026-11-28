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

# Topic 6: Authentication & Protected Pages

> Teaching note: the first, many-terms version of this lesson did not land ("nothing understood"). The version that worked was ONE idea at a time with a single analogy (water-park wristband), no code at first, then small checks.

### 1. Real-Time Example: why a cookie exists
HTTP has no memory. The server treats every request as a brand-new visitor.
```text
Request 1: POST /login (email + password)
   Server -> "Correct!"  + response header:  Set-Cookie: session=<token>
   The browser saves the cookie.

Request 2: GET /orders
   The browser sends it by itself:  Cookie: session=<token>   (on EVERY request to that site)
   Server checks the token -> "this is an admin, stamp is genuine" -> returns the orders.
```
You can see `Set-Cookie` (response header) and `Cookie` (request header) in the Network tab.

* Analogy: **water-park wristband.** Show your ID at the gate once (login) and get a band (cookie). At each ride only the band is checked. The band carries a **stamp (signature)** that only the park can make, so a fake band fails the check. A "VIP" mark on the band decides which rides you may enter (role).

### 2. Simple Definitions
| Word | Meaning | Water park |
|---|---|---|
| **Cookie** | small piece of data the browser saves and sends with every request | wristband |
| **Authentication** | proving who you are | showing ID at the gate |
| **Authorization** | what you are allowed to do / which records are yours | VIP ride permission |
| **Session** | the server remembering you across requests (here: a signed token in a cookie) | the band itself |
| **Signature** | a stamp made with a secret only the server has (`SESSION_SECRET` in `.env`) | the park's stamp |
| **DAL** | one server-only module that does the real auth check and all data reads | ride operator next to the ride |
| **DTO** | the small object you send out instead of a full DB row | |

### 3. The Essentials
1. Three separate jobs: **authentication** (who), **session management** (remember), **authorization** (allowed?).
2. In real projects use a maintained library (Auth.js, Better Auth, Clerk, Supabase). Build it by hand once to learn. Password hashing, refresh tokens, RBAC come in Phase 6.
3. **Session cookie flags:** `HttpOnly` (JavaScript cannot read it, so an XSS script cannot steal it), `Secure` (HTTPS only), `SameSite=Lax` (helps against CSRF). Set the cookie on the server. Sign the token with `jose`; secret in an env var; no personal info (PII) inside the token.
4. **Why not `localStorage` for the token?** Any JavaScript running on the page (an XSS comment-box `<script>`, a compromised npm package) can do `localStorage.getItem("token")` and send it to a hacker. An `HttpOnly` cookie cannot be read by JavaScript at all.
5. **DAL:** `lib/dal.ts` (`import "server-only"`) with `verifySession()` wrapped in `React.cache` (runs once per request). **Every data read, every Server Action and every Route Handler calls it.**
6. **DTO:** never send a whole DB row (it can contain `passwordHash`); a Client Component's props travel to the browser (Topic 2). Return only the fields the UI needs.
7. **`proxy.ts`** (was `middleware.ts`) is only an **optimistic gate guard**: "is there a cookie?" No DB calls, because it runs on every route and prefetch. A fake cookie passes it. It is **never** the only protection, and its `matcher` can miss routes (the example matcher even skips `/api`).
8. **Real check goes next to the data**, not in a layout (Topic 1: layouts don't re-run on each navigation). Rule: wherever data comes out (page, Server Action, Route Handler) call `verifySession()` there.
9. Under Cache Components the session is runtime data (`cookies()`), which has its own guide; not needed yet.

### 4. Code Example
```ts
// proxy.ts  (Next.js 16; was middleware.ts)  --  OPTIMISTIC check only
import { NextResponse, type NextRequest } from "next/server";

export function proxy(req: NextRequest) {
  const hasSession = req.cookies.has("session");
  if (!hasSession && req.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", req.url));
  }
}
export const config = { matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"] };
```
```ts
// lib/dal.ts  (simplified): the REAL check
import "server-only";
import { cache } from "react";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { jwtVerify } from "jose";

const secret = new TextEncoder().encode(process.env.SESSION_SECRET);

export const verifySession = cache(async () => {
  const token = (await cookies()).get("session")?.value;   // Next 16: await cookies()
  if (!token) redirect("/login");
  try {
    const { payload } = await jwtVerify(token, secret);    // signature + expiry
    return { userId: payload.userId as string, role: payload.role as string };
  } catch {
    redirect("/login");                                     // fake or expired token
  }
});

export async function requireRole(role: string) {
  const session = await verifySession();
  if (session.role !== role) redirect("/forbidden");
  return session;
}

// DTO: only the fields the UI needs
export async function getUserCard(id: string) {
  await verifySession();
  const user = await db.users.findById(id);        // full row stays on the server
  return { id: user.id, name: user.name };
}
```
```ts
// in the login Server Action: set the cookie on the server
(await cookies()).set("session", token, {
  httpOnly: true, secure: true, sameSite: "lax", maxAge: 60 * 60 * 24 * 7, path: "/",
});
```
```ts
// app/api/export/route.ts: the check lives INSIDE the handler (proxy does not cover /api here)
export async function GET() {
  const session = await verifySession();
  if (session.role !== "admin") return new Response("Forbidden", { status: 403 });
  const csv = await buildOrdersCsv();
  return new Response(csv, { headers: { "Content-Type": "text/csv" } });
}
```

### 5. Common Mistakes
| Mistake | Why it fails |
|---|---|
| "Protected" page that only redirects on the client | The data has already reached the browser |
| JWT in `localStorage` | XSS script can read and steal it |
| Role checked only in the UI (hidden button) | The action is a public endpoint; a hacker edits the page JS or calls it directly |
| Relying only on `proxy.ts` | It only checks that a cookie exists; a fake cookie passes |
| Extending the proxy `matcher` instead of adding a check in the handler | Still only an optimistic check; the next new route can be missed |
| DB call inside `proxy.ts` | Runs on every route and prefetch, so the site gets slow |
| Sending a whole DB row to the client | `passwordHash` etc. leak |
| Auth check only in `layout.tsx` | Layouts do not re-run on every navigation |
| Cookie without `HttpOnly` | JavaScript can read it |

### 6. Practice Checks (passed)
* **Wristband checks:** "How does the server know request 2 is the same person?" = the browser sends the cookie with each request. Fake cookie = the server checks the stamp against its secret and rejects it. Both correct. Refinement: the cookie goes on every request, not only API calls.
* **Matcher trap** (`/api/export` not covered by the proxy): correctly said anyone can open it. His fix was to make the proxy cover the route (change the matcher or move the folder). That is only the guard again, and a fake cookie still passes. **Correct fix:** `verifySession()` and a role check inside the Route Handler.
* **XSS question:** token in `localStorage` gets stolen; an `HttpOnly` cookie does not. Correct.
* **Final answer** (token in `localStorage` + button hidden only in the UI): problem 1 = a hacker can read `localStorage`, fix = `HttpOnly` cookie. Problem 2 = a hacker can remove the UI condition in browser JS. **Fix not stated:** check the role on the server, inside the Server Action / Route Handler (hiding a button is UX, not security). DTO: "only the data the frontend uses" = correct; add: sensitive fields like `passwordHash` never leave the server.
* First time one-line reasons appeared in the answers; keep doing it.
* Interview answers ready: "Why isn't proxy.ts enough?" (only checks cookie presence, not validity; matcher can miss routes; Actions/Handlers need their own checks). "Why HttpOnly cookies, not localStorage?" (JS cannot read them, so XSS cannot steal them). "DAL and DTO?" (see definitions).

### 7. Optional / Later (not needed now)
* Password hashing (bcrypt/argon2), refresh tokens, OAuth / social login, rate limiting (Phases 6 and 14).
* "Authentication with Cache Components" guide; database sessions (cookie holds only an encrypted session id).
* `SameSite` and CSRF in detail (Phase 14).

---

# Topic 7: Error Handling, not-found, Env Variables, Metadata/SEO & Image Optimization (quick)

### 1. Real-Time Example: five scenes on `myshop.com/products/42`
**Scene 1: something breaks (error).** The DB is down while the page runs.
* Without handling the page breaks. With `app/products/error.tsx` the same spot shows a friendly message and a "Try again" button.
```tsx
"use client";                                   // error.tsx is always a Client Component
export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (<div><p>Something went wrong. Please try again.</p><button onClick={() => reset()}>Try again</button></div>);
}
```
* It is the Next.js version of a React error boundary (Phase 4). `reset()` retries the segment. `global-error.tsx` handles root-layout errors.
* **Expected errors** (validation, "email already taken") are **returned as state** from a Server Action (`useActionState`, Topic 4), not thrown. **Unexpected errors** (DB down, bug) are thrown and caught by `error.tsx`. Never show raw error messages to users; log details on the server.

**Scene 2: product does not exist (not-found).** `/products/99999`:
```tsx
const product = await getProduct(id);
if (!product) notFound();            // renders not-found.tsx with HTTP status 404
```

**Scene 3: where do secrets live (env variables).**
```text
.env.local        real secrets; never commit it
.env.example      names only, no values; documentation for other developers
DATABASE_URL=...            # server only
STRIPE_SECRET_KEY=...       # server only
NEXT_PUBLIC_SITE_NAME=...   # also shipped to the browser (public things only)
```
* Only names starting with `NEXT_PUBLIC_` are inlined into the browser bundle, **at build time**. So changing one needs a rebuild (interview question). Never put `NEXT_PUBLIC_` on a secret.
* Validate env with Zod at startup so the app fails fast if one is missing.

**Scene 4: how the link looks on WhatsApp/Google (metadata).**
```tsx
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);
  if (!product) return { title: "Product not found" };
  return { title: `${product.name} | MyShop`, description: product.description };
}
```
* Fixed title: `export const metadata = { title: "About", description: "..." }`. Per-page title lives in `page.tsx` or `layout.tsx` (interview question).

**Scene 5: the product photo (image).**
```tsx
import Image from "next/image";
<Image src={product.imageUrl} alt={product.name} width={600} height={400} priority />
```
```ts
// next.config.ts: remote images must be allowed
images: { remotePatterns: [{ protocol: "https", hostname: "cdn.myshop.com" }] }
```
* `next/image` resizes for the screen, serves modern formats, lazy-loads, and with `width`/`height` reserves the space so the page does not jump (CLS, Phase 3 Topic 11). Use `priority` on the top image (LCP). Always write `alt`.

### 2. Common Mistakes
| Mistake | Why it fails |
|---|---|
| Throwing an expected error (email taken) | The user gets an error screen, not a friendly form message |
| Showing `error.message` in `error.tsx` | Can leak internal details |
| `NEXT_PUBLIC_` on a secret | Every visitor can see it |
| Committing `.env.local` | Secret becomes public |
| `<img>` without `width`/`height` | Layout shift (CLS) and no optimization |
| Missing `alt` | Hurts accessibility and SEO |
| Remote image without `remotePatterns` | Next.js refuses to load it |
| Blank page instead of `notFound()` | Google sees a normal page, not a 404 |

### 3. Practice Checks (passed)
* **V1:** (a) email already taken = return as state; (b) product not in DB = `notFound()`; (c) DB down = `error.tsx` (throw). All correct. No one-line reasons this time.
* **V2** (`NEXT_PUBLIC_STRIPE_SECRET_KEY` and `<img>` without sizes):
  * Env: correct. `NEXT_PUBLIC_` ships the key to the browser at build time so a hacker can read it; remove the prefix; do not push `.env.local`. **Add:** if that key was ever built or deployed, it is already exposed, so **rotate it** (revoke and create a new key). Renaming alone is not enough. The correct name is `STRIPE_SECRET_KEY`.
  * Image: **partial.** He noticed the missing `width`/`height`, but the problem is not "moves with the screen". Without sizes the browser does not know the image size until it downloads, so the space is not reserved and the content below **jumps** when it loads (layout shift, CLS). A plain `<img>` also gets no resizing or lazy loading. **Fix:** use `next/image` with `width`/`height` (or `fill`) and `alt`.

### 4. Optional / Later (not needed now)
* `global-error.tsx`, `catchError` (Cache Components).
* `await connection()` to read an env value at request time instead of build time.
* Sitemap, `robots.txt`, `opengraph-image`, `next/font`, Next.js 16 image default changes (`minimumCacheTTL`, `qualities`, `localPatterns`).

---
