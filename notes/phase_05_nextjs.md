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
