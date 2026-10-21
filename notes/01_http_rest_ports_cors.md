# 01 — HTTP, REST, Ports & CORS Cheat Sheet

> **Quick Summary:** Core mental models for browser-to-server communication, request lifecycles, and cross-origin security.

---

## 1. HTTP Request & Response Anatomy

### The Wire Lifecycle
1. **DNS Lookup:** Domain (`api.site.com`) $\rightarrow$ IP address (`93.184.216.34`).
2. **TCP 3-Way Handshake:** `SYN` $\rightarrow$ `SYN-ACK` $\rightarrow$ `ACK` (establishes port connection).
3. **TLS Handshake:** Secure key exchange for HTTPS encryption.
4. **HTTP Exchange:** Request travels $\rightarrow$ Server processes $\rightarrow$ Response returns.

### Request vs Response Format
```http
-- REQUEST --
POST /orders HTTP/1.1
Host: api.site.com
Content-Type: application/json
Authorization: Bearer <token>

{"item": "book", "qty": 1}

-- RESPONSE --
HTTP/1.1 201 Created
Content-Type: application/json

{"orderId": 42, "status": "confirmed"}
```

---

## 2. HTTP Status Codes Cheat Sheet

| Code | Name | Meaning & Use Case |
|---|---|---|
| **200** | OK | Standard success for `GET`, `PUT`, `PATCH`. |
| **201** | Created | Standard success for `POST` (new record made). |
| **204** | No Content | Standard success for `DELETE` (no body returned). |
| **301** | Moved Permanently | Permanent URL redirect (SEO cached). |
| **304** | Not Modified | Cached copy is valid (0 bytes downloaded). |
| **400** | Bad Request | Syntax error, malformed JSON body. |
| **401** | Unauthorized | **"Who are you?"** Missing/invalid token or session. |
| **403** | Forbidden | **"I know who you are, but you lack permission."** |
| **404** | Not Found | Resource or endpoint URL does not exist. |
| **422** | Unprocessable Entity | Valid JSON, but validation failed (e.g. `age < 0`). |
| **500** | Internal Server Error | Unhandled crash/exception in backend code. |
| **502** | Bad Gateway | **Reverse Proxy** (Nginx/Cloudflare) reached a dead backend. |
| **503** | Service Unavailable | Backend server overloaded or restarting. |
| **504** | Gateway Timeout | Upstream database or external API took too long. |

---

## 3. REST Architecture Rules

* **Rule 1: URLs are NOUNS (resources):**
  * ❌ `/getOrders`, `/createOrder`, `/deleteOrder/12`
  * ✅ `/orders`, `/orders/12`
* **Rule 2: HTTP Methods are VERBS (actions):**
  * `GET` $\rightarrow$ Read
  * `POST` $\rightarrow$ Create
  * `PUT` $\rightarrow$ Complete replacement (wipes missing fields)
  * `PATCH` $\rightarrow$ Partial update (modifies only sent fields)
  * `DELETE` $\rightarrow$ Remove

### Safety & Idempotency Table
* **Safe:** Does NOT modify server data (read-only).
* **Idempotent:** Running it 1 time has the exact same effect as running it 100 times.

| Method | Safe? | Idempotent? | Explanation |
|---|---|---|---|
| **`GET`** | **YES** | **YES** | Read-only; repeats change nothing. |
| **`PUT`** | **NO** | **YES** | Replaces record; repeating with same data leaves same state. |
| **`PATCH`** | **NO** | **Usually NO** | e.g. `{ increment: 1 }` changes value on every call. |
| **`DELETE`** | **NO** | **YES** | Deleting item #42 repeatedly leaves it deleted. |
| **`POST`** | **NO** | **NO** | Running 5 times creates 5 separate records / charges 5 times. |

---

## 4. Common Network Ports

* **`80`**: Standard HTTP (unencrypted)
* **`443`**: Standard HTTPS (encrypted)
* **`3000` / `5173`**: Common local frontend/Node dev servers (Next.js, Vite)
* **`5432`**: PostgreSQL Database
* **`27017`**: MongoDB Database
* **`EADDRINUSE` Error:** Occurs when two apps attempt to listen on the exact same port on the same IP. Only one process can bind to a port at a time.

---

## 5. CORS (Cross-Origin Resource Sharing)

### The Core Truth
* **CORS does NOT have an HTTP status code.**
* Handled entirely by the **browser security engine**, not the server.
* In JavaScript: throws `TypeError: Failed to fetch`.
* In Network tab: status may show `(failed)` or even `200 OK` (because server responded, but browser hid data from JS!).

### Origin Definition
Two URLs share an origin ONLY if **Protocol + Domain + Port** match:
* `http://localhost:3000` vs `http://localhost:5000` $\rightarrow$ **CORS Error** (Different port).
* `http://site.com` vs `https://site.com` $\rightarrow$ **CORS Error** (Different protocol).
* `https://site.com` vs `https://api.site.com` $\rightarrow$ **CORS Error** (Different subdomain).

### Preflight (`OPTIONS`)
* Sent automatically before non-simple requests (`PUT`, `DELETE`, custom headers, `application/json`).
* If preflight fails (`404` or `405`), the real request is never sent.

### How to Fix
1. **Backend:** Add CORS headers (`Access-Control-Allow-Origin: http://localhost:3000`).
2. **Frontend Proxy:** Proxy via Next.js rewrites or Vite proxy (Server-to-server calls do NOT have CORS).

---

## 6. Top Production & Interview Traps

1. **`fetch()` only rejects on network loss:** A `404` or `500` resolves normally. Always check `if (!res.ok)`.
2. **Double stream read:** Calling `res.json()` and then `res.text()` throws `TypeError: Body has already been consumed`.
3. **Missing `Content-Type: application/json`:** Backend will receive an empty `req.body: {}`.
4. **Who sends 502:** The reverse proxy (Nginx, Vercel proxy, Cloudflare) sends it when the Node app behind it is dead or unreachable.
5. **CORS does NOT protect servers:** Postman, curl, and backend servers ignore CORS completely. CORS only protects the user in their browser from cross-site data theft.
