## 1. Web and HTTP

### DNS, networking and infrastructure

**Q: Which DNS record types should you know?**
A: `A` maps a name to an IPv4 address, `AAAA` to IPv6, `CNAME` makes one name an alias of another, `MX` lists mail servers, `TXT` holds free text (domain verification, SPF) and `NS` names the authoritative name servers.

**Q: What is DNS TTL and why does it matter when you move a site?**
A: TTL tells resolvers how long they may cache a record. A long TTL means a change spreads slowly, so lower it a day or two before a planned migration.

**Q: TCP vs UDP?**
A: TCP is connection-based and gives reliable, ordered delivery. UDP sends independent packets with no guarantees but low overhead, so it suits DNS lookups, video calls and games.

**Q: What happens in a TLS handshake, in simple words?**
A: Client and server agree on a protocol version and cipher, the server proves its identity with a certificate, and both derive shared secret keys. After that, all data is encrypted with those fast symmetric keys.

**Q: What is a CDN and why use one?**
A: A network of edge servers near users that cache static files (and sometimes dynamic responses). It cuts latency, lowers load on your origin server and helps absorb traffic spikes.

**Q: Forward proxy vs reverse proxy?**
A: A forward proxy sits in front of clients and makes requests on their behalf (a corporate proxy). A reverse proxy sits in front of servers (Nginx, Cloudflare) and handles TLS, caching, compression and load balancing.

**Q: What does a load balancer do, and what are L4 vs L7?**
A: It spreads requests across several servers and stops sending traffic to unhealthy ones using health checks. L4 balances on IP and port (TCP), while L7 understands HTTP, so it can route by host, path or header.

**Q: What is HTTP/3?**
A: HTTP running over QUIC, which uses UDP. It avoids TCP head-of-line blocking, sets up connections faster and survives network changes better (for example Wi-Fi to mobile data).

### HTTP messages, methods and status codes

**Q: What are the parts of an HTTP request and response?**
A: A request has a request line (method, path, version), headers and an optional body. A response has a status line (code and reason), headers and a body.

**Q: 301 vs 302 vs 307 vs 308?**
A: 301 and 308 are permanent redirects, 302 and 307 are temporary. 307 and 308 force the client to repeat the same method and body, while old 301/302 handling may turn a POST into a GET.

**Q: 502 vs 503 vs 504?**
A: 502 means a gateway or proxy got an invalid response from the upstream server, 503 means the service is unavailable (overloaded or in maintenance), and 504 means the upstream did not answer in time.

**Q: 400 vs 422 for bad input?**
A: 400 usually means the request is malformed (broken JSON). 422 means it was well-formed but failed validation rules. Many APIs use only one, so be consistent and document it.

**Q: `Content-Type` vs `Accept`?**
A: `Content-Type` says what format the body you are sending is in. `Accept` says which formats the client is willing to receive back.

**Q: Which body formats can a form or API send?**
A: `application/json` for APIs, `application/x-www-form-urlencoded` for simple HTML forms, and `multipart/form-data` for file uploads.

**Q: Safe vs idempotent HTTP methods?**
A: Safe methods (GET, HEAD, OPTIONS) don't change server state. Idempotent methods (those plus PUT and DELETE) can be repeated with the same end result. Every safe method is idempotent, but not the other way round.

**Q: What are HEAD and OPTIONS for?**
A: HEAD is GET without the response body, useful to check existence or size. OPTIONS asks what a resource supports, and browsers use it for CORS preflight.

**Q: Why shouldn't you put secrets in the URL query string?**
A: URLs end up in browser history, server and proxy logs and the `Referer` header. Send tokens in the `Authorization` header or the request body instead.

**Q: What are gzip and Brotli (`Content-Encoding`)?**
A: The server compresses text responses (HTML, CSS, JS, JSON) and the browser decompresses them. It cuts transfer size a lot, and Brotli usually compresses better than gzip.

### Caching

**Q: How do you cache-bust static files safely?**
A: Put a content hash in the file name (`app.3f9a1c.js`) and serve it with a long `max-age` and `immutable`. Keep the HTML on a short cache or `no-cache` so it points to the new file names after a deploy.

**Q: What does `stale-while-revalidate` do?**
A: The cache serves an expired copy immediately and refreshes it in the background. Users get a fast response and the next request sees fresh data.

**Q: `Cache-Control: public` vs `private`?**
A: `public` lets shared caches such as a CDN store the response. `private` allows only the user's own browser cache, which is what you want for per-user data.

**Q: What does the `Vary` header do?**
A: It lists request headers (such as `Accept-Encoding`) that change the response, so caches keep a separate copy per value. A missing or wrong `Vary` can serve one user's variant to another.

### Cookies and auth flows

**Q: What do `SameSite=Strict`, `Lax` and `None` mean?**
A: `Strict` never sends the cookie on cross-site requests. `Lax` also sends it on top-level navigations such as clicking a link, and is the default in Chromium browsers when the attribute is missing. `None` always sends it and requires `Secure`.

**Q: What do the `HttpOnly` and `Secure` cookie flags do?**
A: `HttpOnly` hides the cookie from JavaScript, which limits token theft through XSS. `Secure` sends it only over HTTPS. Neither one stops CSRF on its own.

**Q: What is OAuth 2.0 in simple words?**
A: A way for a user to let an app access their data at another service without sharing their password. The app receives a limited access token, usually through the authorization code flow with PKCE.

**Q: OAuth vs OpenID Connect?**
A: OAuth 2.0 is about authorization (access tokens). OpenID Connect sits on top and adds authentication: an ID token that says who the user is, which is what "Sign in with Google" uses.

**Q: What is inside a JWT?**
A: Three Base64URL parts: header, payload (claims such as `sub` and `exp`) and signature. It is signed, not encrypted, so anyone can read the payload and you must not put secrets in it.

### CORS and browser security

**Q: What is a CORS preflight request?**
A: Before some cross-origin requests (non-simple methods, custom headers such as `Authorization`, or a JSON content type) the browser sends an `OPTIONS` request first. The server must answer with the allowed origin, methods and headers, or the real request is blocked.

**Q: Why can't you use `Access-Control-Allow-Origin: *` with cookies?**
A: For credentialed requests the browser requires a specific origin plus `Access-Control-Allow-Credentials: true`, and it rejects the wildcard. The client must also opt in, for example `credentials: "include"` in `fetch`.

**Q: What is the same-origin policy?**
A: An origin is scheme + host + port. A page can send requests to other origins, but its scripts cannot read the response unless the other server allows it through CORS.

**Q: Why does a request work in Postman but fail with a CORS error in the browser?**
A: CORS is enforced by browsers only. Postman and `curl` don't apply the same-origin policy, so the server must send the right CORS headers for browser clients.

**Q: What is HSTS?**
A: The `Strict-Transport-Security` header tells the browser to use only HTTPS for your domain for a set time. It prevents downgrade attacks and accidental plain-HTTP first requests.

**Q: What is a Content Security Policy (CSP)?**
A: A response header listing which sources may load scripts, styles, images and so on. It limits the damage of XSS by blocking inline or third-party scripts you did not approve.

### API design and real-time

**Q: What makes an API RESTful?**
A: Resources as nouns in URLs (`/orders/5`), standard HTTP methods and status codes, stateless requests and consistent representations (usually JSON). Few APIs follow every REST constraint, and that is fine.

**Q: What does stateless mean for an HTTP API?**
A: Each request carries everything the server needs (token, parameters), so no server instance keeps per-client memory between requests. That lets you add servers behind a load balancer.

**Q: How do you version an API?**
A: Common ways are a URL prefix (`/v1/orders`) or a header. The key rule is not to break existing clients, so add fields rather than rename or remove them.

**Q: What should an API return when it rate-limits a client?**
A: Status 429 Too Many Requests, usually with a `Retry-After` header, so the client knows when to try again.

**Q: What is a webhook and how do you receive one safely?**
A: A webhook is another service calling your URL when an event happens. Verify the signature, return a 2xx quickly, process the work in a queue and handle duplicates, because senders retry.

**Q: Polling vs long polling vs SSE vs WebSocket?**
A: Polling asks repeatedly (simple but wasteful). Long polling holds the request open until data arrives. SSE is a one-way server-to-browser stream over HTTP with auto-reconnect, and WebSocket is a two-way persistent connection.

**Q: Which would you use to stream LLM tokens to the browser?**
A: Usually SSE (or a streamed `fetch` response), because data flows one way and it works over plain HTTP. Use WebSocket when the client also sends frequent messages.

## 2. Git

### Everyday concepts

**Q: What is the staging area?**
A: A holding area (the index) where you choose exactly which changes go into the next commit. `git add` copies changes into it and `git commit` records them.

**Q: `git diff` vs `git diff --staged`?**
A: `git diff` shows unstaged changes. `git diff --staged` (or `--cached`) shows what is staged and will go into the next commit. `git diff main...feature` shows what the feature branch changed since it diverged from `main`.

**Q: What is `HEAD`, and what does `HEAD~2` mean?**
A: `HEAD` points to the commit (usually through a branch) that you currently have checked out. `HEAD~2` is the commit two steps back along the first parent.

**Q: What is the difference between `origin/main` and `main`?**
A: `main` is your local branch. `origin/main` is a remote-tracking branch: your local record of where `main` was on the remote at the last fetch.

**Q: Does Git store snapshots or diffs?**
A: Each commit points to a snapshot of the whole project (trees and blobs identified by hashes) and to its parent commit(s). A branch is just a movable pointer to a commit, which is why branching is cheap.

### Undoing changes

**Q: How do you discard local changes to a file, or unstage it?**
A: `git restore file` discards working-tree changes permanently, and `git restore --staged file` unstages it but keeps the edits. These replace older habits such as `git checkout -- file`.

**Q: `git reset --soft` vs `--mixed` vs `--hard`, and how do you undo the last commit?**
A: All three move the branch pointer. `--soft` keeps changes staged, `--mixed` (default) keeps them unstaged, and `--hard` also throws them away. `git reset --soft HEAD~1` undoes the last commit but keeps your work, for unpushed commits only.

**Q: How do you fix the last commit message or add a forgotten file?**
A: `git commit --amend` (stage the file first if needed). It replaces the last commit with a new one, so avoid it after pushing to a shared branch.

**Q: How can you recover a commit lost after a bad reset or a deleted branch?**
A: Run `git reflog` to see where `HEAD` recently pointed, find the commit hash, then recreate a branch with `git branch rescue <hash>`. Reflog entries expire eventually, so act soon.

**Q: What is a detached HEAD?**
A: `HEAD` points straight at a commit instead of a branch, for example after checking out a tag or a hash. Commits made there can be lost, so create a branch with `git switch -c name` to keep them.

**Q: How do you revert a merge commit?**
A: `git revert -m 1 <merge-hash>`. The `-m 1` tells Git which parent is the mainline to keep, usually the branch you merged into.

### Branching, merging and history

**Q: What is a fast-forward merge?**
A: When the target branch has no new commits, Git just moves its pointer forward and creates no merge commit. `git merge --no-ff` forces a merge commit anyway.

**Q: Merge commit vs squash merge vs rebase merge in a pull request?**
A: A merge commit keeps all commits plus a merge commit. Squash merge turns the whole PR into one commit on `main`, and rebase merge replays each commit on top with no merge commit. Teams pick one for a tidy history.

**Q: What does `git cherry-pick` do?**
A: It applies the changes of a specific commit from another branch as a new commit on your current branch. It is handy for hotfixes, but it duplicates the commit, so use it sparingly.

**Q: What is `git rebase -i` used for?**
A: Interactive rebase lets you squash, reorder, reword, edit or drop your own commits before sharing them. It rewrites those commits, so don't use it on commits others have already pulled.

**Q: What does `git pull --rebase` do?**
A: It fetches, then replays your local commits on top of the updated remote branch instead of creating a merge commit. The result is a straighter history.

**Q: How do you find which commit introduced a bug?**
A: Use `git bisect`. Mark one bad and one good commit, and Git binary-searches between them while you test each step. `git bisect run <script>` can automate it.

**Q: How do you see who changed a line, or when a string appeared?**
A: `git blame file` shows the last commit for each line, `git log -p -- file` shows the file's history, and `git log -S"text"` finds commits that added or removed that text.

**Q: What are Git tags used for?**
A: A tag marks a fixed commit, usually a release such as `v1.2.0`. Annotated tags (`git tag -a`) store a message, author and date, while lightweight tags are only a name.

### Collaboration and workflow

**Q: `--force` vs `--force-with-lease`?**
A: `--force` overwrites the remote branch no matter what. `--force-with-lease` refuses if someone else pushed since your last fetch, so you don't wipe their work.

**Q: You pushed a bad commit to a shared `main`. What do you do?**
A: Use `git revert` and push the new commit. Rewriting shared history with a force-push disrupts everyone, and protected branches usually block it anyway.

**Q: Why do merge conflicts happen and how do you reduce them?**
A: Two branches changed the same lines, or one deleted what the other edited. Keep branches short-lived, sync from `main` often and make small, focused PRs.

**Q: Git Flow vs trunk-based development?**
A: Git Flow uses long-lived `develop`, `release` and `hotfix` branches. Trunk-based development merges small changes into `main` often, protected by CI and feature flags, and suits teams that deploy continuously.

**Q: What are Conventional Commits?**
A: A message format such as `feat: add login` or `fix(api): handle null`. It keeps history readable and lets tools generate changelogs and version bumps.

**Q: What are Git hooks, and what is Husky?**
A: Hooks are scripts Git runs at certain events, such as `pre-commit` to lint or format staged files. Husky helps JavaScript projects share hooks through the repository.

**Q: How do you remove a leaked secret from Git history?**
A: Rotate the secret first, then rewrite history with `git filter-repo` (or BFG), force-push and ask everyone to re-clone. Rewriting does not undo the exposure, so rotation is still mandatory.

**Q: Fork vs clone vs branch?**
A: A clone copies a repo to your machine, a branch is a line of work inside a repo, and a fork is your own server-side copy of someone else's repo, used for open-source pull requests. Forks usually keep the original as an `upstream` remote.

## 3. JavaScript

### Scope, hoisting and the temporal dead zone

**Q: Output of `console.log(a); var a = 5;`?**
A: `undefined`. The `var` declaration is hoisted and initialised to `undefined`, but the assignment stays where it is.

**Q: Output of `console.log(b); let b = 5;`, and are `let`/`const` hoisted?**
A: `ReferenceError: Cannot access 'b' before initialization`. The binding is created at the top of the block (so it is hoisted), but it sits in the temporal dead zone until the declaration line runs.

**Q: Function declaration vs function expression: what is hoisted?**
A: A declaration (`function f() {}`) is hoisted with its body, so you can call it earlier. With `var f = function () {}` only `f` is hoisted as `undefined`, so an early call throws `TypeError: f is not a function`. With `let`/`const` you get a ReferenceError.

**Q: Output of `var x = 1; function f() { console.log(x); var x = 2; } f();`?**
A: `undefined`. The inner `var x` is hoisted to the top of `f` and shadows the outer `x`, but it has no value yet at the log.

**Q: What is lexical scope?**
A: Scope is decided by where code is written, not where it is called. An inner function can read the variables of the functions around it, and lookup goes outward through the scope chain up to the global scope.

**Q: What happens if you assign to an undeclared variable, e.g. `var a = b = 5;` in a function?**
A: Only `a` is declared. `b = 5` creates an implicit global in sloppy mode and throws a ReferenceError in strict mode and ES modules. Declare every variable explicitly.

**Q: What is an IIFE and why was it used?**
A: An immediately invoked function expression, `(function () { ... })()`, creates a private scope. It was the standard way to avoid globals before modules and block scope existed.

### Closures

**Q: Give practical uses of closures.**
A: Private state (counters, modules), function factories, memoization, `once`, partial application, and callbacks that remember data such as event handlers and timers.

**Q: Output of `for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0);` and how do you fix it?**
A: `3 3 3`, because every callback shares one function-scoped `i` and the loop ends before the timers run. Use `let i` (a new binding per iteration, giving `0 1 2`) or pass the value into a wrapper function.

**Q: Output of `function outer() { let x = 1; return { inc() { x++; }, get() { return x; } }; } const o = outer(); o.inc(); o.inc(); console.log(o.get());`?**
A: `3`. Both methods close over the same `x`, which starts at 1 and is incremented twice. Calling `outer()` again would create a fresh, independent `x`.

**Q: Write a `once(fn)` helper.**
A: `const once = (fn) => { let done = false, result; return (...args) => { if (!done) { done = true; result = fn(...args); } return result; }; };`. The flag and result live in the closure.

**Q: How would you memoize a function?**
A: Keep a `Map` in a closure, build a key from the arguments (for example `JSON.stringify(args)`), return the cached value if present, otherwise compute and store it. Only memoize pure functions and watch cache growth.

**Q: How can closures cause memory leaks?**
A: A closure keeps its captured scope alive. A long-lived listener or timer that captures a big object stops it from being garbage collected, so remove listeners and clear timers when done.

**Q: What is currying and how does it relate to closures?**
A: Turning `f(a, b)` into `f(a)(b)`. Each returned function remembers the earlier arguments through a closure, which also enables partial application.

### this, call, apply and bind

**Q: What rules decide the value of `this`?**
A: `new` (a fresh object), explicit (`call`/`apply`/`bind`), implicit (`obj.method()` uses `obj`) and default (the global object, or `undefined` in strict mode). Arrow functions skip all of these and use `this` from where they were defined.

**Q: Output of `const o = { n: 1, f() { return this.n; } }; const g = o.f; console.log(g());`?**
A: `undefined` in sloppy mode (`this` is the global object) and a `TypeError` in strict mode or modules (`this` is `undefined`). Pulling a method off its object loses `this`.

**Q: `call` vs `apply` vs `bind`?**
A: `call(thisArg, a, b)` and `apply(thisArg, [a, b])` invoke the function now and differ only in how arguments are passed. `bind(thisArg, ...)` returns a new function with `this` (and optional leading arguments) fixed, without calling it.

**Q: Why does passing `obj.method` as a callback lose `this`, and how do you fix it?**
A: The callback is later called as a plain function with no object. Fix it with `obj.method.bind(obj)`, a wrapper arrow `() => obj.method()`, or an arrow-function class field.

**Q: Can `call` or `bind` change `this` of an arrow function, and should arrows be object methods?**
A: No. An arrow function's `this` is fixed lexically, so `call`/`apply`/`bind` only pass arguments. That is also why an arrow is a poor object method: `this` would be the outer scope, not the object.

**Q: What does the `new` operator do?**
A: It creates an empty object linked to the constructor's `prototype`, runs the constructor with `this` set to that object, and returns it unless the constructor returns another object.

**Q: Output of `function F() { this.a = 1; return { b: 2 }; } console.log(new F());`?**
A: `{ b: 2 }`. If a constructor returns an object, it replaces the new instance. Returning a primitive is ignored.

### Functions

**Q: Arrow function vs regular function?**
A: Arrows have lexical `this`, no own `arguments`, cannot be used with `new` and have no `prototype`. They suit callbacks. Use regular functions for methods that need their own `this` and for constructors.

**Q: What is a pure function and why prefer it?**
A: The same input always gives the same output, with no side effects such as mutating arguments or touching globals. Pure functions are easy to test, cache and reason about, and React reducers rely on them.

**Q: Are default parameter values shared between calls like Python's mutable defaults?**
A: No. They are evaluated on every call, so `function f(a, b = []) { b.push(a); return b; }` returns a fresh array each time.

**Q: Rest vs spread?**
A: Both use `...`. Rest collects items into one array or object (`function f(...args)`, `const { a, ...others } = obj`). Spread expands an array or object into separate items (`[...arr]`, `{ ...obj }`).

### Prototypes and classes

**Q: `prototype` vs `__proto__`?**
A: `prototype` is a property on constructor functions: the object that becomes the prototype of instances created with `new`. `__proto__` (best read with `Object.getPrototypeOf`) is the actual link from an instance to its prototype.

**Q: Where does the prototype chain end, and what is `Object.create(null)`?**
A: It ends at `Object.prototype`, whose prototype is `null`. `Object.create(null)` makes an object with no prototype at all, handy as a clean dictionary with no inherited keys such as `toString`.

**Q: Output of `"toString" in {}` and `Object.hasOwn({}, "toString")`?**
A: `true` and `false`. `in` also checks the prototype chain, while `Object.hasOwn` (the modern `hasOwnProperty`) checks only the object's own properties.

**Q: How is a `class` different from a constructor function?**
A: Mostly sugar over prototypes, but classes are always strict, cannot be called without `new`, are not usable before their declaration (TDZ), have non-enumerable methods and support `extends`, `super` and `#private` fields. `typeof class {}` is `"function"`.

**Q: What are `#private` fields?**
A: Fields declared like `#count` that are truly private, enforced by the language. Accessing `obj.#count` outside the class is a SyntaxError, unlike the `_count` naming convention.

**Q: Output of `class A {} class B extends A { constructor() { this.x = 1; super(); } } new B();`?**
A: A `ReferenceError` saying you must call the super constructor before accessing `this`. In a derived class, call `super()` before using `this`.

**Q: Output of `function Dog() {} Dog.prototype.speak = () => "woof"; const d = new Dog(); Dog.prototype = {}; console.log(d.speak());`?**
A: `"woof"`. The instance keeps its link to the old prototype object. Replacing `Dog.prototype` only affects instances created afterwards.

**Q: Why put methods on the prototype instead of inside the constructor?**
A: Methods defined with `this.fn = function () {}` in the constructor are copied per instance and waste memory. Prototype (class) methods are shared by all instances.

### Event loop and output order

**Q: Output of `console.log("A"); setTimeout(() => console.log("B"), 0); Promise.resolve().then(() => console.log("C")); (async () => { console.log("D"); await null; console.log("E"); })(); console.log("F");`?**
A: `A D F C E B`. Synchronous code runs first (A, D, F), then the microtasks in the order queued (C, then E after the `await`), then the timer (B).

**Q: Microtask vs macrotask?**
A: Microtasks are promise callbacks, `queueMicrotask` and `MutationObserver`. Macrotasks are `setTimeout`, `setInterval`, I/O and UI events. After each macrotask the engine drains the whole microtask queue before the next macrotask or a render.

**Q: Output of `async function f() { console.log(1); await g(); console.log(2); } async function g() { console.log(3); } f(); console.log(4);`?**
A: `1 3 4 2`. `f` runs synchronously until its first `await`, `g` logs 3, and the rest of `f` continues as a microtask after the main script logs 4.

**Q: Output of `Promise.resolve().then(() => console.log(1)).then(() => console.log(2)); Promise.resolve().then(() => console.log(3));`?**
A: `1 3 2`. The second `.then` of the first chain is queued only after the first callback runs, so it lands behind the callback `3` that was already waiting.

**Q: Output of `setTimeout(() => console.log("t1"), 0); setTimeout(() => console.log("t2"), 0); Promise.resolve().then(() => console.log("p"));`?**
A: `p t1 t2`. The microtask runs before any timer, and timers with the same delay run in the order they were scheduled.

**Q: Can promises block the event loop?**
A: Yes. The microtask queue is drained completely, so microtasks that keep queueing more microtasks starve timers and rendering. Heavy synchronous loops block it too.

### Promises and async/await

**Q: Output of `new Promise((res) => { console.log(1); res(); console.log(2); }).then(() => console.log(3)); console.log(4);`?**
A: `1 2 4 3`. The executor runs synchronously, `res()` does not stop the rest of the executor, and the `.then` callback is a microtask that runs after the main script.

**Q: Output of `Promise.resolve(1).then(2).then((v) => console.log(v));`?**
A: `1`. A non-function passed to `.then` is ignored, so the value passes through to the next handler.

**Q: Output of `Promise.reject("x").catch((e) => { console.log(e); return "y"; }).then((v) => console.log(v));`?**
A: `x` then `y`. `catch` handles the rejection, and whatever it returns becomes the resolved value for the next `.then`.

**Q: What happens with an unhandled promise rejection?**
A: Browsers fire an `unhandledrejection` event and log an error. Modern Node versions crash the process by default. Always end chains with `catch` or use `try/catch` around `await`.

**Q: Output of `[1, 2, 3].forEach(async (n) => { await null; console.log(n); }); console.log("done");`?**
A: `done`, then `1 2 3`. `forEach` ignores the promises returned by an async callback and doesn't wait. Use `for...of` with `await`, or `Promise.all(arr.map(...))`.

**Q: What is wrong with `async function load() { try { return fetchData(); } catch (e) { handle(e); } }`?**
A: Returning the promise without `await` means a rejection escapes the `try/catch`. Write `return await fetchData();` when you want to catch errors in that function.

**Q: Sequential `await` in a loop vs `Promise.all`?**
A: `await` inside a `for` loop runs requests one after another. `await Promise.all(items.map(fn))` starts them together, which is faster for independent work. Use a concurrency limit if there are too many.

**Q: How do you cancel a `fetch` or add a timeout?**
A: Pass an `AbortController` signal to `fetch` and call `controller.abort()`, or use `AbortSignal.timeout(ms)` where supported. The fetch then rejects with an `AbortError`.

### Iterators and generators

**Q: What is the iterator protocol?**
A: An iterator is an object with a `next()` method returning `{ value, done }`. An iterable has a `[Symbol.iterator]()` method that returns an iterator, which makes it work with `for...of`, spread and destructuring. Arrays, strings, Map and Set are iterable, plain objects are not.

**Q: What is a generator, and what does `function* g() { yield 1; yield 2; } const it = g(); it.next(); console.log(it.next());` print?**
A: A `function*` can pause at `yield` and resume later, producing values lazily. The log prints `{ value: 2, done: false }`.

**Q: `for...in` vs `for...of`?**
A: `for...in` loops over enumerable property names (as strings, including inherited ones), so avoid it on arrays. `for...of` loops over the values of an iterable.

**Q: What is `for await...of`?**
A: It loops over an async iterable, awaiting each item, which suits streams and paginated APIs that deliver data over time.

### Map, Set and WeakMap

**Q: Map vs plain object?**
A: A Map accepts any type as a key, keeps insertion order, has `.size` and has no inherited keys, so it is better for frequent adds and removes. Objects are simpler and JSON-friendly for fixed records.

**Q: Output of `new Set([1, "1", 1, NaN, NaN]).size`?**
A: `3`. The values are `1`, `"1"` and `NaN`: the number and the string are different, and a Set treats `NaN` as equal to itself.

**Q: Output of `new Map([[{}, 1]]).get({})`?**
A: `undefined`. Object keys compare by reference, and the second `{}` is a different object.

**Q: What is a WeakMap and when is it useful?**
A: A map whose keys must be objects and are held weakly, so an entry disappears when the key object is garbage collected. It has no `size` and can't be iterated. It suits private data or caches keyed by objects without causing leaks.

**Q: Output of `Object.keys({ b: 1, 2: 1, a: 1, 1: 1 })`?**
A: `["1", "2", "b", "a"]`. Integer-like keys come first in ascending order, then string keys in insertion order.

### Arrays

**Q: Output of `[10, 9, 1].sort()`?**
A: `[1, 10, 9]`. The default sort converts items to strings. Use `sort((a, b) => a - b)` for numbers.

**Q: What happens with `[].reduce((a, b) => a + b)`?**
A: `TypeError: Reduce of empty array with no initial value`. Always pass an initial value, for example `reduce(fn, 0)`.

**Q: Output of `[NaN].includes(NaN)` and `[NaN].indexOf(NaN)`?**
A: `true` and `-1`. `includes` uses SameValueZero, which treats `NaN` as equal, while `indexOf` uses strict equality.

**Q: Which array methods mutate and which return a new array?**
A: `push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse` and `fill` mutate. `map`, `filter`, `slice` and `concat` don't, and newer `toSorted`, `toReversed`, `toSpliced` and `with` are non-mutating versions (check browser support).

**Q: Output of `const a = []; a[5] = 1; console.log(a.length);`?**
A: `6`. Assigning past the end creates empty slots, and `length` is the highest index plus one.

### Immutability and copying

**Q: What does `Object.freeze` do and what are its limits?**
A: It stops adding, removing or changing properties of that object, but only shallowly, so nested objects stay mutable. Writes to a frozen object are silently ignored in sloppy mode and throw a TypeError in strict mode.

**Q: `freeze` vs `seal` vs `const`?**
A: `freeze` blocks add, delete and change. `seal` blocks add and delete but lets you change existing values. `const` only stops reassigning the variable, not changing the object.

**Q: How do you update nested state immutably?**
A: Copy each level you change: `{ ...state, user: { ...state.user, name } }`. For deep structures, use Immer, which lets you write mutating code that produces an immutable result.

**Q: What are the limits of `structuredClone`?**
A: It deep-copies most data (including Date, Map, Set and circular references) but throws for functions and DOM nodes, and class instances lose their prototype and become plain objects.

### Modules

**Q: Named vs default exports?**
A: Named exports allow many per file and keep the same name across the codebase, which helps refactoring, autocomplete and tree shaking. A default export is one per module and the importer chooses any name.

**Q: Are ES module imports copies or live bindings?**
A: Live, read-only views of the exporting module's variable, so an updated export is seen by importers. CommonJS `require` returns an object whose primitive exports were copied at require time.

**Q: What is a dynamic `import()`?**
A: A function-like import that returns a promise for the module. It enables lazy loading and code splitting, and it is what `React.lazy` and Next.js dynamic imports use.

**Q: What problem do circular imports cause?**
A: One module may run while the other is half-loaded, so an import can be `undefined` or in the TDZ when first used. Fix it by moving shared code into a third module.

### Errors

**Q: Output of `function f() { try { return 1; } finally { console.log("f"); } } console.log(f());`?**
A: It prints `f` and then `1`. A `finally` block always runs, even after a `return`, and a `return` inside `finally` would override the earlier one.

**Q: Does `try/catch` catch an error thrown inside a `setTimeout` callback or a rejected promise?**
A: Not for the timer: the callback runs later, outside the `try`. Put `try/catch` inside the callback. For promises, use `.catch()` or `await` inside the `try`.

**Q: How do you create a custom error class?**
A: `class ApiError extends Error { constructor(message, status) { super(message); this.name = "ApiError"; this.status = status; } }`. Then check with `instanceof` in `catch` blocks.

**Q: Which built-in error types should you know, and what is `cause`?**
A: `TypeError`, `ReferenceError`, `SyntaxError` and `RangeError` are the common ones. `new Error("msg", { cause: err })` chains the original error so you keep the root cause.

### Regex basics

**Q: Output of `const re = /a/g; console.log(re.test("a"), re.test("a"));`?**
A: `true false`. A global regex remembers `lastIndex` between calls, so the second test starts after the first match. Avoid reusing `g` regexes with `test`.

**Q: Greedy vs lazy matching?**
A: `.*` is greedy and matches as much as possible, so `/<.*>/` on `"<b>x</b>"` matches the whole string. `.*?` is lazy, so `/<.*?>/` matches only `"<b>"`.

**Q: How do you use named groups and `matchAll`?**
A: `/(?<year>\d{4})-(?<month>\d{2})/` lets you read `match.groups.year`. `str.matchAll(re)` (needs the `g` flag) returns an iterator of all matches with their groups.

**Q: What is ReDoS and should you validate emails with regex?**
A: Catastrophic backtracking in a badly written regex can freeze the CPU on crafted input. Use a simple email check and confirm by sending a verification email, instead of a huge regex.

### Date and time

**Q: What are the classic `Date` gotchas, e.g. output of `new Date(2024, 1, 31).getMonth()`?**
A: Months are zero-indexed, and out-of-range days roll over. That call returns `2` because 31 February 2024 becomes 2 March. `Date` is also mutable and parsing is inconsistent.

**Q: `new Date("2024-01-15")` vs `new Date("2024-01-15T00:00:00")`?**
A: A date-only ISO string is parsed as UTC, while a date-time string without an offset is parsed as local time. In time zones behind UTC the first can show the previous day when printed locally.

**Q: How should you store and send dates?**
A: As UTC, using ISO 8601 strings (`toISOString()`) or timestamps, and convert to the user's time zone only for display. Use `timestamptz` in PostgreSQL.

**Q: How do you format dates for a locale and do date maths safely?**
A: Use `Intl.DateTimeFormat` or `toLocaleDateString("en-IN", options)` for display. For adding days or months and handling daylight saving, use a library such as date-fns, or check whether the newer Temporal API is supported in your target environments.

### JSON

**Q: Output of `JSON.stringify({ a: undefined, b: () => 1, c: NaN, d: new Date(0) })`?**
A: `{"c":null,"d":"1970-01-01T00:00:00.000Z"}`. `undefined` and functions are dropped from objects, `NaN` becomes `null` and a Date becomes an ISO string through `toJSON`.

**Q: What does `JSON.parse` do with invalid JSON?**
A: It throws a `SyntaxError`. Trailing commas, single quotes and comments are not valid JSON, so wrap parsing of untrusted input in `try/catch`.

**Q: How are `Map`, `Set`, `BigInt` and `undefined` handled by `JSON.stringify`?**
A: A Map or Set becomes `{}`, so convert with `Array.from` or `Object.fromEntries` first. A BigInt throws a TypeError, and `undefined` is dropped in objects and becomes `null` in arrays.

**Q: Why is `JSON.parse(JSON.stringify(obj))` a poor deep clone?**
A: It drops functions and `undefined`, turns Dates into strings, loses Map/Set and throws on circular references. Use `structuredClone` instead.

### DOM and events

**Q: Event capturing vs bubbling?**
A: An event first travels down from the window to the target (capture), then back up through the ancestors (bubble). Listeners run in the bubble phase by default; pass `{ capture: true }` to listen earlier.

**Q: `event.target` vs `event.currentTarget`?**
A: `target` is the element that triggered the event (the deepest clicked element). `currentTarget` is the element the listener is attached to.

**Q: `stopPropagation` vs `preventDefault`?**
A: `stopPropagation` stops the event from reaching other elements' listeners. `preventDefault` cancels the browser's default action, such as following a link or submitting a form. They are independent.

**Q: What do the `once` and `passive` listener options do?**
A: `once: true` removes the listener after its first call. `passive: true` promises you won't call `preventDefault`, so the browser can scroll smoothly without waiting for your handler (useful for touch and wheel events).

**Q: Why can't you remove a listener added with an anonymous function?**
A: `removeEventListener` needs the same function reference. Keep the handler in a variable, or pass an `AbortController` signal when adding it and abort to remove it.

**Q: `querySelectorAll` vs `getElementsByClassName`?**
A: `querySelectorAll` returns a static NodeList snapshot and accepts any CSS selector. `getElementsByClassName` returns a live HTMLCollection that updates as the DOM changes.

**Q: `textContent` vs `innerHTML` vs `innerText`?**
A: `textContent` reads or sets plain text and is fast and safe. `innerHTML` parses HTML, which is an XSS risk with untrusted input. `innerText` depends on rendered layout, so it can trigger a reflow.

**Q: `DOMContentLoaded` vs `load`?**
A: `DOMContentLoaded` fires when the HTML is parsed (and deferred scripts have run), without waiting for images and styles. `load` fires after everything, including images, has loaded.

### Memory and performance

**Q: How does JavaScript garbage collection work?**
A: Engines use reachability (mark and sweep): objects reachable from roots such as globals and the call stack are kept, and unreachable ones are freed. You can't force it, you only make objects unreachable.

**Q: How do you find a memory leak in a web app?**
A: Watch memory grow in Chrome DevTools, take heap snapshots before and after an action and compare retained objects. Typical causes are detached DOM nodes, forgotten listeners or intervals and ever-growing caches.

**Q: How do you speed up repeated lookups in a big array?**
A: Build a `Map` or `Set` once, so each lookup is O(1) on average, instead of calling `find` or `includes` (O(n)) inside a loop.

**Q: Write a basic `debounce` function.**
A: `const debounce = (fn, ms) => { let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); }; };`. The timer id lives in a closure and resets on every call.

**Q: What is layout thrashing and how do Web Workers help performance?**
A: Alternating DOM reads (like `offsetHeight`) and writes in a loop forces repeated layout, so batch reads first, then writes. Web Workers run heavy JavaScript on another thread, communicating with `postMessage`, so the UI stays responsive.

### Tricky coercion and "what is the output?"

**Q: Output of `typeof null`, `typeof NaN` and `typeof []`?**
A: `"object"`, `"number"` and `"object"`. `typeof null` is a historical quirk, and use `Array.isArray` to test for arrays.

**Q: Output of `[] + []` and `[] + {}`?**
A: `""` and `"[object Object]"`. The `+` operator turns both operands into strings (an empty array becomes `""`).

**Q: Output of `"5" + 2` and `"5" - 2`?**
A: `"52"` and `3`. `+` concatenates when either side is a string, while `-` always converts to numbers.

**Q: Output of `0.1 + 0.2 === 0.3`, and how do you handle money?**
A: `false`, because the sum is `0.30000000000000004` (binary floating point). Compare with a tolerance or, for money, store integer paise/cents.

**Q: Output of `NaN === NaN`, and how do you test for NaN?**
A: `false`. Use `Number.isNaN(x)` or `Object.is(x, NaN)`. The global `isNaN` coerces its argument first, so avoid it.

**Q: Output of `["1", "2", "3"].map(parseInt)`?**
A: `[1, NaN, NaN]`. `map` passes `(value, index)`, so `parseInt("2", 1)` and `parseInt("3", 2)` use invalid radixes. Use `map(Number)` or `map((s) => parseInt(s, 10))`.

**Q: Output of `[] == ![]`?**
A: `true`. `![]` is `false`, and `[]` converts to `""` and then `0`, so `0 == 0`. This is why you use `===`.

**Q: Output of `null == 0`, `null >= 0` and `null == undefined`?**
A: `false`, `true`, `true`. `>=` converts `null` to `0`, but `==` has a special rule where `null` equals only `undefined` (and itself).

**Q: Output of `1 < 2 < 3` and `3 > 2 > 1`?**
A: `true` and `false`. The comparison is evaluated left to right, so `3 > 2 > 1` becomes `true > 1`, which is `1 > 1`.

**Q: Which values are falsy?**
A: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined` and `NaN`. Everything else is truthy, including `[]`, `{}` and the string `"0"`.

**Q: Output of `9007199254740992 === 9007199254740993`, and what is the fix?**
A: `true`. Numbers lose integer precision beyond `Number.MAX_SAFE_INTEGER`. Use `BigInt` (`123n`) for big integers, and don't mix BigInt and Number in arithmetic.

## 4. TypeScript

### Everyday types

**Q: When should you write types explicitly and when let TypeScript infer them?**
A: Let it infer local variables and simple expressions. Annotate function parameters, exported return types and public APIs, where the annotation documents the contract and catches mistakes early.

**Q: Why is `const x = "a"` typed as `"a"` but `let x = "a"` typed as `string`?**
A: A `const` can never change, so TypeScript keeps the narrow literal type. A `let` can be reassigned, so the type widens to `string`.

**Q: What does `as const` do?**
A: It makes a value deeply readonly with literal types. After `const roles = ["admin", "user"] as const;` you can write `type Role = (typeof roles)[number];` to get `"admin" | "user"`.

**Q: Enum vs a union of string literals?**
A: Enums generate runtime code and numeric enums have quirks such as reverse mapping. A union of string literals (or an `as const` object) is erased at compile time, simpler and often preferred.

**Q: What is a tuple?**
A: A fixed-length array with a known type at each position, such as `[string, number]`. React's `useState` returns a tuple of value and setter.

**Q: Type assertion (`as`) vs type guard?**
A: `as` tells the compiler to trust you, with no runtime check, so a wrong assertion hides bugs. A type guard (`typeof`, `instanceof`, a predicate function) really checks at runtime and narrows the type.

**Q: What is the non-null assertion `!` and why use it sparingly?**
A: `user!.name` tells TypeScript the value is not `null` or `undefined`. If you are wrong it crashes at runtime, so prefer a real check or `?.`.

**Q: What does the `satisfies` operator do?**
A: It checks a value against a type without widening the value's inferred type. `const cfg = { port: 3000 } satisfies Config;` catches typos and missing keys but keeps `port` as a number (TypeScript 4.9+).

### Narrowing and type checks

**Q: What is a user-defined type guard (type predicate)?**
A: A function whose return type is `x is Type`, such as `function isUser(x: unknown): x is User`. When it returns true, TypeScript narrows the argument inside that branch.

**Q: How do you write an exhaustiveness check in a `switch`?**
A: In the `default` branch assign the value to a `never` variable: `const _exhaustive: never = action;`. If you add a union member and forget a case, compilation fails.

**Q: What type does `e` have in `catch (e)`, and how do you use it?**
A: With `strict` it is `unknown` (older code treated it as `any`). Narrow it first, for example `if (e instanceof Error) console.log(e.message)`.

**Q: What is structural typing?**
A: Types are compatible when their shapes match, not because of names or declarations, similar to duck typing. Two unrelated interfaces with the same fields are interchangeable.

**Q: Why does `const p: { a: number } = { a: 1, b: 2 }` fail but assigning an existing variable that has `b` works?**
A: Fresh object literals get excess property checks to catch typos. Once the object is in a variable, only shape compatibility is checked, so extra properties are allowed.

**Q: Why is a function that returns a value assignable to a callback typed `() => void`?**
A: A `void` return in a callback type means the caller ignores the result, so any return value is allowed. That is why `arr.forEach((x) => list.push(x))` compiles.

### Generics and advanced types

**Q: How do you constrain a generic?**
A: With `extends`: `function getId<T extends { id: number }>(item: T) { return item.id; }`. Callers can pass anything with an `id`, and the specific type is preserved.

**Q: What do `keyof`, `typeof` and indexed access types do?**
A: `keyof T` is the union of T's property names, `typeof value` gives the type of an existing value in a type position, and `T["key"]` or `T[number]` reads a property or array element type. Example: `type K = keyof typeof config;`.

**Q: What is a mapped type?**
A: A type built by looping over keys: `type MyPartial<T> = { [K in keyof T]?: T[K] };`. Built-ins such as `Partial`, `Readonly` and `Pick` work this way.

**Q: What is a conditional type, and what does `infer` do?**
A: `T extends U ? X : Y` picks a type based on a check, and `infer` captures part of the matched type: `type Item<T> = T extends (infer U)[] ? U : T;`.

**Q: What do `ReturnType`, `Parameters`, `Awaited` and `NonNullable` do?**
A: `ReturnType<F>` is a function's return type, `Parameters<F>` its argument tuple, `Awaited<P>` the resolved value of a Promise and `NonNullable<T>` removes `null` and `undefined`.

**Q: `Omit` vs `Exclude`, and `Pick` vs `Extract`?**
A: `Omit` and `Pick` work on the keys of an object type. `Exclude` and `Extract` filter members of a union, for example `Exclude<"a" | "b", "a">` is `"b"`.

**Q: What are template literal types?**
A: String types built from other string types using template syntax, for example turning `"click" | "hover"` into `"onClick" | "onHover"`. They are useful for typed event names and key patterns.

**Q: What is a branded (opaque) type?**
A: A primitive tagged so it cannot be mixed up: `type UserId = string & { readonly __brand: "UserId" };`. It stops you passing an `OrderId` where a `UserId` is expected, with no runtime cost.

**Q: Why does `Object.keys(obj)` return `string[]` and not `(keyof T)[]`?**
A: Because of structural typing, an object may have extra properties at runtime, so TypeScript can't promise the keys are only the declared ones. A cast is the usual workaround when you know better.

### Interfaces, objects and classes

**Q: What happens when properties conflict in `interface extends` vs an intersection `&`?**
A: `extends` reports an error if the property types are incompatible. An intersection combines them silently, and a conflicting property can collapse to `never`.

**Q: Optional property `a?: string` vs `a: string | undefined`?**
A: An optional property can be left out entirely. `a: string | undefined` must still be present, even if its value is `undefined`.

**Q: Does `readonly` make an object immutable at runtime?**
A: No. `readonly`, `Readonly<T>` and `ReadonlyArray<T>` are compile-time checks only. Use `Object.freeze` for runtime protection.

**Q: `object` vs `Object` vs `{}` as types?**
A: `object` means any non-primitive. `{}` and `Object` accept almost any value except `null` and `undefined`, including primitives, so they are rarely what you want. Prefer a real shape or `Record<string, unknown>`.

**Q: What is declaration merging and module augmentation?**
A: Interfaces with the same name merge, which lets you add fields to existing types, for example `declare global { interface Window { dataLayer: unknown[] } }` or extending Express's `Request`.

**Q: TypeScript `private` vs JavaScript `#private`?**
A: `private` is a compile-time check only and the field is still reachable at runtime. `#field` is real runtime privacy enforced by the JavaScript engine.

### Configuration and tooling

**Q: What does `strict: true` turn on?**
A: A group of checks including `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply` and `useUnknownInCatchVariables`. New projects should enable it (check the docs for the exact list in your version).

**Q: What does `noUncheckedIndexedAccess` do?**
A: It types `arr[i]` and `record[key]` as `T | undefined`, so you must handle a missing value. It is not part of `strict`, but it catches real bugs.

**Q: Does Vite, Babel or SWC type-check your code?**
A: No. They only strip types for speed. Run `tsc --noEmit` in CI (or use a framework build step that type-checks) so type errors actually fail the pipeline.

**Q: What are `.d.ts` files and `@types` packages?**
A: Declaration files describe the types of JavaScript code. Packages like `@types/react` from DefinitelyTyped add types for libraries that don't ship their own.

**Q: What does `import type` do?**
A: It imports only a type and is always erased from the output. That avoids accidental runtime imports and helps tools that compile one file at a time.

**Q: How do you migrate a JavaScript project to TypeScript gradually?**
A: Enable `allowJs`, rename files to `.ts` or `.tsx` one at a time, start with a lenient config and tighten `strict` flags later. Add types at API boundaries first.

### TypeScript with React and APIs

**Q: How do you type React props and children?**
A: `type Props = { title: string; children?: React.ReactNode };` then `function Card({ title, children }: Props)`. Many teams type props directly instead of using `React.FC`.

**Q: How do you type `useState` when the initial value is `null`?**
A: Give the type explicitly: `useState<User | null>(null)`. Otherwise it is inferred as `null` and you can't set a user later.

**Q: How do you type event handlers and refs?**
A: `React.ChangeEvent<HTMLInputElement>` for input changes, `React.MouseEvent<HTMLButtonElement>` for clicks, and `useRef<HTMLInputElement>(null)` for DOM refs.

**Q: How do you write a generic React component?**
A: `function List<T>({ items, render }: { items: T[]; render: (item: T) => React.ReactNode })`. The item type is inferred from `items`.

**Q: What does `response.json()` return in TypeScript, and how should you type it?**
A: `Promise<any>`. Don't just cast it. Validate with a schema library such as Zod and use `z.infer<typeof Schema>`, so the runtime check and the static type come from one source.

**Q: How can a TypeScript frontend stay in sync with a FastAPI backend?**
A: FastAPI publishes an OpenAPI schema, and generators (for example openapi-typescript) can produce TS types or a client from it. That stops hand-written types from drifting out of date.

## 5. HTML and CSS

### Semantic HTML and document basics

**Q: Block vs inline vs inline-block elements?**
A: Block elements start on a new line and take the full width (`div`, `p`). Inline elements flow within text and ignore width and height (`span`, `a`). `inline-block` flows inline but accepts width, height and vertical padding.

**Q: What does `<!DOCTYPE html>` do?**
A: It puts the browser in standards mode. Without it browsers use quirks mode, which has old, inconsistent layout behaviour.

**Q: `<section>` vs `<article>` vs `<div>`?**
A: `article` is self-contained content that could stand alone (a blog post, a card). `section` groups related content under a heading. `div` has no meaning and is just a styling hook.

**Q: `<button>` vs `<a>`?**
A: Use `<a href>` to navigate and `<button>` to perform an action. Both are keyboard accessible by default, while a clickable `div` needs roles, `tabindex` and key handlers to match.

**Q: `defer` vs `async` on a `<script>`?**
A: Both download without blocking HTML parsing. `defer` runs scripts in order after the document is parsed. `async` runs each script as soon as it arrives, in any order, which suits independent scripts such as analytics.

**Q: How do you write good `alt` text?**
A: Describe the image's purpose or content in a short phrase. For purely decorative images use `alt=""` so screen readers skip them.

**Q: How do `srcset` and `<picture>` help?**
A: `srcset` and `sizes` let the browser pick the best image size for the screen and pixel density. `<picture>` lets you offer different formats (AVIF, WebP) or a different crop per breakpoint.

**Q: Why set `width` and `height` on images, and when not to use `loading="lazy"`?**
A: The attributes let the browser reserve space before the image loads, preventing layout shift. `loading="lazy"` defers offscreen images, but don't use it on the hero or LCP image because it delays your most important image.

**Q: What are `data-*` attributes?**
A: Custom attributes for storing small bits of data on elements. Read them in JavaScript with `element.dataset.name` or select them in CSS with attribute selectors.

### Forms

**Q: Why use specific input types like `email`, `tel` and `number`?**
A: They bring the right mobile keyboard, built-in validation and better autofill. Pair them with `autocomplete` values such as `email` or `one-time-code`, and always validate again on the server.

**Q: How does native form validation work?**
A: Attributes such as `required`, `pattern`, `min`, `max` and `minlength` make the browser block submission and show messages. The `:invalid` pseudo-class lets you style invalid fields.

**Q: What is the default `type` of a `<button>` inside a form?**
A: `submit`. A button meant only for a click handler should be `type="button"`, otherwise it submits the form.

**Q: Why does the `name` attribute matter on inputs?**
A: Form submission and `FormData` use `name` as the key, and radio buttons share a `name` to form a group. An input without a `name` is not submitted.

**Q: `readonly` vs `disabled` on an input?**
A: A `disabled` input can't be focused and is not submitted. A `readonly` input can be focused and is submitted, but the user can't edit it.

**Q: How do you upload a file with a form or `fetch`?**
A: Use `method="post"` with `enctype="multipart/form-data"` and an `<input type="file">`. With `fetch`, send a `FormData` body and don't set the `Content-Type` header yourself, so the browser adds the boundary.

**Q: Is `placeholder` a substitute for `<label>`?**
A: No. A placeholder disappears when typing, often has low contrast and is not a reliable accessible name. Use a visible `<label for>` or wrap the input in the label.

### Accessibility

**Q: What is the first rule of ARIA?**
A: Use a native HTML element if one exists. ARIA only changes what assistive technology is told (roles, states), it adds no keyboard behaviour, and wrong ARIA is worse than none.

**Q: `aria-label` vs `aria-labelledby` vs `aria-describedby`?**
A: `aria-label` gives a string name, `aria-labelledby` points to another element's text as the name, and `aria-describedby` points to extra description such as help text or an error message.

**Q: When should you use `aria-hidden="true"`?**
A: To hide purely decorative or duplicate content from screen readers. Never put it on focusable elements, because keyboard users could focus something assistive technology can't see.

**Q: How do you make a modal dialog accessible?**
A: Move focus into it when it opens, keep focus inside while it is open, close on Esc, return focus to the trigger and give it an accessible name. The native `<dialog>` with `showModal()` handles much of this.

**Q: What do `tabindex="0"`, `tabindex="-1"` and positive values do?**
A: `0` puts a non-interactive element into the natural tab order. `-1` makes it focusable by script or click but skips it when tabbing. Positive values create a confusing custom order and should be avoided.

**Q: What contrast ratios does WCAG AA require?**
A: 4.5:1 for normal text, and 3:1 for large text and for UI components and icons that convey information.

**Q: Why is `outline: none` a problem, and what is `:focus-visible`?**
A: Removing the focus ring leaves keyboard users lost. `:focus-visible` applies focus styling mainly for keyboard focus, so you can style it without showing rings on mouse clicks.

**Q: What are `aria-live` regions for?**
A: They announce dynamic changes (toasts, form errors, result counts) to screen readers. `polite` waits for a pause and `assertive` interrupts, so use `assertive` sparingly.

**Q: How do you name an icon-only button, and why does heading order matter?**
A: Add `aria-label="Close"` (or visually hidden text) to the button and mark the decorative icon `aria-hidden="true"`. Screen reader users jump between headings, so use one `h1` and don't skip levels.

**Q: How do you test accessibility?**
A: Use only the keyboard, try a screen reader (NVDA, VoiceOver), run axe or Lighthouse, and add lint rules such as `eslint-plugin-jsx-a11y`. Automated tools find only part of the issues.

**Q: What does `prefers-reduced-motion` do?**
A: It is a media query that detects users who asked their OS to reduce animation. Turn off or simplify large motion inside `@media (prefers-reduced-motion: reduce)`.

### Selectors, cascade and specificity

**Q: Which wins: `#nav a` or `.menu .item a.link`, and what if specificity is equal?**
A: `#nav a` wins (one ID beats any number of classes). Specificity is compared column by column: IDs, then classes, then elements. If it is equal, the rule that appears later in the CSS wins.

**Q: How do `:is()`, `:where()` and `:not()` affect specificity?**
A: `:is()` and `:not()` take the specificity of their most specific argument. `:where()` always counts as zero, which makes it good for easy-to-override defaults.

**Q: Descendant space vs `>` vs `+` vs `~` selectors?**
A: Space matches any descendant, `>` a direct child, `+` the next sibling and `~` any later sibling.

**Q: Pseudo-class vs pseudo-element?**
A: A pseudo-class (`:hover`, `:first-child`) targets an element in a state or position. A pseudo-element (`::before`, `::placeholder`) targets a generated element or a part of one. `::before` needs a `content` value to show.

**Q: Which CSS properties are inherited?**
A: Mostly text-related ones such as `color`, `font-*` and `line-height`, not box properties such as `margin` or `border`. The keywords `inherit`, `initial` and `unset` control this explicitly.

**Q: What are CSS custom properties, and how do they differ from Sass variables?**
A: `--brand: #0a5;` used as `var(--brand)`. They are live at runtime, cascade and inherit, and can change per element or from JavaScript, which makes theming and dark mode easy. Sass variables are compiled away.

**Q: What is margin collapsing?**
A: Vertical margins of adjacent block siblings (or a parent and its first child with no padding or border) merge into the larger one instead of adding. It does not happen inside flex or grid containers.

**Q: What are CSS cascade layers (`@layer`)?**
A: A way to order groups of rules explicitly (reset, base, components, utilities) so that layer order beats specificity between layers. They help tame third-party CSS.

### Layout: flexbox, grid and positioning

**Q: How do you center a div horizontally and vertically?**
A: On the parent use `display: grid; place-items: center;` or `display: flex; justify-content: center; align-items: center;`.

**Q: In flexbox, `justify-content` vs `align-items` vs `align-content`?**
A: `justify-content` aligns along the main axis, `align-items` along the cross axis for each line, and `align-content` distributes multiple wrapped lines.

**Q: What does `flex: 1` mean?**
A: Shorthand for `flex: 1 1 0%`: grow to fill space, shrink if needed and start from a zero basis, so siblings share the space equally.

**Q: Why won't text truncate inside a flex child, and how do you fix it?**
A: Flex items default to `min-width: auto`, so they won't shrink below their content width. Set `min-width: 0` on the item, plus `overflow: hidden; text-overflow: ellipsis; white-space: nowrap`.

**Q: How do you build a responsive card grid without media queries?**
A: Use `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));` with `gap`. Columns wrap automatically as the container width changes.

**Q: `auto-fit` vs `auto-fill` in grid?**
A: Both create as many columns as fit. `auto-fill` keeps the empty tracks, while `auto-fit` collapses them so the existing items stretch to fill the row.

**Q: Why isn't my `z-index` working?**
A: It only applies to positioned elements (and flex or grid items), and it is compared only inside its stacking context. A parent with `transform`, `opacity` below 1 or its own `z-index` can trap the child.

**Q: Why does `position: sticky` not stick?**
A: Usual causes: no `top` (or other offset) is set, an ancestor has `overflow: hidden`, `auto` or `scroll`, or the parent is too short for the element to travel.

**Q: Why use `dvh` instead of `vh` on mobile?**
A: `100vh` can be taller than the visible area when mobile browser bars show. `dvh` follows the dynamic viewport height as the bars collapse or expand.

### Responsive design

**Q: Mobile-first vs desktop-first media queries?**
A: Mobile-first writes base styles for small screens and adds `@media (min-width: ...)` for larger ones. It ships simpler CSS to phones and is usually easier to maintain.

**Q: What problem do container queries solve?**
A: `@container` lets a component respond to its container's size instead of the viewport, so the same card works in a narrow sidebar and a wide column.

**Q: How does `clamp()` help typography?**
A: `font-size: clamp(1rem, 2.5vw, 2rem)` scales smoothly between a minimum and a maximum without media queries.

**Q: Why use logical properties such as `margin-inline-start`?**
A: They follow the writing direction, so layouts flip automatically for right-to-left languages such as Urdu or Arabic without separate left/right CSS.

**Q: How do you support dark mode in CSS?**
A: Define colors as CSS variables and switch them with `@media (prefers-color-scheme: dark)`, or with a class or data attribute when the user picks a theme.

### Browser rendering and performance

**Q: What is the critical rendering path?**
A: HTML becomes the DOM, CSS becomes the CSSOM, the two combine into the render tree, then the browser does layout, paint and compositing.

**Q: What is render-blocking, and how do you reduce it?**
A: CSS blocks rendering until it loads, and synchronous scripts block HTML parsing. Keep CSS small, inline critical CSS, load scripts with `defer` and avoid unused CSS and JavaScript.

**Q: Reflow vs repaint vs composite: which animations are cheap?**
A: Layout (reflow) recalculates geometry and is expensive, repaint redraws pixels, and compositing just moves layers on the GPU. Animate `transform` and `opacity` instead of `width`, `top` or `left`.

**Q: How do you fix a poor CLS score?**
A: Reserve space for images, embeds, ads and fonts (`width` and `height`, `aspect-ratio`), avoid inserting content above existing content and animate with transforms.

**Q: How do you improve LCP?**
A: Get the main image or text on screen sooner: a fast server response, an optimised and correctly sized hero image, `fetchpriority="high"` or a preload for it, no lazy loading on it and less render-blocking CSS and JavaScript.

**Q: What is INP and how do you improve it?**
A: Interaction to Next Paint measures how quickly the page responds to user input across a visit. It replaced FID as a Core Web Vital. Break up long JavaScript tasks, reduce main-thread work and avoid heavy re-renders.

**Q: How should web fonts be loaded?**
A: Use WOFF2, subset the fonts, preload the critical one and set `font-display: swap` (or `optional`) so text isn't invisible while loading. Fewer weights and families means faster loads.

**Q: `preload` vs `prefetch` vs `preconnect`?**
A: `preload` fetches a resource needed for the current page now. `prefetch` fetches something likely needed later at low priority. `preconnect` opens the connection (DNS, TCP, TLS) to another origin early.

