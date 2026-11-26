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
