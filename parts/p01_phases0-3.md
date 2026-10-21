# Prerequisite assessment

Research date: 2026-10-09.

You are a React and Next.js developer, so you may feel you know "the basics". This test checks that honestly. The rule is simple: **you skip a topic only if you can DEMONSTRATE it.** "I have seen it" or "I can ask Claude" does not count.

> **Honest note:** Many working developers have gaps under the surface. They can build a React page but cannot explain a closure, write a SQL join without help, or fix a merge conflict calmly. This test is not a judgement. It only tells you where to spend your 8-10 hours per week.

## How to take the test

1. Use a fresh empty folder. No AI, no copy-paste from old projects. Documentation (MDN, official docs) is allowed, because real work allows it.
2. Give yourself 15 minutes per task. If you are not done in 15 minutes, mark it "not passed".
3. A task passes only if the code runs AND you can explain every line out loud in simple English.
4. Write your score for each area in the table at the end. Do the whole test in Week 1 (about 3 hours in total, spread over two sittings).

## The 25 tasks

### HTML (3 tasks)

- [ ] **H1.** Write a page with `header`, `nav`, `main`, `article`, `aside`, `footer`. No `div` is allowed for these roles. Explain why this helps screen readers.
- [ ] **H2.** Build a signup form with name, email, password, a select, and a checkbox. Every input has a real `<label>`. Use built-in validation (`required`, `type="email"`, `minlength`) with no JavaScript.
- [ ] **H3.** Make a data table with `caption`, `thead`, `tbody`, and `scope` on header cells.

### CSS (3 tasks)

- [ ] **C1.** Build a 3-column card layout with CSS Grid that becomes 1 column below 640px. No framework.
- [ ] **C2.** Centre a box horizontally and vertically in two different ways (flexbox and grid). Explain `box-sizing: border-box`.
- [ ] **C3.** Given two conflicting CSS rules, predict which wins and why (specificity). Then define 3 CSS variables and use them for a dark/light switch.

### JavaScript (5 tasks)

- [ ] **J1.** Write a counter factory using a closure (`makeCounter()` returns `increment` and `get`). Explain where the variable lives.
- [ ] **J2.** Given an array of orders `{ id, status, total }`, use `filter`, `map`, and `reduce` to get the total of paid orders. No loops.
- [ ] **J3.** Predict the output order of a snippet that mixes `console.log`, `setTimeout(..., 0)`, and `Promise.resolve().then(...)`. Explain the event loop.
- [ ] **J4.** Write an `async` function that fetches a public API, handles a 404 (fetch does not throw on 404!) and a network error, and returns data or a clear error.
- [ ] **J5.** Explain what `this` is in a normal function, an arrow function, and a method called with `.call()`. Show one bug caused by a lost `this`.

### React (3 tasks)

- [ ] **R1.** Build a searchable list with a debounced input. State is local. No `useEffect` for derived data.
- [ ] **R2.** Write a `useFetch(url)` custom hook with loading, error, and cleanup (AbortController). Explain the effect dependency array.
- [ ] **R3.** Explain why a list needs a stable `key`, and show a bug when you use the array index as key in a reorderable list.

### Node.js (3 tasks)

- [ ] **N1.** Create a small Express (or plain `http`) server with `GET /health` and `POST /echo` that returns JSON.
- [ ] **N2.** Add one middleware (logger) and one error-handling middleware. Explain the order of middleware.
- [ ] **N3.** Read a value from `process.env` (loaded from a `.env` file), and show that `.env` is in `.gitignore`.

### Git (3 tasks)

- [ ] **G1.** Make a repo, 3 commits, a branch, a merge. Show `git log --oneline --graph`.
- [ ] **G2.** Create a merge conflict on purpose and resolve it by hand.
- [ ] **G3.** Push a branch to GitHub and open a pull request. Explain what `.gitignore` does and why `node_modules` and `.env` are in it.

### SQL (3 tasks)

- [ ] **S1.** Given tables `users` and `orders`, write a `JOIN` that lists each user with their order count (include users with zero orders).
- [ ] **S2.** Write a `GROUP BY` with `HAVING` (for example, users with more than 3 orders).
- [ ] **S3.** Explain primary key vs foreign key, and what an index does in one sentence each.

### Python (2 tasks)

- [ ] **P1.** Create a virtual environment, install `requests`, and call a public API from a script.
- [ ] **P2.** Write a function with a default argument, a list comprehension, and a `try/except`. Read a JSON file and print a summary.

## Scoring guide

Count how many tasks you passed in each area. Then use the table.

| Area | Tasks | Strong (skip or skim) | Medium (do the phase, move fast) | Weak (do the full phase and slower track) |
| --- | --- | --- | --- | --- |
| HTML + CSS | 6 | 5-6 | 3-4 | 0-2 |
| JavaScript | 5 | 5 | 3-4 | 0-2 |
| React | 3 | 3 | 2 | 0-1 |
| Node.js | 3 | 3 | 2 | 0-1 |
| Git | 3 | 3 | 2 | 0-1 |
| SQL | 3 | 3 | 2 | 0-1 |
| Python | 2 | 2 | 1 | 0 |

What each result means in this roadmap:

- **Strong:** You may skip that phase's reading and videos. Still do its checkpoint at the end of the phase. If you fail the checkpoint, you were not strong.
- **Medium:** Do the phase, but spend your time only on the concepts you got wrong.
- **Weak:** Do the whole phase. Use the slower-track option in the week plan. Do not feel bad: this is exactly why the roadmap has 24 weeks.

> **Warning:** Do not skip JavaScript (J1 to J5) even if everything else is strong. Closures, `this`, and the event loop are the base for React hooks, Node, and later async Python. Most "mystery bugs" come from here.

> **Tip:** Be especially honest about Git (G2, G3), SQL (S1, S2) and Python (all). Frontend developers often have not used them under pressure. Phases 7, 8 and 9 assume you can do S1, S2, P1 and P2 before you start. If you cannot do them now, they become Week 9-10 work, so plan time.

Record your result here:

| Area | Score | Decision |
| --- | --- | --- |
| HTML + CSS | __ / 6 | skip / skim / full |
| JavaScript | __ / 5 | skip / skim / full |
| React | __ / 3 | skip / skim / full |
| Node.js | __ / 3 | skip / skim / full |
| Git | __ / 3 | skip / skim / full |
| SQL | __ / 3 | skip / skim / full |
| Python | __ / 2 | skip / skim / full |


# Phase 0 — Developer foundations and setup

## Why this phase matters

Everything later sits on this: how a browser talks to a server, how you move around the terminal, how Git saves your work, and how you keep secrets safe. Many tutorials skip these because "everyone knows them". In practice, a lot of beginner pain (CORS errors, "command not found", leaked API keys, broken `node_modules`) comes from missing one small idea here. This phase is light on code and heavy on mental models. It is only one week, so you will not become an expert, but you will stop being surprised.

## Prerequisites and "skip test"

You can skip a topic if you can DEMONSTRATE it:

- Explain, in 2 minutes and without notes, what happens from typing `https://example.com/products` until the page appears (DNS, TCP, TLS, HTTP, render).
- In a terminal, create a folder tree, move files, show hidden files, and read file permissions (`ls -l`) without a GUI.
- Show a repo with a branch, a merge, a resolved conflict, and a pull request on GitHub.
- Show a `.env` file that is git-ignored plus a `.env.example` that is committed, and read a value from `process.env`.
- Create a Python virtual environment and install one package inside it.

If you pass all five, skim this phase for the OS-specific setup table and the debugging section, then go to Phase 1.

## Concepts explained

### How the web works: frontend, backend, database, deployment

**[Must learn now]** A website is a conversation between two computers. Your **browser** is the *client*. It asks for things. A **server** is a computer that is always on and answers. The **frontend** is the code that runs in the browser (HTML, CSS, JavaScript, React). The **backend** is code that runs on a server (Node, Python). The **database** is where the backend keeps data safely on disk. **Deployment** means putting your code on a server on the internet so other people can use it.

Analogy: a restaurant. The browser is the customer, the frontend is the menu and the table, the backend is the kitchen, the database is the pantry, and deployment is opening the restaurant door to the public.

```js
// Frontend (browser): ask the backend for data
const res = await fetch("https://api.example.com/products");
const products = await res.json();
console.log(products.length);
```

Common mistake: thinking that React "talks to the database". It does not. React runs in the browser. Only your backend (or a Next.js server function) talks to the database, because the browser must never hold database passwords.

Interview questions:

- What is the difference between frontend, backend, and database in a web app?
- Why should a browser never connect directly to your production database?
- Where does a Next.js Server Component run, and why does that matter for secrets?

### What happens after you type a URL

**[Must learn now]** Steps, in order:

1. The browser reads the URL: scheme (`https`), host (`example.com`), path (`/products`).
2. **DNS** turns the name `example.com` into an IP address like `93.184.216.34`. DNS is the phone book of the internet. Answers are cached in the browser, the OS and your internet provider.
3. The browser opens a **TCP connection** to that IP and a **port** (443 for HTTPS).
4. For HTTPS, a **TLS handshake** happens: the server shows a certificate, both sides agree on a secret key, and from then on traffic is encrypted.
5. The browser sends an **HTTP request**. The server sends back an **HTTP response** (usually HTML).
6. The browser parses HTML, finds CSS, JS and images, requests those too, builds the DOM, and paints pixels.

You can watch this in Chrome: DevTools, Network tab, reload the page, click the first row.

Common mistake: believing "the page is slow because of React". Often the time is DNS, a slow server response, or a huge image. Always look at the Network tab first.

Interview questions:

- Walk me through what happens when I type a URL and press Enter.
- What does DNS do, and what is a DNS cache?
- Why is HTTPS needed, and what does a certificate prove?

### HTTP request/response lifecycle, JSON, REST, ports

**[Must learn now]** HTTP is plain text rules for the conversation. A **request** has a *method* (`GET` read, `POST` create, `PUT`/`PATCH` update, `DELETE` remove), a *path*, *headers* (extra info like `Authorization`), and an optional *body*. A **response** has a *status code*, headers, and a body.

Status code families: `2xx` success, `3xx` redirect, `4xx` your request was wrong (401 not logged in, 403 not allowed, 404 not found, 422 invalid data), `5xx` server broke.

**JSON** is the text format for data: `{"name":"Asha","age":25}`. **REST** is a style: URLs are *nouns* (`/orders/42`) and methods are *verbs*. A **port** is a numbered door on a computer: 80 for HTTP, 443 for HTTPS, 3000 and 5173 are common dev ports, 5432 is PostgreSQL, 27017 is MongoDB.

```js
const res = await fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "hello", body: "world", userId: 1 }),
});
console.log(res.status); // 201
console.log(await res.json());
```

Common mistake: forgetting that `fetch` only rejects on network failure. A 404 or 500 still "succeeds", so you must check `res.ok`. (More in Phase 1.)

Interview questions:

- What is the difference between PUT and PATCH? Is GET safe and idempotent?
- What does status 401 mean versus 403?
- What makes an API "RESTful"? Give a good and a bad URL example.
- Two apps both want port 3000. What happens?

### Client-server architecture and HTTPS in practice

**[Must learn now]** Servers are stateless by default: each request stands alone, and the server does not remember you. To remember a login, we send something with each request (a cookie or a token). **HTTPS** = HTTP over TLS. It gives encryption (nobody can read it), integrity (nobody can change it), and identity (you really reached `example.com`). In development you use `http://localhost`, which browsers treat as a safe exception.

Analogy: a bank counter clerk who forgets you after each visit. You show your ID card (token) every time.

Common mistake: storing a "logged in" flag only in React state. A refresh erases it, and anyone can fake it. The server must verify the cookie or token on every request.

Interview questions:

- What does "stateless" mean for HTTP? How do we keep users logged in?
- What are the three things TLS gives you?

### Terminal, files, folders, paths, permissions

**[Must learn now]** The terminal is a text way to talk to your computer. A **shell** is the program inside it (zsh on Mac, bash on Linux, PowerShell on Windows). Commands you must know:

| Task | macOS and Linux | Windows PowerShell |
| --- | --- | --- |
| Where am I? | `pwd` | `pwd` |
| List files (with hidden) | `ls -la` | `ls -Force` |
| Go into a folder | `cd projects` | `cd projects` |
| Go up one folder | `cd ..` | `cd ..` |
| Make folder | `mkdir -p a/b` | `mkdir a\b` |
| Create empty file | `touch a.txt` | `ni a.txt` |
| Copy, move, delete | `cp`, `mv`, `rm -r` | `cp`, `mv`, `rm -r` |
| Show a file | `cat a.txt` | `cat a.txt` |
| Search text | `grep -rn "word" .` | `Select-String -Path * -Pattern "word"` |
| Find a program | `which node` | `where.exe node` |

A **path** is the address of a file. *Absolute* starts from the root (`/Users/asha/app` on Mac and Linux, `C:\Users\asha\app` on Windows). *Relative* starts from where you are (`./src/index.js`, `../config`). Mac and Linux use `/`. Windows uses `\` but Node and Git accept `/` too. Use `path.join()` in Node so your code works everywhere.

**Permissions** (Mac and Linux): `ls -l` shows something like `-rwxr-xr-- `. Three groups (owner, group, others) times three rights (read, write, execute). `chmod +x script.sh` lets you run a script. Never fix a permission error with `sudo npm install`; it creates root-owned files that cause more errors later. Windows uses a different permission model; if you work in WSL (Linux inside Windows) you get the Linux behaviour.

Common mistake: running `rm -rf` with a wrong path or a variable that is empty. Always run `pwd` and `ls` before deleting.

Interview questions:

- What is the difference between an absolute and a relative path?
- What does `chmod 755 file` mean?
- Why is `sudo npm install -g` a bad idea?

### Environment variables

**[Must learn now]** An environment variable is a named value that lives outside your code, given to a program when it starts. Examples: `PORT=3000`, `DATABASE_URL=...`, `OPENAI_API_KEY=...`. Your code reads it, so the same code can run in dev and production with different settings.

```js
// Node: read env variables
const port = process.env.PORT ?? 3000;
console.log(`Server will use port ${port}`);
```

```bash
# macOS / Linux
export PORT=4000
node server.js

# Windows PowerShell
$env:PORT = "4000"
node server.js
```

Frontend note: in Vite, only variables starting with `VITE_` are put in the browser bundle; in Next.js, only `NEXT_PUBLIC_`. Anything in the browser bundle is **public**. Never put a secret there.

Common mistake: putting an API key in a `NEXT_PUBLIC_` variable "to make it work". Now every visitor can read it in DevTools.

Interview questions:

- Why use environment variables instead of constants in code?
- What does `NEXT_PUBLIC_` change, and what is the security risk?
- Where is `process.env` available: browser, server, or both?

### Installing and updating tools (macOS, Windows, Linux)

**[Must learn now]** You need: **Git**, **Node.js** (current LTS; the Node download page shows v24 as LTS on the research date, and v26 as the newest line), **VS Code**, **Python 3** (python.org lists 3.14 as current; use whatever is the latest stable your tools support), and a terminal. Use a **version manager** for Node, so you can switch versions without admin rights.

| Step | macOS | Windows 10/11 | Linux (Ubuntu or Debian) |
| --- | --- | --- | --- |
| Package manager | Homebrew from brew.sh | winget (built in) | apt (built in) |
| Git | `brew install git` | `winget install Git.Git` | `sudo apt install git` |
| VS Code | `brew install --cask visual-studio-code` | `winget install Microsoft.VisualStudioCode` | Download .deb from the VS Code site |
| Node.js | `nvm` or `brew install node` | `winget install OpenJS.NodeJS.LTS` or nvm-windows | `nvm` (install script from its repo) |
| Python 3 | `brew install python` | python.org installer, tick "Add to PATH" | `sudo apt install python3 python3-venv python3-pip` |
| Best shell | zsh (default) | PowerShell; for Python and backend work, use WSL2 | bash or zsh |
| Check versions | `node -v`, `git --version`, `python3 --version` | same, but `python --version` | same as macOS |

Windows extras that save pain:

- Install **WSL2** (`wsl --install` in an admin PowerShell). It gives you a real Ubuntu terminal. Many server tools in this roadmap (Docker, Linux commands, Python venvs) behave exactly like production there.
- Line endings: Windows uses CRLF, Linux uses LF. Run `git config --global core.autocrlf true` on Windows (or `input` on Mac and Linux) to avoid noisy diffs.
- PowerShell may block scripts (such as venv activation). The fix is `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

macOS extras:

- Command line tools: `xcode-select --install` gives you git and compilers some npm and pip packages need.
- On Apple Silicon (M1/M2/M3), prefer ARM builds; avoid mixing Intel Homebrew under `/usr/local` with ARM Homebrew under `/opt/homebrew`.

Linux extras:

- Do not use the old Node from `apt`. Use nvm, or the official instructions on nodejs.org.
- Docker Desktop is not needed on Linux; you install Docker Engine (Phase 15).

Update habits: update Node by installing the new LTS with your version manager; keep a `.nvmrc` file or `engines` field in `package.json` so your team uses the same version. Update VS Code and extensions monthly. Never upgrade major tools in the middle of a project week.

Recommended VS Code extensions: ESLint, Prettier, GitLens (optional), Python (later), Tailwind CSS IntelliSense. Turn on "format on save".

Common mistake: installing Node from three different places (installer, brew, nvm). `which node` then points to a surprise. Choose one method and remove the others.

Interview questions:

- How do you manage multiple Node versions on one machine?
- What is the `PATH` variable and why does "command not found" happen?

### Package managers: npm, npx, Python venv and pip

**[Must learn now]** A **package manager** downloads libraries and records exact versions. For JavaScript: **npm** (comes with Node). `package.json` lists dependencies, `package-lock.json` freezes exact versions (commit it), and `node_modules/` holds downloaded code (never commit it). **npx** runs a package's command without installing it globally, for example `npx create-next-app@latest`.

```bash
npm init -y
npm install express          # runtime dependency
npm install -D vitest        # dev-only dependency
npm run test                 # runs "test" script from package.json
npx prettier --check .       # run a tool once
```

Python has a different habit: every project gets its own **virtual environment**, a private folder of packages, so projects do not clash.

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install requests
pip freeze > requirements.txt

# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install requests
```

`uv` (from Astral) is a fast modern alternative to pip and venv; we will use it later in the Python phase. For now, plain `venv` + `pip` is enough and is what every tutorial shows.

Common mistake: running `pip install` outside a venv, which changes your global Python. Check that your prompt shows `(.venv)` first.

Interview questions:

- What is the difference between `dependencies` and `devDependencies`?
- Why commit `package-lock.json` but not `node_modules`?
- What problem does a Python virtual environment solve?

### Git: repos, commits, branches, merging, pull requests, .gitignore

**[Must learn now]** Git is a time machine for your project. A **repository** (repo) is your project plus its history. A **commit** is a saved snapshot with a message. A **branch** is a separate line of work. **Merging** joins a branch back. A **pull request (PR)** is a GitHub page where you ask to merge your branch and others review it. `.gitignore` lists files Git must not track.

Three places a change lives: working directory (edited), staging area (`git add`), repository (`git commit`).

```bash
git init
git add .
git commit -m "feat: add health route"
git switch -c feature/login        # new branch
# ...edit files...
git add -p && git commit -m "feat: add login form"
git switch main
git merge feature/login            # join the work
git log --oneline --graph
git push -u origin feature/login   # then open a PR on GitHub
```

Starter `.gitignore` for a JS and Python project:

```text
node_modules/
.env
.env.*
!.env.example
dist/
.next/
.venv/
__pycache__/
.DS_Store
```

Merge conflict: two branches changed the same lines. Git marks them with `<<<<<<<`, `=======`, `>>>>>>>`. Open the file, keep the right code, delete the markers, then `git add` and `git commit`.

Good habits: small commits; messages like `feat(scope): summary` (Conventional Commits); one branch per task; never commit directly to `main` on a team; pull before you push.

Common mistake: committing a secret, then deleting it in the next commit. It is still in history. Rotate (replace) the key immediately; deleting is not enough.

Interview questions:

- What is the difference between `git merge` and `git rebase`?
- What does `git stash` do? When do you use it?
- You committed `.env` by mistake. What do you do?
- What is the difference between `git fetch` and `git pull`?

### .env files, secret management, and why API keys must not be committed

**[Must learn now]** A `.env` file holds secrets for local development: `KEY=value` lines. It is ignored by Git. You commit a `.env.example` with fake values, so teammates know which variables exist. Why not commit keys: public repos are scanned by bots within minutes, and stolen cloud or AI keys can create large bills quickly. GitHub has *secret scanning* that warns you, but prevention is your job.

```bash
# .env  (never commit)
DATABASE_URL=postgres://user:pass@localhost:5432/app
OPENAI_API_KEY=sk-xxxx

# .env.example  (commit this)
DATABASE_URL=postgres://user:pass@localhost:5432/app
OPENAI_API_KEY=
```

```js
// Node 20+ can load .env with a flag, no library needed:
//   node --env-file=.env server.js
if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is missing. Copy .env.example to .env");
}
```

In production you do not copy a `.env` file by hand. You set variables in your host (Vercel, AWS, Docker) or a secret manager. The Twelve-Factor App idea: config lives in the environment, not in code.

Rules: one key per environment; least permissions; rotate if leaked; never paste keys into chat, screenshots, issues, or AI prompts.

Common mistake: logging `process.env` or the full request headers while debugging. Logs often get stored and shared.

Interview questions:

- How do you handle secrets in local dev versus production?
- A key was pushed to a public repo 10 minutes ago. List your steps.

### Reading error messages, debugging, docs, asking good questions

**[Must learn now]** Most time is spent reading, not writing. Read errors from the **top and the bottom**: the first line says *what*, the stack trace says *where*. Find the first line that points to *your* file, not to `node_modules`.

```text
TypeError: Cannot read properties of undefined (reading 'map')
    at ProductList (src/ProductList.jsx:12:25)
```

This says: `products` was `undefined` on line 12. Now ask why: did the fetch finish? Is the API shape different?

A debugging routine you can repeat:

1. Reproduce the bug with the smallest steps.
2. Read the exact error message. Copy it.
3. Print or inspect the real values (`console.log`, `debugger`, DevTools Sources).
4. Change one thing at a time. Undo changes that did not help.
5. Search with the exact message, add the tool name and version.
6. Read official docs for the function you misused.
7. Ask for help with a good question (below).

A good question includes: what you want, what you did, exact error text, a minimal code sample, what you already tried, versions of tools. See the Stack Overflow guide in the resources. With Claude: paste the error and the code, and say "do not give me the fix yet, give me hints".

Common mistake: changing five things at once, then not knowing which one fixed (or broke) the app.

Interview questions:

- Describe how you debug a production bug you cannot reproduce locally.
- How do you read a stack trace?

### A basic software development workflow

**[Must learn now]** The loop you will use for 24 weeks:

1. Understand the task. Write it in one sentence and a short checklist.
2. Create a branch.
3. Build the smallest working piece. Run it.
4. Test it (manually first, then with an automated test).
5. Commit with a clear message.
6. Push, open a PR, review your own diff first.
7. Merge, deploy, check it works in the real environment.
8. Write what you learned in your notes file.

Analogy: a kitchen. You prep, cook one dish, taste, serve, then clean up. You do not cook ten dishes at once.

Common mistake: a "big bang" commit after three days. When something breaks, you cannot find out why.

Interview questions:

- Describe your normal flow from ticket to production.
- Why do teams use pull requests and code review?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| How the web works | URL, DNS, TCP, TLS, HTTP, render | [MDN: How the web works](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_Web_works) and [MDN: HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | [What happens when you click a URL (JayPMedia, English)](https://www.youtube.com/watch?v=1XbvNSwvkAs) | Beginner | 1 h | Record the Network tab for one site and label each request |
| HTTP details | Methods, status, headers, a typical session | [MDN: A typical HTTP session](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Session) and [MDN: status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status) | Same video above; no second video needed | Beginner | 1 h | Use `curl -i` on 3 URLs and explain each header |
| Terminal and files | Navigation, paths, permissions | [MDN: Command line crash course](https://developer.mozilla.org/docs/Learn_web_development/Getting_started/Environment_setup/Command_line) and [VS Code terminal basics](https://code.visualstudio.com/docs/terminal/basics) | [Command Line Basics for Beginners (freeCodeCamp, Beau Carnes, English)](https://www.youtube.com/watch?v=mABpAI-pCw0) | Beginner | 1.5 h | Build a folder tree and set a script executable using only the terminal |
| Tool setup | Git, Node, Python, VS Code, OS differences | [Node.js download](https://nodejs.org/en/download), [nvm](https://github.com/nvm-sh/nvm), [Homebrew](https://brew.sh/), [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/), [WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [VS Code setup](https://code.visualstudio.com/docs/setup/setup-overview) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | Write a SETUP.md that lets a stranger rebuild your machine |
| Package managers | npm, npx, venv, pip, uv | [npm: about npm](https://docs.npmjs.com/about-npm), [npx](https://docs.npmjs.com/cli/v10/commands/npx), [Python venv](https://docs.python.org/3/library/venv.html), [uv](https://docs.astral.sh/uv/) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Make one Node project and one Python venv project, each with one dependency |
| Git and GitHub | Commit, branch, merge, PR, .gitignore | [Pro Git book](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F), [gitignore docs](https://git-scm.com/docs/gitignore), [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) | [Git and GitHub Crash Course for Beginners 2026 (freeCodeCamp, Sumit Saha, English)](https://www.youtube.com/watch?v=mAFoROnOfHs) | Beginner | 3 h | Create a conflict on purpose, resolve it, open a PR to yourself |
| Secrets and env | .env, .env.example, secret scanning | [12-Factor: Config](https://12factor.net/config), [GitHub secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Add dotenv-style loading to a small script and a startup check for missing variables |
| Debugging and questions | Stack traces, DevTools, asking well | [Chrome DevTools](https://developer.chrome.com/docs/devtools), [How to ask (Stack Overflow)](https://stackoverflow.com/help/how-to-ask), [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Break your own code in 5 ways and write down the error and the fix |

## Verification notes

- **youtube.com/oembed was not reachable** from my environment (connections to youtube.com timed out). I verified every video title and channel through `noembed.com`, a public service that returns YouTube's own oEmbed data (title and channel). I also opened some watch pages with a fetch tool to see the title. Because of this, **durations were NOT verified with `lengthSeconds`**.
- JayPMedia `1XbvNSwvkAs`: title "What happens when you click a URL: DNS Lookup, TCP Handshake & HTTP IN 3 MINUTES (With Visuals)", channel JayPMedia, English. Duration: about 3 minutes by title; not verified.
- freeCodeCamp `mAFoROnOfHs`: title "Git & GitHub Crash Course for Beginners [2026]", channel freeCodeCamp.org. The freeCodeCamp article that embeds it names Sumit Saha as the instructor and calls it about a 1-hour watch. I confirmed the article embeds this exact video ID. Language: English (not formally verified). Duration not verified from the video itself.
- freeCodeCamp `mABpAI-pCw0`: title "Command Line Basics for Beginners - Full Course", channel freeCodeCamp.org. The article that embeds it names Beau Carnes and says about one hour. Language: English (not formally verified). Duration not verified from the video.
- For Git, a second older freeCodeCamp video exists (`RGOj5yH7evk`, "Git and GitHub for Beginners - Crash Course", Gwen Faraday). I verified title and channel but I did not include it in the table, to avoid overlapping courses.
- All documentation links in the table returned HTTP 200 when fetched on 2026-10-09. Several pages are client-rendered, so I confirmed the status code but not every heading.
- Node LTS (v24 line) and Python 3.14 information comes from the Node download page and the Python docs page I opened. Check them again on the day you install. The exact `winget` package IDs shown (`Git.Git`, `Microsoft.VisualStudioCode`, `OpenJS.NodeJS.LTS`) are common IDs that I did not individually test; confirm with `winget search`.

## Hands-on exercises

1. **Network detective.** Open any site you know. In DevTools Network, find the HTML document, one CSS file, one image. Write its status code, size, and `cache-control` header.
2. **Curl tour.** Run `curl -i https://example.com`, `curl -I https://developer.mozilla.org`, and a POST to `https://jsonplaceholder.typicode.com/posts`. Explain each line of the response.
3. **Terminal only.** Create `phase0/a/b/c`, put three files in it, move one, copy one, delete one, list hidden files. Do not use Finder or Explorer.
4. **Permissions.** On Mac, Linux, or WSL: create `hello.sh` that prints your name, run it (it fails), `chmod +x`, run it again.
5. **Setup log.** Install every tool in the setup table. Write `SETUP.md` with the exact commands you used on your OS and the version output.
6. **Git drill.** Make a repo, 5 commits, two branches that edit the same line, merge, solve the conflict, push, open a PR to your own `main`.
7. **Secrets drill.** Create `.env`, `.env.example`, `.gitignore`. Run `git status` and prove `.env` is ignored. Add a startup check that crashes with a clear message when a variable is missing.
8. **Broken app.** Take a tiny Express or script file, introduce five errors (typo, wrong path, missing env, wrong port, undefined variable) and practise reading each message.

## Checkpoint

**Explain (out loud, 2 minutes each):**

- What happens when you type a URL? Include DNS, TCP, TLS, HTTP.
- Why is a secret in `NEXT_PUBLIC_` unsafe?
- What is the difference between `package.json` and `package-lock.json`?

**Modify:** Change your Git repo so `dist/` and `.env` are ignored even though they were already committed once (hint: `git rm --cached`).

**Debug:** Your teammate says "node: command not found" after installing Node. List three things you check (PATH, restart terminal, version manager).

**Write a test / check:** Write a small script that exits with code 1 and a clear message when required env variables are missing. Run it with and without the variables.

**Ready to move on when:**

- All tools in the setup table run and you have a SETUP.md.
- You finished the Git drill without help, including a conflict.
- You explained the URL journey without notes.
- Your `.env` is ignored and you know what to do if a key leaks.

## Week plan

### Week 1 — Phase 0 foundations and the prerequisite assessment (estimated hours: 9)

**Learning objectives**

- Explain how a browser, DNS, TCP/TLS, HTTP, and a server work together.
- Work comfortably in a terminal on your OS.
- Have a clean, documented dev environment.
- Use Git with branches, merges, conflicts, and a PR.
- Handle env variables and secrets safely.
- Know exactly which later phases you can skim, from the assessment.

**Topics and subtopics**

- **[Must learn now]** Prerequisite assessment (25 tasks, about 3 h across two sittings; do it first)
- **[Must learn now]** How the web works, URL journey, HTTP, JSON, REST, ports
- **[Must learn now]** Terminal, paths, permissions
- **[Must learn now]** Tool setup for your OS and version managers
- **[Must learn now]** npm, npx, venv, pip
- **[Must learn now]** Git workflow and `.gitignore`
- **[Must learn now]** `.env`, secrets, safe habits
- **[Must learn now]** Debugging routine and asking good questions
- **[Learn later if needed]** WSL2 deep dive (Windows only), SSH keys for Git (needed when you deploy)

**Small prerequisite concepts**

- What a "process" is (a running program) and what "localhost" means (your own computer).
- Plain text vs binary files, and what an "extension" really is (just part of the name).
- What "open source" and "license" mean at a basic level.

**Reading**

- [MDN: How the web works](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_Web_works)
- [MDN: HTTP overview](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [MDN: Command line crash course](https://developer.mozilla.org/docs/Learn_web_development/Getting_started/Environment_setup/Command_line)
- [Pro Git: What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [Pro Git: Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [12-Factor: Config](https://12factor.net/config)

**Video**

- "What happens when you click a URL: DNS Lookup, TCP Handshake & HTTP IN 3 MINUTES (With Visuals)", JayPMedia, English, about 3 minutes by title (duration not verified): [watch](https://www.youtube.com/watch?v=1XbvNSwvkAs)
- "Command Line Basics for Beginners - Full Course", freeCodeCamp.org (Beau Carnes), English, about 1 hour per article (duration not verified): [watch](https://www.youtube.com/watch?v=mABpAI-pCw0)
- "Git & GitHub Crash Course for Beginners [2026]", freeCodeCamp.org (Sumit Saha), English, about 1 hour per article (duration not verified): [watch](https://www.youtube.com/watch?v=mAFoROnOfHs)

**Hands-on exercises**

1. Take the 25-task assessment and fill the score table (about 3 h).
2. Do exercises 1 to 3 of the Phase 0 list (network, curl, terminal).
3. Complete the setup table and write SETUP.md.
4. Do the Git drill and the secrets drill.
5. Do the "broken app" exercise.

**What you must build**

A repo called `dev-foundations` on GitHub containing: `SETUP.md`, `.gitignore`, `.env.example`, a small `check-env.js` script, a `NOTES.md` with your assessment scores, and at least 8 meaningful commits plus one merged PR.

**Completion checklist**

- [ ] Assessment finished and scored honestly
- [ ] Node, Git, VS Code, Python installed and versions recorded
- [ ] Can navigate and manage files in the terminal without a GUI
- [ ] Merge conflict created and resolved
- [ ] PR opened and merged on GitHub
- [ ] `.env` ignored, `.env.example` committed
- [ ] Can explain the URL journey without notes
- [ ] Phase 0 checkpoint passed

**Self-test**

1. What are the steps between pressing Enter on a URL and seeing the page?
2. What is the difference between a 401 and a 403?
3. Why do we use a virtual environment in Python?
4. You pushed a secret key. What are your first three actions?
5. What does `git add` do versus `git commit`?

**Common mistakes**

- Skipping the assessment and "feeling" ready.
- Installing Node in several ways and breaking PATH.
- Using `sudo` to silence npm permission errors.
- Committing `.env` or `node_modules`.
- Watching videos without typing the commands.

**Ready to continue when**

- You can show your SETUP.md, your Git history with a conflict resolved, and your assessment table.
- You can explain the URL journey in under 2 minutes.
- You have decided, with evidence, which phases to skim.

**Slower-track option**

Split into two weeks: week 1a = assessment, setup and terminal; week 1b = Git, env and debugging. Skip the optional WSL deep dive and the second Git video. Keep the checkpoint; it is not optional.


# Phase 1 — JavaScript fundamentals

## Why this phase matters

You write JavaScript every day in React, but React hides many core ideas. When a hook "does not update", when `this` is `undefined`, or when two requests finish in a strange order, the cause is almost always a core JavaScript idea: closures, references, `this`, or the event loop. Node, TypeScript, and even Python's `asyncio` later reuse these ideas. This phase is a gap-fill, not a beginner course. Spend your time on what the assessment showed you are weak at.

## Prerequisites and "skip test"

You may skip a concept if you can DEMONSTRATE it from a blank file, without AI:

- Predict the output order of a snippet with `console.log`, `setTimeout(0)`, a resolved Promise `.then`, and `async/await`, and explain it with "call stack, microtask queue, task queue".
- Write a closure-based counter and explain why two counters do not share state.
- Explain `this` in a method, a detached method, an arrow function, and after `bind`.
- Write `fetch` code that handles `res.ok === false` and a network error.
- Write `Promise.all` and `Promise.allSettled` versions of "load 3 things" and explain when each is right.
- Write 3 small tests with Node's built-in test runner or Vitest.

## Concepts explained

Every concept below has: a label, plain explanation, an analogy, a small example, a common mistake, and interview questions.

### Variables: let, const, var

**[Must learn now]** `const` makes a name that cannot be pointed at something else. `let` makes a name you may reassign. `var` is the old way: it is function-scoped (not block-scoped) and *hoisted* (moved to the top as `undefined`). Use `const` by default, `let` when you must reassign, and never `var` in new code.

Analogy: `const` is a label glued onto a box. You cannot move the label to another box, but you can still change what is *inside* the box if it is an object.

```js
const user = { name: "Asha" };
user.name = "Ravi";      // allowed: we changed the inside
// user = {};            // TypeError: Assignment to constant variable

console.log(a); // undefined (var is hoisted)
var a = 1;
// console.log(b); // ReferenceError (let is in the temporal dead zone)
let b = 2;
```

Common mistake: believing `const` means "frozen". It only freezes the *binding*. Use `Object.freeze` for shallow freezing, or just do not mutate.

Interview questions:

- What is hoisting? What is the temporal dead zone?
- Why can you `push` to a `const` array?
- What is the difference between block scope and function scope?

### Primitive vs reference values; strings, numbers, booleans, null, undefined

**[Must learn now]** Primitives (`string`, `number`, `boolean`, `null`, `undefined`, `bigint`, `symbol`) are copied by value. Objects, arrays, and functions are passed by *reference*: two names can point to the same object. `undefined` means "no value was set"; `null` means "I set it to empty on purpose". Numbers are floating point, so `0.1 + 0.2 !== 0.3`.

Analogy: a primitive is a number written on a sticky note (copy the note, they are independent). An object is a house address (copy the address, both notes point to the same house).

```js
let x = 5;
let y = x;
y = 6;
console.log(x); // 5

const a = { n: 1 };
const b = a;       // same house
b.n = 2;
console.log(a.n);  // 2

console.log(typeof null);      // "object" (an old bug in the language)
console.log(0.1 + 0.2);        // 0.30000000000000004
console.log(Number.isNaN(NaN)); // true
```

Common mistake: comparing objects with `===` and expecting deep equality. `{} === {}` is `false`. In React this matters: a new object each render means a "changed" prop.

Interview questions:

- What are the primitive types? Why is `typeof null` "object"?
- How do you deep clone an object (`structuredClone`) and why is spread shallow?
- Why is `0.1 + 0.2 !== 0.3`? How do you handle money? (Use integer paise/cents.)

### Operators, comparison, truthy/falsy, coercion

**[Must learn now]** `===` compares value and type. `==` converts types first (coercion) and gives surprises. Use `===`. Falsy values: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`. Everything else is truthy, including `"0"`, `[]`, and `{}`. `??` (nullish coalescing) only replaces `null` and `undefined`; `||` replaces every falsy value.

```js
console.log(0 == "");        // true  (surprise)
console.log(0 === "");       // false
console.log([] ? "yes" : "no"); // "yes"

const count = 0;
console.log(count || 10);    // 10  (bug if 0 is valid)
console.log(count ?? 10);    // 0   (correct)

console.log("5" + 1);        // "51"
console.log("5" - 1);        // 4
```

Common mistake: `const port = process.env.PORT || 0` when 0 is a legal value. Use `??`.

Interview questions:

- `==` vs `===`? What does `[] == false` give and why?
- What is the difference between `||` and `??`?
- List the falsy values.

### Conditions, loops, iteration

**[Must learn now]** Use `if/else`, `switch`, and the ternary `a ? b : c`. Loops: `for`, `while`, `for...of` (values of an iterable such as an array), `for...in` (keys of an object; rarely needed). Prefer `for...of` or array methods over index loops. `break` and `continue` control loops. `forEach` cannot be stopped early and does not wait for `await`.

```js
const items = ["a", "b", "c"];
for (const item of items) console.log(item);
for (const [i, item] of items.entries()) console.log(i, item);

for (const [k, v] of Object.entries({ x: 1, y: 2 })) console.log(k, v);
```

Common mistake: using `items.forEach(async (i) => { await save(i); })` and expecting it to finish before the next line. It does not wait. Use `for...of` with `await`, or `Promise.all(items.map(...))`.

Interview questions:

- `for...of` vs `for...in`?
- Why does `await` inside `forEach` not behave like inside `for...of`?

### Functions: parameters, return, scope, declarations, expressions, arrows

**[Must learn now]** A function can be declared (`function f() {}`, hoisted), an expression (`const f = function() {}`, not usable before the line), or an arrow (`const f = () => {}`). Arrows have a shorter syntax and **no own `this`**. Parameters can have defaults. A function with no `return` returns `undefined`. **Scope** decides which names a piece of code can see: inner scopes can see outer ones, not the other way around.

```js
function add(a, b = 0) { return a + b; }
const double = (n) => n * 2;
const makeUser = (name) => ({ name }); // parentheses to return an object

function outer() {
  const secret = "x";
  return function inner() { return secret; }; // inner sees outer's variable
}
```

Common mistake: `const f = () => { name: "a" }` returns `undefined` because `{}` is read as a block. Wrap the object in `()`.

Interview questions:

- Function declaration vs expression: what differs in hoisting?
- Why can't you use an arrow function as a constructor?
- What are default parameters? When are they evaluated?

### Arrays and objects

**[Must learn now]** Arrays hold ordered items (`push`, `pop`, `slice`, `splice`, `includes`, `at`). Objects hold key-value pairs. Know `Object.keys/values/entries`, `Object.assign`, and `Map`/`Set` for when you need non-string keys or unique items. `slice` copies, `splice` mutates; `sort` mutates (use `toSorted` in modern JS, or copy first).

```js
const nums = [3, 1, 2];
const sorted = [...nums].sort((a, b) => a - b); // copy, then sort
console.log(nums, sorted); // [3,1,2] [1,2,3]

const unique = [...new Set([1, 1, 2, 3, 3])]; // [1,2,3]
const prices = new Map([["tea", 10], ["coffee", 20]]);
console.log(prices.get("tea"));
```

Common mistake: sorting numbers without a compare function. `[10, 9, 1].sort()` gives `[1, 10, 9]` (string order).

Interview questions:

- Which array methods mutate and which return a new array?
- When would you use `Map` over a plain object?
- How do you remove duplicates from an array?

### Destructuring, spread, rest, optional chaining

**[Must learn now]** Destructuring unpacks values: `const { name, age = 18 } = user`. Spread (`...`) copies or expands. Rest (`...args`) collects the remaining items. Optional chaining `?.` stops safely when something is `null` or `undefined`.

```js
const user = { id: 1, profile: { city: "Surat" }, tags: ["a", "b"] };
const { id, profile: { city }, tags: [firstTag, ...otherTags] } = user;

const updated = { ...user, id: 2 };       // shallow copy with a change
const sum = (...nums) => nums.reduce((s, n) => s + n, 0);

console.log(user.address?.street);        // undefined, no crash
console.log(user.getName?.() ?? "none");  // safe call
```

Common mistake: believing spread makes a deep copy. Nested objects are still shared, which breaks React state updates that mutate nested data.

Interview questions:

- What is the difference between spread and rest?
- How do you update one nested field immutably?
- What does `a?.b.c` do when `a` is null?

### map, filter, reduce, find, some, every

**[Must learn now]** These are the daily tools. `map` transforms each item, `filter` keeps some, `reduce` folds many into one, `find` returns the first match, `some` and `every` answer yes/no. They return new values and do not change the original.

```js
const orders = [
  { id: 1, status: "paid", total: 500 },
  { id: 2, status: "pending", total: 300 },
  { id: 3, status: "paid", total: 200 },
];
const paidTotal = orders
  .filter((o) => o.status === "paid")
  .reduce((sum, o) => sum + o.total, 0);   // 700

const ids = orders.map((o) => o.id);
const firstPending = orders.find((o) => o.status === "pending");
const allPaid = orders.every((o) => o.status === "paid"); // false
const grouped = orders.reduce((acc, o) => {
  (acc[o.status] ??= []).push(o);
  return acc;
}, {});
```

Common mistake: `reduce` without an initial value on an empty array throws. Always pass the second argument.

Interview questions:

- Implement `map` using `reduce`.
- `find` vs `filter()[0]`? (`find` stops early.)
- Group an array of objects by a key.

### Object methods and immutability

**[Must learn now]** Immutability means "do not change the old value; make a new one". React, Redux, and many bugs depend on it. Tools: spread, `Object.freeze` (shallow), `structuredClone` (deep), array methods that return copies (`map`, `filter`, `slice`, `toSorted`, `with`).

```js
const state = { user: { name: "Asha" }, items: [1, 2] };
const next = {
  ...state,
  user: { ...state.user, name: "Ravi" },
  items: [...state.items, 3],
};
console.log(state.items.length, next.items.length); // 2 3
```

Common mistake: `state.items.push(3); setState(state)` in React. The reference is the same, so React may not re-render.

Interview questions:

- Why does React need immutable updates?
- `Object.freeze` vs `const`? Is freeze deep?

### Callbacks, higher-order functions, closures

**[Must learn now]** A **callback** is a function you hand to another function to call later. A **higher-order function** takes or returns functions (`map`, `addEventListener`, `debounce`). A **closure** is a function that remembers the variables from where it was *created*, even after the outer function has finished.

Analogy: a closure is a backpack. When a function is made, it packs the variables around it. Wherever it travels, the backpack goes with it.

```js
function makeCounter() {
  let count = 0;                    // lives in the backpack
  return {
    increment: () => ++count,
    get: () => count,
  };
}
const a = makeCounter();
const b = makeCounter();
a.increment(); a.increment();
console.log(a.get(), b.get()); // 2 0

function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}
```

React link: the "stale closure" bug. A `useEffect` or handler captures `count` from one render and keeps using the old value.

```js
for (var i = 0; i < 3; i++) setTimeout(() => console.log(i), 0); // 3 3 3
for (let j = 0; j < 3; j++) setTimeout(() => console.log(j), 0); // 0 1 2
```

Common mistake: the `var` in the loop above. Each `let` iteration gets its own binding.

Interview questions:

- What is a closure? Give a real use (private state, memoize, debounce).
- Why does the `var` loop print 3 3 3?
- What is a stale closure in React and how do you avoid it?

### this, binding, prototypes, classes

**[Must learn now]** `this` is decided by *how a function is called*, not where it is written (arrow functions are the exception: they use `this` from where they are written). Rules: `obj.method()` gives `this = obj`; a plain call `fn()` gives `undefined` in strict mode and modules; `fn.call(x)` or `fn.bind(x)` sets it; `new F()` makes a new object; arrow functions take it from the surrounding scope.

```js
const user = {
  name: "Asha",
  hello() { return `Hi ${this.name}`; },
  later() { setTimeout(() => console.log(this.name), 0); }, // arrow keeps this
};
const f = user.hello;
// f();                    // this is undefined: TypeError in a module
const g = user.hello.bind(user);
console.log(g());          // "Hi Asha"
```

**Prototypes**: every object has a hidden link to another object (its prototype). If a property is not found, JavaScript looks up the chain. `class` is cleaner syntax over this same system.

```js
class Account {
  #balance = 0;                       // private field
  constructor(owner) { this.owner = owner; }
  deposit(n) { this.#balance += n; return this; }
  get balance() { return this.#balance; }
}
class Savings extends Account {
  addInterest() { return this.deposit(this.balance * 0.05); }
}
const s = new Savings("Asha").deposit(100).addInterest();
console.log(s.balance); // 105
```

Common mistake: passing `obj.method` as a callback (`button.onclick = obj.method`) and losing `this`. This is also why React class components needed `bind`.

Interview questions:

- List the rules that decide `this`.
- `call` vs `apply` vs `bind`?
- What is the prototype chain? What does `class` compile to?
- Why do arrow functions not work as methods that need `this`?

### Modules: import and export; CommonJS vs ES modules

**[Must learn now]** A module is a file with its own scope. **ES modules (ESM)** use `import` and `export`, are standard in browsers, Vite, and Next.js, and are analysed statically (good for tree-shaking). **CommonJS (CJS)** uses `require()` and `module.exports`, the older Node style. Node decides by file extension (`.mjs`/`.cjs`) or `"type": "module"` in `package.json`.

```js
// math.js (ESM)
export const add = (a, b) => a + b;
export default function multiply(a, b) { return a * b; }

// app.js
import multiply, { add } from "./math.js"; // Node ESM needs the extension

// CommonJS
// const { add } = require("./math");
// module.exports = { add };

// dynamic import (works in both)
const { add: add2 } = await import("./math.js");
```

Common mistakes: using `__dirname` in ESM (use `import.meta.dirname` in current Node, or `fileURLToPath`); forgetting the `.js` extension in Node ESM; mixing `require` and `import` in one file.

Interview questions:

- CJS vs ESM: loading time, syntax, `this` at the top level, tree-shaking?
- What is a default export vs a named export? Why do many teams prefer named exports?
- What is a circular import and what goes wrong?

### Error handling: try/catch

**[Must learn now]** `throw` an `Error` object (not a string). `try/catch/finally` handles errors. `finally` always runs (good for cleanup). A `catch` only catches errors inside its own `try`, and in async code only if you `await` the call. Create custom errors by extending `Error`.

```js
class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.name = "HttpError";
    this.status = status;
  }
}

function parseJson(text) {
  try {
    return JSON.parse(text);
  } catch (err) {
    throw new Error("Invalid JSON", { cause: err });
  } finally {
    console.log("parse finished");
  }
}
```

Common mistake: an empty `catch {}` that hides bugs. Log it or rethrow it.

Interview questions:

- When does `finally` run? What if `try` has a `return`?
- How do you handle errors in async code?
- Why extend `Error` rather than throw a string?

### Promises and async/await

**[Must learn now]** A Promise is a receipt for a value that will arrive later. States: *pending*, *fulfilled*, *rejected*. `.then` handles success, `.catch` handles failure. `async/await` is nicer syntax over promises: `await` pauses *that function* (not the whole program) until the promise settles. An `async` function always returns a Promise.

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function load() {
  try {
    await wait(100);
    const res = await fetch("https://jsonplaceholder.typicode.com/todos/1");
    return await res.json();
  } catch (err) {
    console.error("failed:", err.message);
    throw err;
  }
}
load().then((todo) => console.log(todo.title));
```

Common mistakes: forgetting `await` (you get a Promise, not data); `await` in a loop when the requests are independent (slow, sequential); not handling rejections (unhandled rejection can crash Node).

Interview questions:

- What are the three states of a Promise?
- What does `async` change about a function's return value?
- Rewrite a `.then` chain using `async/await` with correct error handling.
- What is an unhandled promise rejection?

### Event loop, call stack, microtasks

**[Must learn now]** JavaScript runs one thing at a time on the **call stack**. Slow things (timers, network) are handed to the environment (browser or Node). When they finish, their callbacks wait in a queue. When the stack is empty, the **event loop** moves the next callback in. There are two queues: **microtasks** (Promise `.then`, `await` continuation, `queueMicrotask`) run first and are fully drained; **tasks/macrotasks** (`setTimeout`, I/O, UI events) run after.

Analogy: a single cashier (the stack). Customers with long jobs (timers, downloads) go sit in the waiting room and are called back one at a time. VIPs (microtasks) are served before the next normal customer.

```js
console.log("1 start");
setTimeout(() => console.log("2 timeout"), 0);
Promise.resolve().then(() => console.log("3 microtask"));
(async () => { console.log("4 inside async"); await null; console.log("5 after await"); })();
console.log("6 end");
// Order: 1 start, 4 inside async, 6 end, 3 microtask, 5 after await, 2 timeout
```

Common mistake: a heavy synchronous loop (`for` over a million items) blocks the stack, so the UI freezes and no callbacks run. Split the work, use a Web Worker, or move it to the server.

Interview questions:

- Explain the event loop. What is the difference between microtasks and macrotasks?
- Why does `setTimeout(fn, 0)` not run immediately?
- Predict the output of the snippet above and explain it.
- Is JavaScript single-threaded? How does it do async work?

### Promise.all, allSettled, race, and concurrency basics

**[Must learn now]** If tasks do not depend on each other, start them together and wait once. `Promise.all` waits for all and **rejects at the first failure**. `Promise.allSettled` always waits for all and tells you each result. `Promise.race` gives the first to settle. `Promise.any` gives the first success. "Concurrency" here means overlapping waiting time; it is not parallel CPU work.

```js
const getJson = async (url) => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
};

const [user, posts] = await Promise.all([
  getJson("https://jsonplaceholder.typicode.com/users/1"),
  getJson("https://jsonplaceholder.typicode.com/posts?userId=1"),
]);

const results = await Promise.allSettled([
  getJson("https://jsonplaceholder.typicode.com/todos/1"),
  getJson("https://jsonplaceholder.typicode.com/nope"), // 404
]);
for (const r of results) {
  console.log(r.status, r.status === "fulfilled" ? r.value.title : r.reason.message);
}
```

Limit concurrency: do not fire 1,000 requests at once. Process in batches of 5 to 10 (or use a small helper like `p-limit` in real projects).

Common mistake: `for (const id of ids) { await get(id) }` for independent calls (slow). Another: `Promise.all` when you want partial results (use `allSettled`).

Interview questions:

- `Promise.all` vs `allSettled` vs `race` vs `any`?
- How would you run 100 requests but only 5 at a time?
- Is `await Promise.all` parallel? (Waiting is overlapped; JS code still runs on one thread.)

### Fetch API and HTTP error handling

**[Must learn now]** `fetch` returns a Promise that rejects only on network failure (offline, DNS error, CORS block). A 404 or 500 is a *successful* fetch with `res.ok === false`. So you must check it yourself. Read the body once (`res.json()` or `res.text()`). Support cancel with `AbortController` and a timeout with `AbortSignal.timeout(ms)`.

```js
async function request(url, options = {}) {
  let res;
  try {
    res = await fetch(url, { signal: AbortSignal.timeout(8000), ...options });
  } catch (err) {
    throw new Error(`Network error or timeout: ${err.message}`);
  }
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`HTTP ${res.status}: ${body.slice(0, 200)}`);
  }
  return res.status === 204 ? null : res.json();
}
```

Common mistake: `const data = await (await fetch(url)).json()` with no `ok` check; a 500 HTML page then crashes `.json()` with a confusing error.

Interview questions:

- Why does `fetch` not throw on a 404?
- How do you cancel a fetch? Why is this important in React effects?
- How do you send JSON with `POST`?

### Memory basics and common mistakes

**[Learn during projects]** JavaScript frees memory automatically with *garbage collection*: an object is removed when nothing can reach it. A **memory leak** happens when you keep a reference without meaning to: forgotten timers, event listeners never removed, growing global caches, closures holding big objects, detached DOM nodes. Fix by cleaning up (`clearInterval`, `removeEventListener`, abort controllers) and by bounding caches.

```js
const handler = () => console.log("scroll");
window.addEventListener("scroll", handler);
// later, cleanup
window.removeEventListener("scroll", handler);
```

Common mistakes list for the whole phase: `==` instead of `===`; mutating shared objects; missing `await`; `forEach` with async; forgetting `res.ok`; `parseInt` without radix on user input; shadowed variable names; swallowing errors.

Interview questions:

- What is a memory leak in a JS app? Name three causes.
- How does garbage collection decide what to free?

### Debugging with browser DevTools

**[Must learn now]** Learn five tools: **Console** (`console.table`, `console.error`), **Sources** (breakpoints, step over/into, watch, call stack panel, "pause on exceptions"), **Network** (status, timing, request and response bodies, throttling), **Performance** (flame chart for slow code), **Application** (storage, cookies). Use `debugger;` in code to pause. For Node, run `node --inspect` and open `chrome://inspect`, or use VS Code's debugger.

Practice: set a breakpoint inside a `.map` callback and watch variables change; use "blackbox" to skip library code; use a "conditional breakpoint" for the 500th loop iteration.

Common mistake: `console.log` everywhere for hard bugs. A breakpoint shows the full state and the call stack in one stop.

Interview questions:

- How do you find which request is slow? How do you find which function is slow?
- How do you debug a bug that happens only on the 100th item of a loop?

### Basic JavaScript testing

**[Must learn now]** A test calls your code with known input and checks the output. Pattern: Arrange, Act, Assert. Two good starting points: Node's built-in `node:test` (nothing to install) and **Vitest** (fast, works with Vite and React projects). Test pure functions first; they are easy and give the most value.

```js
// sum.js
export const sum = (nums) => nums.reduce((s, n) => s + n, 0);

// sum.test.js (Vitest)
import { describe, it, expect } from "vitest";
import { sum } from "./sum.js";

describe("sum", () => {
  it("adds numbers", () => expect(sum([1, 2, 3])).toBe(6));
  it("returns 0 for an empty array", () => expect(sum([])).toBe(0));
});
```

```js
// same idea with the built-in runner: node --test
import test from "node:test";
import assert from "node:assert/strict";
import { sum } from "./sum.js";

test("sum adds numbers", () => assert.equal(sum([1, 2, 3]), 6));
```

Common mistake: testing implementation details (private variables) instead of behaviour, or writing one giant test with many asserts.

Interview questions:

- What makes a good unit test? What is the difference between unit and integration tests?
- How do you test an async function? How do you mock `fetch`?
- What is a test double (mock, stub, spy)?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Language core | Variables, types, operators, control flow | [MDN: JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide), [MDN: data types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures), [MDN: equality](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness) | [JavaScript Crash Course For Beginners (Traversy Media, English)](https://www.youtube.com/watch?v=hdI2bqOjy3c) and Hindi: [Chai aur Javascript playlist (Chai aur Code, Hindi)](https://www.youtube.com/playlist?list=PLu71SKxNbfoBuX3f4EOACle2y-tRC5Q37) | Beginner | 3 h | Do 10 coercion puzzles and explain each |
| Functions and closures | Scope, arrows, closures, HOF | [MDN: Functions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions), [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures), [javascript.info: closure](https://javascript.info/closure) | Hindi short lessons: [Let, const and var ki kahani](https://www.youtube.com/watch?v=yY0bKZNYmJs) and [IIFE](https://www.youtube.com/watch?v=GAIbn16Iytc) (Chai aur Code) | Intermediate | 3 h | Build debounce, once, memoize from scratch |
| Arrays and objects | Destructuring, spread, map/filter/reduce, immutability | [MDN: Working with objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects), [MDN: reduce](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce) | No video verified for this topic; use the official documentation above. | Beginner | 3 h | Solve 15 array tasks (group, count, dedupe, flatten) without loops |
| this and classes | this rules, bind, prototype, class | [MDN: this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this), [MDN: prototype chain](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain), [MDN: Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Write 6 snippets that show each `this` rule |
| Modules | ESM, CJS, dynamic import | [MDN: Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules) | No video verified for this topic; use the official documentation above. | Beginner | 1.5 h | Convert a small CJS project to ESM |
| Errors | try/catch/finally, custom errors | [MDN: control flow and error handling](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Create a typed `HttpError` and use it in a fetch wrapper |
| Async and event loop | Promises, async/await, event loop, microtasks | [MDN: Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises), [MDN: execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop), [javascript.info: event loop](https://javascript.info/event-loop) | [What the heck is the event loop anyway? (Philip Roberts, JSConf EU, English)](https://www.youtube.com/watch?v=8aGhZQkoFbQ) | Intermediate | 3 h | Predict and verify the output of 8 ordering puzzles |
| Concurrency and fetch | all, allSettled, race, fetch errors, abort | [MDN: Promise.allSettled](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled), [MDN: Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [javascript.info: async](https://javascript.info/async) | [Fetch API Introduction (Traversy Media, English)](https://www.youtube.com/watch?v=Oive66jrwBs) | Intermediate | 2.5 h | Write `request()` with timeout and `ok` check; load 20 URLs, 5 at a time |
| Debugging and memory | DevTools, breakpoints, leaks | [Chrome DevTools](https://developer.chrome.com/docs/devtools), [MDN: JS debugging](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Debugging_JavaScript), [MDN: Memory management](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Find a leaked listener using the Memory tab |
| Testing basics | node:test, Vitest | [Node test runner](https://nodejs.org/api/test.html), [Vitest guide](https://vitest.dev/guide/) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | Write 10 tests for your Phase 1 utility functions |

## Verification notes

- As in Phase 0, youtube.com oEmbed was unreachable from my environment. Titles and channels were verified through `noembed.com` (which proxies YouTube oEmbed). Durations were NOT verified for any video below.
- Philip Roberts `8aGhZQkoFbQ`: title "What the heck is the event loop anyway? | Philip Roberts | JSConf EU", channel JSConf. English (not formally verified). A search summary said it is roughly 26 to 30 minutes; I did not confirm this. The talk is from 2014. The core model is still correct, but it explains the browser; Node's phases are described in the Node docs.
- Traversy Media `hdI2bqOjy3c`: title "JavaScript Crash Course For Beginners", channel Traversy Media. Listed in freeCodeCamp's JavaScript course roundup. Upload year and length not verified; check for outdated style (some older crash courses still show `var`).
- Traversy Media `Oive66jrwBs`: title "Fetch API Introduction", channel Traversy Media. Older video. The `fetch` basics are stable; it may not show `AbortSignal.timeout`, so use the MDN page for that.
- Chai aur Code: `yY0bKZNYmJs` ("Let, const and var ki kahani | chai aur #javascript") and `GAIbn16Iytc` ("Immediately Invoked Function Expressions IIFE | chai aur #javascript") have channel "Chai aur Code" from the oEmbed data, and appeared on the playlist listing page I opened. The titles are in Hinglish (Hindi written in English letters), so I label the language Hindi/Hinglish. The playlist page title I fetched is "Chai aur Javascript | हिन्दी". I could not read the playlist's channel name or video count directly from YouTube; one aggregator listed 25 videos (not verified). Quality of the whole series was not reviewed; use it as an optional Hindi companion, not as the main source.
- All MDN, javascript.info, Node, Vitest and Chrome DevTools links returned HTTP 200 on 2026-10-09.
- Only one overlapping video is recommended per topic. I did not find a verified, good video for `this` and prototypes, so I rely on MDN and javascript.info.

## Hands-on exercises

1. **Coercion quiz.** Predict 12 expressions (`[] + {}`, `"5" * "2"`, `null ?? 1`, `0 || "x"`) and then run them.
2. **Closure toolkit.** Implement `once(fn)`, `memoize(fn)`, `debounce(fn, ms)`, `throttle(fn, ms)`. Write tests.
3. **Array kata.** Without loops: group orders by status, count words, flatten and dedupe, find the top 3 by total.
4. **Immutable update.** Write `updateNested(state, path, value)` that returns a new object and never mutates the old.
5. **This lab.** Write five snippets where `this` is: object method, detached method, arrow in method, `bind`, and a class method passed as callback. Fix the broken ones.
6. **Event loop puzzles.** Write 8 snippets mixing `setTimeout`, promises, `await`, and `queueMicrotask`. Predict, run, and explain.
7. **Resilient fetch.** Write `request()` (timeout, `res.ok`, JSON parse error handling, abort). Test it against `https://jsonplaceholder.typicode.com` including a 404 path.
8. **Concurrency pool.** Write `mapLimit(items, limit, fn)` that runs at most `limit` promises at once. Compare with `Promise.all`.
9. **Module swap.** Take one CJS file set and convert it to ESM. Note what broke.
10. **Test it.** Add `vitest` or `node --test` to the utilities and reach 90% of your functions covered by at least one meaningful test.
11. **DevTools hunt.** Create a page with a leaking listener and a slow function. Find both using the Memory and Performance tabs.

## Checkpoint

**Explain:**

- The event loop, with a drawing: stack, Web APIs, microtask queue, task queue.
- Why `this` is `undefined` after `const f = obj.method; f()`.
- Why `fetch` does not reject for HTTP 500 and what you do about it.

**Modify code:** Take the Closure toolkit `debounce` and add a `cancel()` method and a "leading edge" option.

**Debug:** This code logs `[undefined, undefined]`. Fix it in two ways.

```js
const ids = [1, 2];
const users = [];
ids.forEach(async (id) => {
  const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
  users.push((await res.json()).name);
});
console.log(users);
```

(Hint: the array is printed before the awaits finish. Use `Promise.all(ids.map(...))`, or a `for...of` loop with `await`.)

**Write tests:** Write 5 tests for `mapLimit`: order of results, limit respected, empty array, one rejection, and a limit larger than the array.

**Ready to move on when:**

- You pass the Phase 1 skip test items without notes.
- You can explain closures, `this` and the event loop to a friend using a drawing.
- You have a `js-fundamentals` repo with utilities and passing tests.

## Week plan

### Week 2 — JavaScript gap-fill: closures, this, event loop, async, modules, testing (estimated hours: 9)

**Learning objectives**

- Predict how async code is ordered using the event loop model.
- Use closures, `this`, and classes correctly and explain the bugs they cause.
- Handle HTTP and network errors correctly with `fetch`.
- Control concurrency with `Promise.all`, `allSettled`, and a limit.
- Write and run basic JavaScript tests.

**Topics and subtopics**

- **[Must learn now]** Types, references, coercion, `??` vs `||` (quick pass; 1 h)
- **[Must learn now]** Functions, scope, closures, higher-order functions
- **[Must learn now]** Array methods and immutable updates; destructuring, spread, rest, optional chaining
- **[Must learn now]** `this`, bind, prototype, classes
- **[Must learn now]** Modules: ESM vs CJS
- **[Must learn now]** Errors, Promises, async/await
- **[Must learn now]** Event loop, microtasks, tasks
- **[Must learn now]** `Promise.all`, `allSettled`, `race`; fetch and error handling
- **[Must learn now]** DevTools debugging and basic tests
- **[Learn during projects]** Memory leaks, performance profiling
- **[Learn later if needed]** Generators, Proxies, WeakMap, Web Workers

**Small prerequisite concepts**

- What a "stack" and a "queue" are (last-in-first-out versus first-in-first-out).
- What "synchronous" and "asynchronous" mean (wait, or carry on and come back).
- What a "side effect" is (anything a function does besides returning a value).

**Reading**

- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures)
- [MDN: this](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this)
- [MDN: Using promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises)
- [MDN: JavaScript execution model](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop)
- [javascript.info: Event loop](https://javascript.info/event-loop)
- [MDN: Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [Vitest guide](https://vitest.dev/guide/)

**Video**

- "What the heck is the event loop anyway? | Philip Roberts | JSConf EU", JSConf, English, duration not verified: [watch](https://www.youtube.com/watch?v=8aGhZQkoFbQ)
- "Fetch API Introduction", Traversy Media, English, duration not verified: [watch](https://www.youtube.com/watch?v=Oive66jrwBs)
- Optional Hindi/Hinglish: "Let, const and var ki kahani", Chai aur Code, duration not verified: [watch](https://www.youtube.com/watch?v=yY0bKZNYmJs) and the playlist [Chai aur Javascript](https://www.youtube.com/playlist?list=PLu71SKxNbfoBuX3f4EOACle2y-tRC5Q37) (duration not verified)

**Hands-on exercises**

1. Do exercises 1 and 2 (coercion quiz, closure toolkit) on day 1.
2. Do exercises 3 and 4 (array kata, immutable update).
3. Do exercises 5 and 6 (this lab, event loop puzzles), then watch the event loop talk.
4. Do exercises 7 and 8 (resilient fetch, concurrency pool).
5. Do exercises 9 and 10 (module swap, tests). Keep 1 h for the DevTools hunt (exercise 11) if time allows.

**What you must build**

A repo `js-fundamentals` with: `src/` containing `once`, `memoize`, `debounce`, `throttle`, `request`, `mapLimit`, `updateNested`; a `test/` folder with at least 15 passing tests; a `PUZZLES.md` with your 8 event loop puzzles and written explanations.

**Completion checklist**

- [ ] Closure toolkit written and tested
- [ ] Can explain `this` rules with examples
- [ ] Event loop puzzles all predicted correctly (or understood after the miss)
- [ ] `request()` handles timeout, 404, and network error
- [ ] `mapLimit` limits concurrency, with a test
- [ ] Tests run with one command (`npm test`)
- [ ] Phase 1 checkpoint passed

**Self-test**

1. What is printed by a script with `setTimeout(0)`, a `.then`, and sync logs, and why?
2. What is the difference between `Promise.all` and `Promise.allSettled`?
3. What does a closure capture, and how does that cause a stale value in React?
4. Why does `fetch("/missing")` not throw?
5. How do you convert a CJS file to ESM?

**Common mistakes**

- Memorising event loop output without understanding the two queues.
- `forEach(async ...)` and `await` in loops for independent work.
- Mutating objects that React or Redux treats as state.
- Forgetting `res.ok`, or reading the body twice.
- Writing tests that only test the happy path.

**Ready to continue when**

- You can predict the order for a new async snippet you have never seen.
- Your `js-fundamentals` tests are green on a fresh clone.
- You can explain `this`, closures, and the event loop without notes.

**Slower-track option**

Stretch to 1.5 weeks. Cut: classes and prototypes (come back during Node), `race`/`any`, memory profiling. Do not cut: closures, event loop, fetch error handling, async/await, tests. If the assessment showed JavaScript is strong (5/5), compress this week to 4 hours: do only the event loop puzzles, `mapLimit`, and the tests.


# Phase 2 — TypeScript

## Why this phase matters

TypeScript (TS) is JavaScript plus a type checker that runs *before* your code runs. It catches typos, missing fields, and "undefined is not a function" bugs in your editor. Almost every serious React, Next.js, Node, and AI SDK codebase today uses it, so you will meet it in job interviews and in the docs of the tools you use. It does not replace testing, and it does not check data that arrives at runtime (an API can still send the wrong shape). This phase gives you the 20 percent of TS that covers 90 percent of daily work.

## Prerequisites and "skip test"

You can skip a topic if you can DEMONSTRATE it:

- Create a TS project from scratch (`npm init`, install `typescript`, create a `tsconfig.json`, compile or run a file) without a template.
- Type a `fetch` wrapper `request<T>(url): Promise<T>` and use it with an `interface User`.
- Write a discriminated union for `{ status: "loading" } | { status: "error"; message: string } | { status: "success"; data: T }` and narrow it in a `switch`.
- Type a React component with props, `useState<User | null>`, an `onChange` handler, and a custom hook.
- Explain in one sentence each: `unknown` vs `any`, `interface` vs `type`, and `never`.

> **Honest note:** If you already use TS daily at work, you may still hold gaps in generics, narrowing, and `tsconfig`. Do the checkpoint at the end before you skip.

> **Outdated?:** TypeScript 7.0 (the compiler rewritten in Go) was released in July 2026, and the npm `latest` tag was 7.0.2 when I checked on 2026-10-09. The language you write is the same. The InfoQ report says the main practical changes are speed, `strict` on by default, and old deprecated options now being errors; some tools that need the compiler's programmatic API (for example typescript-eslint and some framework tooling) wait for 7.1, and a compatibility package `@typescript/typescript6` exists. Most tutorials and videos (including the Net Ninja series below) were made on older versions, so treat the **language** parts as correct and check the official docs and your `tsconfig` for **configuration** details.

## Concepts explained

### Why TypeScript exists

**[Must learn now]** JavaScript checks types only when the code runs, so `user.nmae` fails in front of your users. TypeScript reads your code, understands the shapes of data, and shows red lines in the editor. TS is **erased** at build time: the browser or Node runs plain JavaScript. Types cost nothing at runtime.

Analogy: a spell-checker and a building inspector that visit before the shop opens.

```ts
type User = { id: number; name: string };

function greet(user: User): string {
  return `Hi ${user.name}`;
}

greet({ id: 1, name: "Asha" });   // ok
// greet({ id: "1", name: "Asha" }); // error: string is not assignable to number
// greet({ id: 1, nmae: "Asha" });   // error: typo caught at edit time
```

Common mistake: thinking TS validates API data. It does not. If the server sends `id` as a string, your code still runs with the wrong value. Validate at the edge (a schema library such as Zod is common; you meet it in later phases).

Interview questions:

- What does TypeScript do at compile time, and what does it do at runtime?
- Does TypeScript make your app faster or safer at runtime? Explain.
- What is "structural typing"? (Shape matters, not the name.)

### Type inference vs explicit types

**[Must learn now]** TS often guesses types for you (**inference**). Let it guess for local variables. Write types yourself on function **parameters**, **exported function returns**, and public data shapes.

```ts
const count = 5;                  // inferred: number
const names = ["a", "b"];         // inferred: string[]
let value;                        // implicit any if you do not assign: avoid

function add(a: number, b: number) {  // params: explicit; return inferred as number
  return a + b;
}

const point = { x: 1, y: 2 } as const; // readonly { x: 1; y: 2 }, literal types
```

Common mistake: annotating everything (`const count: number = 5`). It is noise and can hide better inferred types.

Interview questions:

- When should you write a type annotation, and when should you rely on inference?
- What does `as const` do?

### Primitive, array, tuple, object, and function types

**[Must learn now]**

```ts
let id: number = 1;
let title: string = "x";
let done: boolean = false;
let big: bigint = 10n;

const ids: number[] = [1, 2];          // same as Array<number>
const pair: [string, number] = ["age", 30]; // tuple: fixed length and order

const user: { id: number; name: string; email?: string } = { id: 1, name: "A" };

type Compare = (a: number, b: number) => number;
const asc: Compare = (a, b) => a - b;

function log(msg: string, level: "info" | "warn" = "info"): void {
  console[level](msg);
}
```

Tuples appear in React: `useState` returns `[value, setter]`.

Common mistake: using `Object`, `Function`, or `{}` as types. They are too loose. Describe the shape instead.

Interview questions:

- Array vs tuple?
- How do you type a function that takes a callback?
- Why is `void` different from `undefined` as a return type?

### Interfaces vs type aliases; optional and readonly

**[Must learn now]** Both describe object shapes. `interface` can be extended and merged (declaration merging), and is nice for objects and class contracts. `type` can describe anything: unions, tuples, primitives, mapped types. A practical rule: **use `type` by default for unions and utilities; use `interface` for public object shapes you extend**. Be consistent inside a project. `?` makes a property optional; `readonly` stops reassignment (compile-time only).

```ts
interface BaseEntity { readonly id: number; createdAt: string }
interface Order extends BaseEntity { total: number; note?: string }

type Status = "pending" | "paid" | "cancelled";
type OrderWithStatus = Order & { status: Status };

const o: OrderWithStatus = { id: 1, createdAt: "2026-10-09", total: 500, status: "paid" };
// o.id = 2; // error: readonly
```

Common mistake: marking everything optional (`?`) to silence errors. Then every use needs checks and the type tells you nothing.

Interview questions:

- `interface` vs `type`: differences and when you pick which?
- Does `readonly` stop mutation at runtime?
- What is declaration merging?

### Union and intersection types; literal types; discriminated unions

**[Must learn now]** A **union** `A | B` means "one of these". An **intersection** `A & B` means "all of these combined". **Literal types** are exact values (`"paid"`, `404`). A **discriminated union** is a union where each member has a common literal field (the *tag*), so TS can tell them apart. This is the best way to model loading, error, and success states, and API results.

```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "success"; data: T };

function render(s: RequestState<string[]>) {
  switch (s.status) {
    case "idle":
    case "loading":
      return "Loading...";
    case "error":
      return `Error: ${s.message}`;   // s is narrowed: message exists
    case "success":
      return s.data.join(", ");        // data exists here
    default: {
      const _exhaustive: never = s;    // compile error if a case is missing
      return _exhaustive;
    }
  }
}
```

Common mistake: modelling this as `{ loading: boolean; error?: string; data?: T }`. It allows impossible states such as `loading: true` with data and an error.

Interview questions:

- What is a discriminated union and why use it for UI state?
- How does the `never` trick give you exhaustive `switch` checks?
- Union vs intersection: give an example of each.

### Narrowing and type guards

**[Must learn now]** **Narrowing** means TS gets smarter inside a branch. Tools: `typeof`, `instanceof`, `in`, equality checks, truthiness checks, discriminant checks, and **custom type guards** (`value is T`).

```ts
function len(x: string | string[]) {
  if (typeof x === "string") return x.length;  // string here
  return x.length;                              // string[] here
}

type Cat = { meow: () => void };
type Dog = { bark: () => void };
const isCat = (a: Cat | Dog): a is Cat => "meow" in a;

function speak(a: Cat | Dog) {
  if (isCat(a)) a.meow();
  else a.bark();
}

function isUser(v: unknown): v is { id: number; name: string } {
  return typeof v === "object" && v !== null && "id" in v && "name" in v;
}
```

Common mistake: using `as User` to "force" a type on unknown data. It is a promise to the compiler that you cannot keep. Narrow or validate instead.

Interview questions:

- What are type guards? Write one.
- What does `a is Cat` mean?
- Why is `as` called a "type assertion" and not a conversion?

### Generics

**[Must learn now]** A generic is a type with a blank to fill in, like a function parameter but for types. Use it when the same logic works for many types and the output type depends on the input type.

Analogy: a lunch box. The box code is the same, but you decide at use time if it holds rice or rotis.

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const n = first([1, 2, 3]);       // number | undefined
const s = first(["a", "b"]);      // string | undefined

async function request<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return (await res.json()) as T;  // trust boundary: validate if data is untrusted
}
type Todo = { id: number; title: string; completed: boolean };
const todo = await request<Todo>("https://jsonplaceholder.typicode.com/todos/1");

function pluck<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

Constraints (`extends`) say what a type parameter must look like. Defaults (`<T = string>`) exist too.

Common mistake: over-generic code, such as `<T>(x: T) => x` everywhere. If the function does not relate input and output types, you do not need a generic.

Interview questions:

- What problem do generics solve? Give a small example.
- What does `K extends keyof T` mean?
- Why is `request<Todo>` not a runtime guarantee?

### Utility types

**[Must learn now]** Built-in helpers that transform types: `Partial<T>` (all optional), `Required<T>`, `Readonly<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `ReturnType<F>`, `Parameters<F>`, `Awaited<T>`, `NonNullable<T>`. Also `keyof` and `typeof` in type positions.

```ts
type User = { id: number; name: string; email: string; password: string };

type PublicUser = Omit<User, "password">;
type UserPatch = Partial<Pick<User, "name" | "email">>;
type ById = Record<number, User>;

async function getUser() { return { id: 1, name: "A" }; }
type U = Awaited<ReturnType<typeof getUser>>; // { id: number; name: string }

const ROLES = ["admin", "user"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "user"
```

Common mistake: re-typing the same shape by hand in five places. Derive types from one source.

Interview questions:

- `Pick` vs `Omit`?
- How do you make an update payload type from a full model?
- How do you get a union type from an array of strings?

### Enums and alternatives

**[Learn during projects]** TS has `enum`, but it generates real runtime code and has some quirks (numeric enums accept any number in older versions). Many teams use **union of string literals** or an `as const` object. Use these first; use `enum` only if your team already does.

```ts
// Alternative 1: string union
type Status = "pending" | "paid" | "cancelled";

// Alternative 2: const object + derived type
const Status2 = { Pending: "pending", Paid: "paid" } as const;
type Status2 = (typeof Status2)[keyof typeof Status2];

// enum, for reference
enum Color { Red = "RED", Green = "GREEN" }
```

Common mistake: mixing enums from different packages and getting "not assignable" errors for identical-looking values.

Interview questions:

- Why do many teams avoid `enum`?
- How do you create a union type from an object's values?

### unknown, any, never, void

**[Must learn now]** `any` turns the checker off (avoid). `unknown` means "could be anything, so prove it before use" (use for untrusted data, `catch` variables, `JSON.parse` results). `never` means "this cannot happen" (functions that always throw, impossible branches). `void` means "returns nothing useful".

```ts
function parse(text: string): unknown {
  return JSON.parse(text);
}
const data = parse('{"id":1}');
// data.id;                       // error: unknown
if (typeof data === "object" && data !== null && "id" in data) {
  console.log((data as { id: number }).id);
}

try {
  throw new Error("x");
} catch (err) {            // err is unknown (with strict settings)
  if (err instanceof Error) console.log(err.message);
}

function fail(msg: string): never { throw new Error(msg); }
```

Common mistake: sprinkling `any` to "fix" errors. One `any` leaks: values derived from it also become `any`.

Interview questions:

- `any` vs `unknown`?
- When is a function's return type `never`?
- How should you type a caught error?

### Null safety

**[Must learn now]** With `strictNullChecks` (part of `strict`), `null` and `undefined` are not allowed in a type unless you add them. This forces you to handle "might be missing" cases and removes the most common runtime crash.

```ts
function findUser(users: { id: number; name: string }[], id: number) {
  return users.find((u) => u.id === id); // type: {...} | undefined
}
const u = findUser([], 1);
// console.log(u.name);          // error: possibly undefined
console.log(u?.name ?? "Guest"); // ok
if (u) console.log(u.name);      // ok: narrowed

const el = document.querySelector("#app");
// el!.textContent = "x";        // "!" says "trust me": avoid unless truly sure
```

Common mistake: the non-null assertion `!` everywhere. It hides the same bug TS wanted to show you.

Interview questions:

- What does `strictNullChecks` do?
- `?.` vs `!` vs `??`: explain each.

### Typing API responses and errors

**[Must learn now]** Model what the server returns, including errors. Keep a separate type for the *wire* shape (what JSON contains) and your *domain* shape if they differ (for example, dates as strings). For unknown data, validate (with a schema library) and then derive the type from the schema.

```ts
type ApiOk<T> = { ok: true; data: T };
type ApiErr = { ok: false; status: number; message: string };
type ApiResult<T> = ApiOk<T> | ApiErr;

async function getJson<T>(url: string): Promise<ApiResult<T>> {
  try {
    const res = await fetch(url);
    if (!res.ok) return { ok: false, status: res.status, message: res.statusText };
    return { ok: true, data: (await res.json()) as T };
  } catch (e) {
    return { ok: false, status: 0, message: e instanceof Error ? e.message : "Network error" };
  }
}

const r = await getJson<{ id: number; title: string }>("https://jsonplaceholder.typicode.com/todos/1");
if (r.ok) console.log(r.data.title);
else console.error(r.status, r.message);
```

Common mistake: typing the response as `User` while the endpoint can return `null` or an error object. Your type is a lie, and the crash comes later.

Interview questions:

- How would you type an API that returns either data or an error?
- Where is the "trust boundary" in a typed app, and how do you protect it?

### Typing React props, state, events, and custom hooks

**[Must learn now]** The React docs have a TypeScript page (linked below). Key patterns:

```tsx
import { useState, type ChangeEvent, type ReactNode } from "react";

type ButtonProps = {
  label: string;
  onClick: () => void;
  variant?: "primary" | "ghost";
  children?: ReactNode;
};

export function Button({ label, onClick, variant = "primary" }: ButtonProps) {
  return <button className={variant} onClick={onClick}>{label}</button>;
}

type User = { id: number; name: string };

export function UserForm() {
  const [user, setUser] = useState<User | null>(null);      // union with null
  const [name, setName] = useState("");                      // inferred string

  const onChange = (e: ChangeEvent<HTMLInputElement>) => setName(e.target.value);
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setUser({ id: 1, name });
  };

  return (
    <form onSubmit={onSubmit}>
      <input value={name} onChange={onChange} />
      <p>{user?.name}</p>
    </form>
  );
}

// custom hook, generic and typed
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  // effect with AbortController goes here (Phase 4)
  return { data, error, loading } as const;
}
```

Common mistake: `useState([])` infers `never[]`. Write `useState<Todo[]>([])`.

Interview questions:

- How do you type props with children? With a callback prop?
- Why does `useState<User | null>(null)` need the generic?
- What type does an `onChange` handler event have for an `input`?

### Typing async functions

**[Must learn now]** An `async` function returns `Promise<T>`. Annotate the `T`. `Promise.all` with a tuple of promises gives a tuple of results. Use `Awaited<>` to unwrap.

```ts
async function loadAll(): Promise<[User, Todo[]]> {
  const [user, todos] = await Promise.all([
    request<User>("https://jsonplaceholder.typicode.com/users/1"),
    request<Todo[]>("https://jsonplaceholder.typicode.com/todos?userId=1"),
  ]);
  return [user, todos];
}
```

Common mistake: annotating the return as `User` instead of `Promise<User>` on an async function (TS will complain; the fix is `Promise<User>`).

Interview questions:

- What is the return type of an async function that returns a number?
- How do you type the result of `Promise.all`?

### tsconfig and compiler errors

**[Must learn now]** `tsconfig.json` tells TS how strict to be and how to find files. Key options: `strict` (turn on; includes strict null checks), `target` and `lib` (which JS features exist), `module` and `moduleResolution` (how imports work, must match your bundler or Node ESM), `jsx` (React), `noEmit` (only type-check, used with Vite and Next.js), `paths` (import aliases), `skipLibCheck` (speeds up checks), `include`/`exclude`. Next.js and Vite templates generate a good base file; learn to read it, do not hand-tune on day one.

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "jsx": "react-jsx",
    "strict": true,
    "noEmit": true,
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src"]
}
```

Reading errors: read the *last* line of a long TS error first (it names the real mismatch), then work upward. Hover types in VS Code. Commands: `npx tsc --noEmit` to type-check.

Common mistake: setting `strict: false` to get rid of errors on a new project. You lose most of the benefit.

Interview questions:

- Which `tsconfig` options matter most? Why `strict`?
- What does `noEmit` do and why would a Vite or Next.js project use it?
- How do you migrate a JS project to TS gradually (`allowJs`, `checkJs`)?

### Project organization

**[Learn during projects]** Keep shared types near their use. Put domain types in a `types/` file or next to the feature (`features/orders/types.ts`). Export API types from one place. Use path aliases to avoid `../../../`. Name types in `PascalCase`. Do not create a giant `types.ts` for everything. Use `import type { X }` for type-only imports.

Common mistake: duplicate type definitions for the same API object in the frontend and backend. Share one source when you can, or generate types from an OpenAPI schema (you will meet FastAPI's OpenAPI later).

Interview questions:

- Where do you keep API types in a React app?
- What does `import type` do?

### Essential vs can wait

- **Essential now:** basic types, inference, `interface`/`type`, unions, literal types, narrowing, generics (basic), `unknown`, strict null checks, utility types (`Partial`, `Pick`, `Omit`, `Record`), typing React props/state/events, `tsconfig` basics.
- **Learn during projects:** discriminated unions in real states, typing API results, enum alternatives, project organization, `as const`.
- **Learn later if needed:** conditional types (`T extends U ? X : Y`), mapped types, template literal types, `infer`, declaration files (`.d.ts`), decorators, advanced generics, type-level programming.

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Basics and why TS | Inference, primitives, arrays, tuples, objects | [TS Handbook intro](https://www.typescriptlang.org/docs/handbook/intro.html), [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html), [Object types](https://www.typescriptlang.org/docs/handbook/2/objects.html) | [TypeScript Tutorial playlist (Net Ninja, English)](https://www.youtube.com/playlist?list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI) | Beginner | 3 h | Convert 3 small JS utilities to TS |
| Fast alternative | One-hour overview | Same handbook pages | [Learn TypeScript - Crash Course for Beginners (freeCodeCamp, English)](https://www.youtube.com/watch?v=ZvZ7gvcmPmI) | Beginner | 1 h | Use only if you want one quick video instead of the playlist |
| Narrowing and unions | Unions, literals, guards, discriminated unions | [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Model `RequestState<T>` and render it exhaustively |
| Generics and utility types | Generics, constraints, Partial, Pick, Omit, Record | [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html), [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html), [Types from types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2.5 h | Write a typed `request<T>` and a typed `pluck` |
| Enums | Enum quirks and alternatives | [Enums](https://www.typescriptlang.org/docs/handbook/enums.html) | No video verified for this topic; use the official documentation above. | Beginner | 0.5 h | Replace an enum with a union and an `as const` object |
| tsconfig | strict, module, jsx, paths | [tsconfig handbook](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html), [TSConfig reference](https://www.typescriptlang.org/tsconfig/) | No video verified for this topic; use the official documentation above. | Intermediate | 1 h | Create a strict config from scratch and fix the errors |
| TS in React | Props, state, events, hooks | [React: Using TypeScript](https://react.dev/learn/typescript) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Type a form component and a `useFetch<T>` hook |

## Verification notes

- youtube.com oEmbed was unreachable from my environment. I verified titles and channels with `noembed.com` (a proxy for YouTube oEmbed). Durations were NOT verified.
- Net Ninja playlist `PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI`: the fetched playlist page title is "TypeScript Tutorial". I could not read the channel name or video count from the playlist page. I confirmed the channel indirectly: video `2pZmKW9-I_k` (a member of that playlist, as shown by a GitHub README link containing the same `list=` ID) has title "TypeScript Tutorial #1 - Introduction & Setup" and channel "Net Ninja". Class Central describes the series as 21 episodes; I did not verify that count. This series is older (made well before TS 7), so use it for language basics only.
- freeCodeCamp `ZvZ7gvcmPmI`: title "Learn TypeScript - Crash Course for Beginners", channel freeCodeCamp.org. A freeCodeCamp article titled "Learn TypeScript in 1 hour" embeds this ID; a search snippet said the instructor is Muhammad Omar Al Najjar. Duration of about 1 hour comes from the article title and was not verified from the video.
- I did not find a verified, good Hindi TypeScript video. A Class Central page lists a Hindi TypeScript series, but I could not confirm its creator or quality, so I do not include it.
- TypeScript 7 facts come from an InfoQ article I fetched ("typescript-7-released") and the npm registry `dist-tags` (latest 7.0.2). Check the official TypeScript release notes before upgrading a project.
- All TypeScript handbook and React docs links returned HTTP 200 on 2026-10-09. Several are client-rendered; I confirmed status, not every heading.

## Hands-on exercises

1. **Hello strict.** Make a new folder, `npm init -y`, `npm i -D typescript`, `npx tsc --init`, set `strict: true`, write a file with three type errors and fix them.
2. **Convert utilities.** Take your Phase 1 `js-fundamentals` functions (`debounce`, `memoize`, `mapLimit`, `request`) and add types. `request<T>` and `mapLimit<T, R>` need generics.
3. **State machine.** Write `RequestState<T>` as a discriminated union and a `render()` function with an exhaustive `switch` using `never`.
4. **Narrowing lab.** Write a function `parseUser(input: unknown): User` that validates by hand and throws a clear error. Then compare with how a schema library would do it (read its docs only).
5. **Utility types.** From one `Order` type, derive `OrderSummary` (Pick), `CreateOrderInput` (Omit id, createdAt), `UpdateOrderInput` (Partial), and `OrdersById` (Record).
6. **React typing.** In a Vite React TS template, type a `SearchableList<T>` generic component with a `renderItem` prop and a `useFetch<T>` hook.
7. **Error reading.** Introduce 6 type errors in a file (wrong generic, missing property, possibly undefined, wrong union member, wrong event type, wrong return). Read each from the last line up, and write the cause in one sentence.
8. **Strict migration.** Take a tiny JS file, rename to `.ts`, and clear errors without using `any` or `!`.

## Checkpoint

**Explain:**

- `unknown` vs `any` and when a caught error should be treated as `unknown`.
- Why a discriminated union is better than `{ loading, error?, data? }`.
- What the compiler checks and what it cannot know (runtime API data).

**Modify code:** Given `type User = { id: number; name: string; email: string }`, write a type for a "create user" input that has no `id` and an optional `email`.

**Debug:** Fix this without `any` and without `!`.

```ts
const input = document.querySelector("#name");
console.log(input.value);

function total(items: { price: number }[] | undefined) {
  return items.reduce((s, i) => s + i.price, 0);
}
```

(Hint: `querySelector<HTMLInputElement>` plus a null check; and `items?.reduce(...) ?? 0` or an early return.)

**Write tests:** Write Vitest tests for `parseUser` covering valid input, a missing field, a wrong type, and `null`. Also run `npx tsc --noEmit` and make it pass.

**Ready to move on when:**

- You can create a strict TS project from scratch and read common errors.
- You have typed utilities, a generic `request<T>`, and a typed React component/hook.
- You can explain the difference between compile-time safety and runtime validation.

## Week plan

### Week 3 — TypeScript (estimated hours: 9)

**Learning objectives**

- Write and read everyday TypeScript with strict settings.
- Model states with unions and narrowing.
- Use generics and utility types in real code.
- Type React components, hooks, events, and async API calls.
- Read `tsconfig` and fix compiler errors confidently.

**Topics and subtopics**

- **[Must learn now]** Why TS, inference vs annotations, basic types
- **[Must learn now]** `interface` vs `type`, optional, readonly
- **[Must learn now]** Unions, intersections, literal types, discriminated unions
- **[Must learn now]** Narrowing and type guards
- **[Must learn now]** `unknown`, `any`, `never`, `void`, null safety
- **[Must learn now]** Generics and utility types
- **[Must learn now]** Typing API responses, errors, async functions
- **[Must learn now]** Typing React props, state, events, custom hooks
- **[Must learn now]** `tsconfig` basics
- **[Learn during projects]** Enum alternatives, project organization, `as const`
- **[Learn later if needed]** Conditional, mapped, and template literal types; `infer`; `.d.ts` files

**Small prerequisite concepts**

- The difference between "compile time" (before running) and "runtime" (while running).
- What a "build step" is (tools turn TS into JS, just like Vite or Next.js do for JSX).
- What `npx tsc --noEmit` does (check only, write nothing).

**Reading**

- [TypeScript Handbook intro](https://www.typescriptlang.org/docs/handbook/intro.html)
- [Everyday Types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [Utility Types](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [TSConfig reference](https://www.typescriptlang.org/tsconfig/)
- [React: Using TypeScript](https://react.dev/learn/typescript)

**Video**

- "TypeScript Tutorial" playlist (starts with "#1 - Introduction & Setup"), Net Ninja, English, duration not verified: [playlist](https://www.youtube.com/playlist?list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI)
- Optional fast alternative: "Learn TypeScript - Crash Course for Beginners", freeCodeCamp.org, English, about 1 hour per article (duration not verified): [watch](https://www.youtube.com/watch?v=ZvZ7gvcmPmI)

**Hands-on exercises**

1. Exercises 1 and 2 (hello strict, convert utilities) on days 1-2.
2. Exercises 3 and 4 (state machine, narrowing lab).
3. Exercise 5 (utility types) and exercise 7 (error reading).
4. Exercise 6 (React typing) with a Vite React TS template.
5. Exercise 8 (strict migration) and the checkpoint.

**What you must build**

A repo `ts-toolkit`: your typed utilities from Phase 1, a typed `request<T>` returning `ApiResult<T>`, a `RequestState<T>` module, and a small Vite React TS demo that lists todos from `https://jsonplaceholder.typicode.com/todos` with typed loading, error, and success states. `npx tsc --noEmit` and your tests must pass.

**Completion checklist**

- [ ] Strict TS project created from scratch
- [ ] Utilities converted with generics where needed
- [ ] Discriminated union with exhaustive `switch`
- [ ] No `any` and no `!` in my code (or each use has a comment)
- [ ] React component, event handler, and hook typed
- [ ] Can read my `tsconfig` line by line
- [ ] Phase 2 checkpoint passed

**Self-test**

1. What is the difference between `unknown` and `any`?
2. Why is `useState<User | null>(null)` written like that?
3. How do you make an "update" type from a full model?
4. What does `never` help you check in a `switch`?
5. Why is `res.json() as User` not proof that the data is a `User`?

**Common mistakes**

- Using `any` or `as` to silence errors.
- Turning `strict` off.
- Overusing generics and fancy types too early.
- Believing types validate runtime data.
- Copy-pasting types between files instead of deriving them.

**Ready to continue when**

- `npx tsc --noEmit` passes in your toolkit repo, in strict mode, with no `any`.
- You can explain the checkpoint answers without notes.
- You can open any typed React component and tell what each type means.

**Slower-track option**

Cut: the second video, enum alternatives, project organization, the strict migration exercise. Keep: unions, narrowing, generics, utility types, React typing. If you use TS daily at work and passed the skip test, compress to 4 hours and do only exercises 3, 4, 5, and the checkpoint.


# Phase 3 — HTML, CSS, browser, and web fundamentals

## Why this phase matters

You build UIs in React every day, but React only produces HTML and CSS. Weak HTML gives inaccessible pages; weak CSS gives layout bugs that no component library can fix; weak HTTP knowledge gives mysterious CORS and cookie errors that later hit your Node and FastAPI work. This is a gap-fill week. Skim what you know, and go deep on what the assessment showed you missed. The last section (HTTP status codes, headers, cookies, caching, CORS) matters most for backend work in Phases 6 and 9.

## Prerequisites and "skip test"

You can skip a topic if you can DEMONSTRATE it:

- Build a responsive page (header, nav, main, footer) using only semantic tags, flexbox, and grid, that works from 360px to 1440px wide without horizontal scroll.
- Build an accessible form (labels, errors announced, keyboard-only usable) with native validation.
- Explain specificity with three conflicting rules and fix them without `!important`.
- Use an event delegation handler on a list that adds items dynamically.
- In the Network tab, show a cached response (304 or from disk cache) and explain the `Cache-Control` header.
- Reproduce a CORS error and explain which header fixes it and where it must be set.

## Concepts explained

### Semantic HTML

**[Must learn now]** Semantic tags describe *meaning*: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`, `h1` to `h6`, `ul/ol/li`, `button`, `a`, `time`, `figure`. Screen readers, search engines, and browser features use them. A `button` is focusable, works with Enter and Space, and announces itself as a button. A `div` with an `onClick` does none of that.

Analogy: a building plan with labelled rooms instead of a plain box with walls.

```html
<body>
  <header>
    <nav aria-label="Main">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/orders">Orders</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <h1>Orders</h1>
    <article>
      <h2>Order #42</h2>
      <p>Placed <time datetime="2026-10-09">9 Oct 2026</time></p>
    </article>
  </main>
  <footer><p>Surat, India</p></footer>
</body>
```

Common mistake: `div` soup, skipping heading levels (h1 then h4) for font size, and using `<a>` for actions (use `<button>`) or `<button>` for navigation (use `<a>`).

Interview questions:

- Why use `<button>` instead of `<div onClick>`?
- What is the difference between `<section>` and `<article>`?
- How many `<h1>` should a page have, and why do headings matter?

### Forms, inputs, labels, validation, accessibility

**[Must learn now]** Every input needs a visible `<label>` connected with `for`/`id` (or wrapping). Use the right `type` (`email`, `tel`, `number`, `date`, `password`), `autocomplete`, and native validation (`required`, `minlength`, `pattern`). Group radio buttons in `fieldset` + `legend`. Show errors in text near the field and link them with `aria-describedby`. Never rely on color alone.

```html
<form novalidate>
  <div>
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required autocomplete="email"
           aria-describedby="email-error" />
    <p id="email-error" role="alert"></p>
  </div>
  <fieldset>
    <legend>Plan</legend>
    <label><input type="radio" name="plan" value="free" checked /> Free</label>
    <label><input type="radio" name="plan" value="pro" /> Pro</label>
  </fieldset>
  <button type="submit">Create account</button>
</form>
```

```js
const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  const email = form.elements.email;
  if (!email.checkValidity()) {
    e.preventDefault();
    document.getElementById("email-error").textContent = email.validationMessage;
    email.focus();
  }
});
```

Remember: browser validation helps users, but the **server must validate again**. Anyone can skip your frontend with `curl`.

Common mistakes: placeholder used as a label (it disappears and has poor contrast); `<button>` without `type` inside a form (default is `submit`); removing the focus outline with no replacement.

Interview questions:

- How do you make a form accessible?
- Why must validation also happen on the server?
- What is the difference between `name` and `id` on an input?

### CSS selectors, specificity, inheritance, cascade

**[Must learn now]** The **cascade** decides which rule wins: (1) importance (`!important`), (2) **specificity**, (3) source order (later wins). Specificity is scored like a three-part number: IDs, then classes/attributes/pseudo-classes, then element tags. `#nav` beats `.nav a` beats `nav a`. Some properties are **inherited** (color, font) and some are not (margin, border). Modern CSS also has `:where()` (zero specificity) and `@layer` to control order.

```css
a { color: blue; }                 /* (0,0,1) */
.card a { color: green; }          /* (0,1,1) wins over the one above */
#sidebar .card a { color: red; }   /* (1,1,1) wins */

:where(.card) a { color: teal; }   /* low specificity: easy to override */
```

Keep specificity low and flat: use classes, avoid IDs for styling, avoid `!important`.

Common mistake: fighting specificity with more selectors or `!important`. Fix the structure or use `@layer`.

Interview questions:

- How is specificity calculated? Which wins: `.a .b` or `div.b.c`?
- Which CSS properties are inherited?
- What does `!important` do, and why is it a last resort?

### The box model

**[Must learn now]** Every element is a box: content, padding, border, margin (inside to outside). With `box-sizing: content-box` (the browser default), `width` is only the content; padding and border are added on top. With `border-box`, `width` includes padding and border, which is what you expect. Most projects start with `*, *::before, *::after { box-sizing: border-box; }` (Tailwind's base styles do this for you). Vertical margins can **collapse** (two touching margins merge into the larger one).

```css
.card {
  box-sizing: border-box;
  width: 300px;
  padding: 16px;
  border: 1px solid #ddd;
  margin: 8px;   /* total box is 300px wide, plus 8px margin each side */
}
```

Common mistake: a 100% wide element with padding overflowing its parent because `box-sizing` is `content-box`.

Interview questions:

- Explain `content-box` vs `border-box`.
- What is margin collapsing?
- Padding vs margin: when do you use each?

### Display, positioning, stacking context, overflow

**[Must learn now]** `display`: `block` (full line), `inline` (flows in text, ignores width and height), `inline-block`, `flex`, `grid`, `none`. `position`: `static` (default), `relative` (offset from its own place; also a reference for children), `absolute` (offset from nearest positioned ancestor), `fixed` (relative to viewport), `sticky` (sticks while scrolling). `z-index` only works on positioned (or flex/grid child) elements and only inside its **stacking context**. A new stacking context is created by things like `position` + `z-index`, `opacity < 1`, `transform`, `filter`. A child can never escape its parent's context. `overflow`: `visible`, `hidden`, `auto`, `scroll`. `overflow: hidden` clips and also creates a new block formatting context.

```css
.parent { position: relative; }
.badge  { position: absolute; top: -8px; right: -8px; }   /* sits on parent's corner */

.header { position: sticky; top: 0; z-index: 10; }
.table-wrap { overflow-x: auto; }   /* wide tables scroll inside, page does not */
```

Common mistake: "my modal is behind the header even with z-index: 9999". The modal lives inside a parent with a lower stacking context. Move it out (React portals do this) or fix the parent.

Interview questions:

- Explain `position: relative` vs `absolute`.
- What is a stacking context and what creates one?
- Why does `z-index` sometimes do nothing?

### Flexbox, Grid, responsive design, media queries

**[Must learn now]** **Flexbox** lays items in one direction (a row or a column). Key properties: `display:flex`, `flex-direction`, `justify-content` (main axis), `align-items` (cross axis), `gap`, `flex-wrap`, and `flex: 1` (grow). **Grid** lays items in rows and columns: `grid-template-columns`, `gap`, `repeat(auto-fit, minmax(240px, 1fr))`. Rule of thumb: flex for components (toolbar, card row), grid for page layout and card galleries.

**Responsive design:** start mobile-first, add `min-width` media queries, use fluid units (`%`, `rem`, `vw`, `clamp()`), and include `<meta name="viewport" content="width=device-width, initial-scale=1">`. Container queries let a component react to its own width.

```css
.cards {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); /* responsive without a media query */
}
.toolbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }

.layout { display: grid; grid-template-columns: 1fr; }
@media (min-width: 768px) {
  .layout { grid-template-columns: 240px 1fr; }  /* sidebar appears on wider screens */
}
h1 { font-size: clamp(1.5rem, 4vw, 2.5rem); }
```

Common mistakes: setting fixed pixel widths on layout containers; hiding overflow to hide a layout bug; forgetting `min-width: 0` on a flex child that contains long text (it will not shrink).

Interview questions:

- When do you pick Flexbox over Grid?
- What does `flex: 1` mean?
- What is mobile-first design and why does it help?
- How do `rem`, `em`, `%`, and `vw` differ?

### Typography, spacing, layout systems, reusable styles

**[Must learn now]** Use a small scale for font sizes (for example 12, 14, 16, 20, 24, 32) and spacing (4, 8, 12, 16, 24, 32). Keep line length near 45 to 75 characters, `line-height` about 1.4 to 1.6 for body text, and enough contrast (WCAG: 4.5:1 for normal text). Reuse by classes, components, and tokens, not by copy-paste. A layout system means a consistent container width, gutter, and grid across pages.

```css
:root { --space-1: 4px; --space-2: 8px; --space-4: 16px; --space-6: 24px; }
.container { max-width: 72rem; margin-inline: auto; padding-inline: var(--space-4); }
.stack > * + * { margin-block-start: var(--space-4); }  /* simple vertical rhythm */
```

Common mistake: random pixel values everywhere (13px, 17px, 22px). Use the scale.

Interview questions:

- How do you keep a consistent spacing and type scale in a team?
- What contrast ratio does WCAG AA require for body text?

### CSS variables and design tokens

**[Must learn now]** CSS custom properties (`--name`) hold values you reuse and can change at runtime. **Design tokens** are named design decisions (colors, spacing, radii, font sizes) stored in one place. They make theming (dark mode) easy: change the variables, not every rule.

```css
:root {
  --color-bg: #ffffff;
  --color-text: #111827;
  --color-primary: #2563eb;
  --radius: 8px;
}
@media (prefers-color-scheme: dark) {
  :root { --color-bg: #0b1020; --color-text: #e5e7eb; }
}
[data-theme="dark"] { --color-bg: #0b1020; --color-text: #e5e7eb; }

.btn { background: var(--color-primary); border-radius: var(--radius); color: white; }
```

```js
document.documentElement.dataset.theme = "dark"; // switch theme with one line
```

Common mistake: naming tokens by value (`--blue-500` used for "primary button"). Use meaning names (`--color-primary`) in components.

Interview questions:

- Variables in CSS vs in Sass: what is different? (CSS variables work at runtime.)
- How would you build dark mode?

### Tailwind fundamentals

**[Must learn now]** Tailwind gives small utility classes (`flex`, `p-4`, `text-lg`, `md:grid-cols-3`) that you compose in your markup. Benefits: no naming, consistent scale, small CSS output, easy responsive variants (`sm:`, `md:`, `lg:`), and state variants (`hover:`, `focus:`, `dark:`). Cost: long class strings. Fix with components (extract a React component, not a CSS class), and a helper for conditional classes. Tailwind v4 is configured mostly in CSS and installs with the Vite plugin; check the installation page for your framework, because details change.

```jsx
export function Card({ title, children }) {
  return (
    <section className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:bg-gray-900">
      <h2 className="mb-2 text-lg font-semibold">{title}</h2>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{children}</div>
    </section>
  );
}
```

Mobile-first: unprefixed classes apply to all sizes; `md:` applies from the `md` breakpoint **up**.

Common mistake: building class names dynamically (`` `text-${color}-500` ``). Tailwind scans your source for complete strings and will not generate those classes. Write the full class names or map them in an object.

Interview questions:

- Pros and cons of utility-first CSS?
- How does Tailwind handle responsive and dark mode?
- Why does `` `bg-${color}-500` `` not work?

### Responsive navigation, tables, forms, dashboards

**[Must learn now]** Four patterns you will build in Project 1:

- **Navigation:** horizontal links on desktop; on mobile, a toggle `button` with `aria-expanded` and `aria-controls` that opens a list. Keep it keyboard-usable, and close on Escape.
- **Tables:** keep a real `<table>` for tabular data. On small screens, wrap in `overflow-x: auto`, or re-layout rows as cards with CSS only when the data is simple. Sticky header helps.
- **Forms:** single column on mobile, two columns on wide screens; large touch targets (about 44px); keep labels visible.
- **Dashboards:** grid of cards (`auto-fit/minmax`), a sidebar that collapses, and a content area with `min-width: 0` to avoid blowouts.

```html
<div class="overflow-x-auto">
  <table class="min-w-full text-left text-sm">
    <caption class="sr-only">Orders</caption>
    <thead><tr><th scope="col">ID</th><th scope="col">Total</th></tr></thead>
    <tbody><tr><td>42</td><td>Rs 500</td></tr></tbody>
  </table>
</div>
```

Common mistake: turning data tables into divs, losing screen reader row and column relationships.

Interview questions:

- How would you make a data table work on a phone?
- How do you build an accessible mobile menu?

### Browser rendering and DevTools

**[Must learn now]** What the browser does: parse HTML to the **DOM**, parse CSS to the **CSSOM**, combine into a render tree, **layout** (sizes and positions), **paint** (pixels), **composite** (layers). CSS in `<head>` blocks first paint; `<script>` without `defer`/`async` blocks parsing. Changing `width` or `top` triggers layout (expensive); changing `transform` or `opacity` usually only composites (cheap). In DevTools: **Elements** (inspect, edit, see computed styles and the box model), **Network** (timing, waterfall, cache), **Performance** (what blocked the main thread), **Lighthouse** (audits), **Application** (cookies, storage), device toolbar (responsive testing).

Common mistake: animating `height` or `left` and getting jank. Prefer `transform`.

Interview questions:

- What is the critical rendering path?
- What is the difference between reflow (layout) and repaint?
- What do `defer` and `async` do on a script tag?

### DOM events: bubbling, capturing, delegation

**[Must learn now]** When you click a button, the event travels down from `window` to the target (**capture** phase) and then back up (**bubble** phase). Listeners by default run in the bubble phase. `event.target` is the element clicked; `event.currentTarget` is the element the listener is attached to. **Event delegation** means one listener on the parent handles clicks for many (even future) children. `stopPropagation()` stops the travel; `preventDefault()` stops the browser's default action (like following a link). React attaches its handlers at the root and handles synthetic events, but the same ideas apply.

```js
const list = document.querySelector("#todo-list");
list.addEventListener("click", (e) => {
  const btn = e.target.closest("button[data-action='delete']");
  if (!btn || !list.contains(btn)) return;
  btn.closest("li").remove();            // works for items added later too
});

const li = document.createElement("li");
li.innerHTML = `<span>New</span> <button data-action="delete">x</button>`;
list.append(li);   // no new listener needed
```

Common mistake: adding a listener to every row in a big table (slow and leaky), or `e.target` being the inner `<svg>` icon and not the button (use `closest`).

Interview questions:

- Explain bubbling vs capturing and `target` vs `currentTarget`.
- What is event delegation and when is it useful?
- `stopPropagation` vs `preventDefault`?

### Accessibility and keyboard navigation

**[Must learn now]** Accessibility (a11y) means everyone can use your page: keyboard-only users, screen reader users, low-vision users, and people on slow or small devices. Basics: semantic HTML first; ARIA only when HTML is not enough ("no ARIA is better than bad ARIA"); visible focus styles; logical tab order (do not use positive `tabindex`); skip link; alt text for meaningful images (`alt=""` for decorative); sufficient contrast; do not trap focus (except in modals, where you must trap it and return it on close); announce dynamic changes (`role="status"`, `aria-live="polite"`). Test with the keyboard (Tab, Shift+Tab, Enter, Space, Escape, arrows) and a screen reader (VoiceOver on Mac, NVDA on Windows). In Chrome Lighthouse, run the accessibility audit.

```html
<a class="sr-only focus:not-sr-only" href="#main">Skip to content</a>
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden> ... </ul>
<div role="status" aria-live="polite" id="toast"></div>
```

Common mistake: `outline: none` with no replacement, so keyboard users cannot see where they are.

Interview questions:

- How do you test accessibility?
- When is ARIA needed and when is it harmful?
- How do you make a modal accessible?

### Performance basics, lazy loading, image optimization

**[Learn during projects]** Core Web Vitals to know by name: **LCP** (how fast the main content shows), **INP** (how responsive the page feels to input), **CLS** (how much the layout jumps). Quick wins: compress and resize images, use modern formats (WebP or AVIF), give images `width` and `height` (prevents layout shift), `loading="lazy"` for below-the-fold images (not for the main hero image), `srcset`/`sizes` for responsive images, `defer` scripts, fewer and smaller JS bundles, cache static files. Measure first (Lighthouse, Performance tab), then fix the biggest item.

```html
<img src="/img/hero-800.webp"
     srcset="/img/hero-400.webp 400w, /img/hero-800.webp 800w, /img/hero-1600.webp 1600w"
     sizes="(min-width: 768px) 50vw, 100vw"
     width="800" height="450" alt="Dashboard preview" fetchpriority="high" />
<img src="/img/photo.webp" width="400" height="300" alt="" loading="lazy" decoding="async" />
```

Common mistake: lazy-loading the hero image (it delays LCP), or shipping a 4000px photo for a 300px slot.

Interview questions:

- What are LCP, INP, and CLS?
- How do you stop layout shift from images?
- When should you not use `loading="lazy"`?

### HTTP status codes, headers, cookies, caching, CORS

**[Must learn now]** This is the most important part for your backend work.

**Status codes you must know:** 200 OK, 201 Created, 204 No Content, 301/302 redirects, 304 Not Modified, 400 Bad Request, 401 Unauthorized (not authenticated), 403 Forbidden (authenticated but not allowed), 404 Not Found, 409 Conflict, 422 Unprocessable Content (validation failed), 429 Too Many Requests, 500 Internal Server Error, 502/503/504 gateway or availability problems.

**Headers:** `Content-Type` (what the body is), `Accept`, `Authorization`, `Cookie`/`Set-Cookie`, `Cache-Control`, `ETag`, `Origin`, `Access-Control-Allow-Origin`, `Location`.

**Cookies:** small data the server sets (`Set-Cookie`) and the browser sends back automatically. Important flags: `HttpOnly` (JavaScript cannot read it, protects from XSS theft), `Secure` (HTTPS only), `SameSite=Lax|Strict|None` (limits cross-site sending, helps against CSRF), `Max-Age`/`Expires`, `Path`, `Domain`.

**Caching:** `Cache-Control: max-age=31536000, immutable` for hashed static assets; `no-cache` means "check with the server before using" (not "never store"); `no-store` means never store; `ETag` + `If-None-Match` gives a cheap `304`. HTML usually should be revalidated; hashed JS/CSS can be cached for a year.

**CORS:** Browsers enforce the **same-origin policy**: a page from `https://app.com` cannot read responses from `https://api.com` unless the API says it may. **Origin** = scheme + host + port. The API replies with `Access-Control-Allow-Origin: https://app.com`. For "non-simple" requests (JSON `POST` with custom headers, `PUT`, `DELETE`) the browser first sends a **preflight** `OPTIONS` request and the server must answer with allowed methods and headers. To send cookies cross-origin you need `credentials: "include"` on the client and `Access-Control-Allow-Credentials: true` plus an exact origin (not `*`) on the server. CORS is a browser rule, not a server firewall: `curl` ignores it, and it does not protect your API from other clients.

```js
// Browser at http://localhost:5173 calling API at http://localhost:3000
const res = await fetch("http://localhost:3000/orders", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  credentials: "include",
  body: JSON.stringify({ item: "tea" }),
});
```

```js
// Express side (preview of Phase 6)
// res.set("Access-Control-Allow-Origin", "http://localhost:5173");
// res.set("Access-Control-Allow-Credentials", "true");
// res.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
// OPTIONS requests must reply 204 with those headers.
```

Common mistakes: "fixing" CORS on the frontend (you cannot; the server must send the headers); using `*` with credentials; confusing 401 and 403; using `no-cache` when you mean `no-store`.

Interview questions:

- 401 vs 403? 400 vs 422? Which code for "created"?
- What is CORS? What is a preflight request? Why does `curl` work when the browser fails?
- `HttpOnly`, `Secure`, `SameSite`: what does each do?
- `no-cache` vs `no-store`? What is an ETag?
- Where would you store a login token: `localStorage` or an `HttpOnly` cookie? Trade-offs?

### React review (start)

**[Must learn now]** Week 4 ends with a light React review, so you carry the base into Phase 4. Do a one-hour review of: components and props, state and re-rendering, controlled inputs, lists and keys, `useEffect` dependencies and cleanup. You are not learning new React yet. You are checking what you can explain. The deeper React gaps (reconciliation, effect traps, context decisions, error boundaries, memoization, testing) are Phase 4, Week 5. The full React learning path is covered in the Phase 4 file.

Common mistake: starting Phase 4 without writing down what you do not understand. Make a list of five React questions that confuse you and bring it to Week 5.

Interview questions:

- What triggers a re-render in React?
- Why do list items need a stable `key`?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Semantic HTML and forms | Landmarks, labels, validation, tables | [web.dev Learn HTML](https://web.dev/learn/html), [MDN: Basic HTML syntax](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax), [MDN: Web forms](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | Build the accessible signup form with native validation |
| CSS core | Selectors, specificity, box model, positioning, overflow | [web.dev Learn CSS](https://web.dev/learn/css), [MDN: Box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model), [MDN: Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity), [MDN: Positioning](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Positioning), [MDN: Stacking context](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context) | No video verified for this topic; use the official documentation above. | Beginner | 3 h | Fix 5 broken CSS snippets (specificity, z-index, overflow) |
| Flexbox | Axes, wrap, gap, flex-grow | [MDN: Flexbox](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox) | [Learn flexbox the easy way (Kevin Powell, English)](https://www.youtube.com/watch?v=u044iM9xsWU) | Beginner | 1 h | Build a navbar and a 3-column layout with flexbox |
| Grid and responsive | Grid, auto-fit, media queries, clamp | [MDN: Grids](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids), [MDN: Responsive design](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_design) | [Learn CSS Grid the easy way (Kevin Powell, English)](https://www.youtube.com/watch?v=rg7Fvvl3taU) | Beginner | 1.5 h | Build a responsive card gallery and a dashboard layout |
| Variables and tokens | Custom properties, theming, dark mode | [MDN: custom properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties) | No video verified for this topic; use the official documentation above. | Intermediate | 1 h | Create a token set and a dark/light toggle |
| Tailwind | Utilities, variants, responsive, dark mode | [Tailwind: installation](https://tailwindcss.com/docs/installation), [Tailwind: responsive design](https://tailwindcss.com/docs/responsive-design) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | Rebuild your dashboard layout using only Tailwind classes |
| Browser and events | Rendering, DevTools, bubbling, delegation | [Chrome DevTools](https://developer.chrome.com/docs/devtools), [MDN: Events](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events), [MDN: Event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling) | [JavaScript DOM Crash Course - Part 1 (Traversy Media, English)](https://www.youtube.com/watch?v=0ik6X4DJKCc) | Intermediate | 2 h | Build a todo list with one delegated listener |
| Accessibility | Keyboard, ARIA, contrast, screen readers | [web.dev Learn Accessibility](https://web.dev/learn/accessibility), [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility), [MDN: HTML a11y basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML), [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Use only the keyboard to complete your form and menu; fix what fails |
| Performance | LCP, CLS, lazy loading, images | [MDN: Web performance](https://developer.mozilla.org/en-US/docs/Web/Performance), [MDN: Lazy loading](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Lazy_loading), [web.dev: LCP](https://web.dev/articles/lcp), [web.dev: CLS](https://web.dev/articles/optimize-cls), [web.dev Learn Images](https://web.dev/learn/images) | No video verified for this topic; use the official documentation above. | Intermediate | 1.5 h | Run Lighthouse on a page, fix the top 3 issues, compare scores |
| HTTP, cookies, caching, CORS | Status codes, headers, cookies, cache, CORS | [MDN: status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status), [MDN: headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers), [MDN: Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies), [MDN: Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching), [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS), [MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) | No video verified for this topic; use the official documentation above. | Intermediate | 3 h | Cause a CORS error on purpose and write down the exact fix |

## Verification notes

- youtube.com oEmbed was unreachable from my environment. Titles and channels were checked through `noembed.com` (proxy for YouTube oEmbed). Durations were NOT verified from the video pages.
- Kevin Powell `u044iM9xsWU`: title "Learn flexbox the easy way", channel Kevin Powell. A Class Central listing described a 34-minute video; I did not verify the length from YouTube. A search result also said the video has hundreds of thousands of views; I ignore that. Language: English (not formally verified). I found this ID through a community comment, so I rely only on the oEmbed title and channel match.
- Kevin Powell `rg7Fvvl3taU`: title "Learn CSS Grid the easy way", channel Kevin Powell. A mirror page showed an upload date of 2021-11-25 and a search summary said about 37 minutes; not verified from YouTube. Grid itself has not changed in a breaking way since; newer features (subgrid, container queries) are in MDN.
- Traversy Media `0ik6X4DJKCc`: title "JavaScript DOM Crash Course - Part 1", channel Traversy Media. It was listed in a freeCodeCamp roundup of JavaScript resources. It is an older video and uses older style in places; use MDN for current event details. Length not verified.
- I did not find a verified good video for HTTP caching/CORS/cookies, accessibility, or Tailwind in this research pass, so I use official documentation only. I did not look for a Hindi video on these topics; none is claimed.
- All MDN, web.dev, Chrome, W3C, and Tailwind links returned HTTP 200 on 2026-10-09. A first guess at an MDN "Semantic HTML" URL returned 404, so I do not include it.
- Cookie flags, CORS preflight behaviour, and cache directive meanings are summarised from my knowledge of the MDN pages listed; open them and confirm any detail before you rely on it in production.

## Hands-on exercises

1. **Semantic rebuild.** Take a page of `div`s from one of your projects and rewrite it with semantic tags. Check the heading outline.
2. **Accessible form.** Build the signup form (labels, native validation, error text with `aria-describedby`). Test it with the keyboard only and VoiceOver or NVDA.
3. **CSS puzzle set.** Fix 5 broken snippets: a specificity war, a hidden z-index modal, a flex child that will not shrink, an overflow clip, a margin collapse.
4. **Layout set.** Build three layouts with no framework: a navbar (flex), a card gallery (grid with `auto-fit`), and a dashboard shell (sidebar + content that stacks on mobile).
5. **Token theme.** Create 10 tokens and a dark/light switch using `data-theme` and `prefers-color-scheme`.
6. **Tailwind rebuild.** Rebuild exercise 4's dashboard shell using Tailwind only. Compare the effort.
7. **Delegation.** Build a todo list with add, toggle, and delete using one delegated listener.
8. **Network detective 2.** In DevTools, find a request with `304`, one `from disk cache`, one with `Set-Cookie`, and one CORS preflight (`OPTIONS`). Write what each header means.
9. **CORS lab.** Run a tiny Node server on port 3000 and a page on port 5173. Reproduce the CORS error, then fix it with the correct headers on the server, including a preflight response.
10. **Lighthouse pass.** Audit one page, fix images (size, `width`/`height`, lazy loading), and record the before and after scores.

## Checkpoint

**Explain:**

- Why a `div` with `onClick` is worse than a `button`.
- How the cascade picks a winner (importance, specificity, order).
- Why you cannot fix CORS from the frontend.
- What the stacking context is, with an example where `z-index` fails.

**Modify code:** Make a 4-column grid collapse to 2 columns under 900px and 1 column under 600px in two ways: media queries, and `auto-fit` with `minmax`.

**Debug:** A flex row has a long unbroken word that pushes the card outside the screen. Fix it (hint: `min-width: 0`, `overflow-wrap: anywhere`). A page works on `localhost` but a fetch to your API fails in the browser only; the `curl` works. What do you check first?

**Write tests/checks:** Run Lighthouse accessibility and get 90 or more on your form page. Write a short manual test list (keyboard, screen reader, zoom 200 percent, small phone width).

**Ready to move on when:**

- You can build a responsive, accessible page from scratch with flex and grid.
- You can read the Network tab for status, headers, cache, and cookies.
- You can explain CORS, cookies flags, and caching in your own words.
- You have written down five React questions for Week 5.

## Week plan

### Week 4 — HTML, CSS, browser and HTTP gap-fill, plus start of React review (estimated hours: 9)

**Learning objectives**

- Build semantic, accessible HTML pages and forms.
- Control layout with the box model, flexbox, grid, and media queries.
- Use CSS variables as design tokens and Tailwind utilities.
- Read DevTools (Elements, Network, Performance) and explain browser rendering.
- Explain events, bubbling and delegation, and HTTP concerns (status, cookies, cache, CORS).
- Begin a short React review and list your gaps.

**Topics and subtopics**

- **[Must learn now]** Semantic HTML, forms, labels, native validation
- **[Must learn now]** Selectors, cascade, specificity, box model
- **[Must learn now]** Display, positioning, stacking context, overflow
- **[Must learn now]** Flexbox, Grid, responsive layout, media queries
- **[Must learn now]** CSS variables and tokens; Tailwind fundamentals
- **[Must learn now]** Responsive nav, tables, forms, dashboards
- **[Must learn now]** DevTools and the rendering pipeline; DOM events and delegation
- **[Must learn now]** Accessibility and keyboard navigation
- **[Must learn now]** HTTP status codes, headers, cookies, caching, CORS
- **[Learn during projects]** Performance basics, lazy loading, image optimization
- **[Must learn now]** React review (about 1 hour): list your gaps for Week 5
- **[Learn later if needed]** Container queries, subgrid, CSS animation details, advanced ARIA patterns

**Small prerequisite concepts**

- What a "viewport" is, and what pixels versus CSS pixels mean on phones.
- What a "pseudo-class" is (`:hover`, `:focus-visible`).
- What the "origin" of a web page is (scheme, host, port).

**Reading**

- [web.dev Learn HTML](https://web.dev/learn/html)
- [web.dev Learn CSS](https://web.dev/learn/css)
- [MDN: Box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [MDN: Flexbox](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox) and [Grids](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids)
- [MDN: Event bubbling](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling)
- [web.dev Learn Accessibility](https://web.dev/learn/accessibility)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS), [Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies), [Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching)
- [Tailwind: responsive design](https://tailwindcss.com/docs/responsive-design)

**Video**

- "Learn flexbox the easy way", Kevin Powell, English, about 34 minutes per Class Central (duration not verified): [watch](https://www.youtube.com/watch?v=u044iM9xsWU)
- "Learn CSS Grid the easy way", Kevin Powell, English, about 37 minutes per a mirror page (duration not verified): [watch](https://www.youtube.com/watch?v=rg7Fvvl3taU)
- "JavaScript DOM Crash Course - Part 1", Traversy Media, English, duration not verified: [watch](https://www.youtube.com/watch?v=0ik6X4DJKCc)

**Hands-on exercises**

1. Exercises 1 and 2 (semantic rebuild, accessible form) on days 1-2.
2. Exercises 3 and 4 (CSS puzzles, layout set) after the flexbox and grid videos.
3. Exercises 5 and 6 (tokens, Tailwind rebuild).
4. Exercise 7 (delegation) and exercise 8 (network detective 2).
5. Exercise 9 (CORS lab) and exercise 10 (Lighthouse pass). Then do the one-hour React review and write your five questions.

**What you must build**

A repo `web-fundamentals` with: (a) a responsive dashboard shell (sidebar, header, card grid, a data table) in plain HTML/CSS and then the same layout in Tailwind, (b) an accessible signup form, (c) a token-based dark/light theme, (d) a CORS lab (tiny Node server + page), and (e) `NOTES.md` with your Lighthouse before/after scores and your five React questions.

**Completion checklist**

- [ ] Page passes the keyboard-only test
- [ ] Layout works at 360px, 768px, 1280px without horizontal scroll
- [ ] Can explain specificity and stacking context with examples
- [ ] Delegated event listener works for new items
- [ ] CORS error reproduced and fixed with the correct headers
- [ ] Can read status, `Cache-Control`, and `Set-Cookie` in the Network tab
- [ ] Lighthouse accessibility 90 or more on the form page
- [ ] Five React questions written down
- [ ] Phase 3 checkpoint passed

**Self-test**

1. What is the difference between 401 and 403?
2. Why does `z-index: 9999` sometimes do nothing?
3. What are the three parts of a preflight CORS exchange (request, headers, response)?
4. What does `HttpOnly` protect against?
5. Why is a `button` better than a clickable `div`?

**Common mistakes**

- Using `div`/`span` for everything and `outline: none` without a replacement.
- Fixed pixel widths and no mobile testing.
- Fighting CSS with `!important` instead of fixing the structure.
- Trying to solve CORS in React code.
- Lazy-loading the main hero image, and forgetting image `width`/`height`.

**Ready to continue when**

- You can build and explain a responsive, accessible layout without a UI library.
- You can describe cookies, caching, and CORS in simple words, and show them in DevTools.
- You have your list of React gaps and your Phase 0 to 3 repos on GitHub.

**Slower-track option**

Stretch to 1.5 weeks. Cut: the Tailwind rebuild (do it inside Project 1 instead), the performance exercise, and the second Kevin Powell video if your grid is strong. Keep: forms and accessibility, flexbox and grid, DevTools, and the HTTP/CORS section; those are used in every later phase. If the assessment showed HTML and CSS are strong (5 or 6 out of 6), compress to 4 hours: do exercises 8 and 9 (HTTP and CORS), the accessibility keyboard test, and the React review.

## Sources

Pages I opened or fetched in this session (HTTP status checked on 2026-10-09 unless noted):

- https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_Web_works
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Session
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
- https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy
- https://developer.mozilla.org/docs/Learn_web_development/Getting_started/Environment_setup/Command_line
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Events
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Event_bubbling
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Debugging_JavaScript
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Equality_comparisons_and_sameness
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Functions
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Working_with_objects
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/this
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Inheritance_and_the_prototype_chain
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Control_flow_and_error_handling
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Event_loop
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Basic_HTML_syntax
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
- https://developer.mozilla.org/en-US/docs/Web/Accessibility
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_cascade/Specificity
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Positioning
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_design
- https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascading_variables/Using_custom_properties
- https://developer.mozilla.org/en-US/docs/Web/Performance
- https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Lazy_loading
- https://javascript.info/closure
- https://javascript.info/event-loop
- https://javascript.info/async
- https://www.typescriptlang.org/docs/handbook/intro.html
- https://www.typescriptlang.org/docs/handbook/2/everyday-types.html
- https://www.typescriptlang.org/docs/handbook/2/objects.html
- https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- https://www.typescriptlang.org/docs/handbook/2/generics.html
- https://www.typescriptlang.org/docs/handbook/2/types-from-types.html
- https://www.typescriptlang.org/docs/handbook/utility-types.html
- https://www.typescriptlang.org/docs/handbook/enums.html
- https://www.typescriptlang.org/docs/handbook/tsconfig-json.html
- https://www.typescriptlang.org/tsconfig/
- https://react.dev/learn/typescript
- https://infoq.com/news/2026/08/typescript-7-released/
- https://registry.npmjs.org/typescript (dist-tags, latest 7.0.2)
- https://nodejs.org/en/download
- https://www.python.org/downloads/
- https://noembed.com/embed (used as a YouTube oEmbed proxy)
- https://nodejs.org/api/test.html
- https://vitest.dev/guide/
- https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F
- https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
- https://git-scm.com/docs/gitignore
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
- https://12factor.net/config
- https://www.conventionalcommits.org/en/v1.0.0/
- https://stackoverflow.com/help/how-to-ask
- https://code.visualstudio.com/docs/setup/setup-overview
- https://code.visualstudio.com/docs/terminal/basics
- https://docs.npmjs.com/about-npm
- https://docs.npmjs.com/cli/v10/commands/npx
- https://docs.python.org/3/library/venv.html
- https://docs.astral.sh/uv/
- https://github.com/nvm-sh/nvm
- https://brew.sh/
- https://learn.microsoft.com/en-us/windows/package-manager/winget/
- https://learn.microsoft.com/en-us/windows/wsl/install
- https://developer.chrome.com/docs/devtools
- https://web.dev/learn/html
- https://web.dev/learn/css
- https://web.dev/learn/accessibility
- https://web.dev/learn/images
- https://web.dev/articles/lcp
- https://web.dev/articles/optimize-cls
- https://www.w3.org/WAI/ARIA/apg/
- https://tailwindcss.com/docs/installation
- https://tailwindcss.com/docs/responsive-design
- https://www.freecodecamp.org/news/git-and-github-crash-course-for-beginners/
- https://www.freecodecamp.org/news/git-and-github-crash-course/
- https://www.freecodecamp.org/news/command-line-basics-for-beginners
- https://www.freecodecamp.org/news/learn-typescript-with-this-crash-course/
- https://www.freecodecamp.org/news/learn-javascript-free-js-courses-for-beginners/
- YouTube videos (title/channel checked via noembed.com; watch pages for some fetched): https://www.youtube.com/watch?v=1XbvNSwvkAs , https://www.youtube.com/watch?v=mAFoROnOfHs , https://www.youtube.com/watch?v=mABpAI-pCw0 , https://www.youtube.com/watch?v=8aGhZQkoFbQ , https://www.youtube.com/watch?v=hdI2bqOjy3c , https://www.youtube.com/watch?v=Oive66jrwBs , https://www.youtube.com/watch?v=yY0bKZNYmJs , https://www.youtube.com/watch?v=GAIbn16Iytc , https://www.youtube.com/watch?v=ZvZ7gvcmPmI , https://www.youtube.com/watch?v=u044iM9xsWU , https://www.youtube.com/watch?v=rg7Fvvl3taU , https://www.youtube.com/watch?v=0ik6X4DJKCc , https://www.youtube.com/watch?v=2pZmKW9-I_k
- YouTube playlists (title fetched only): https://www.youtube.com/playlist?list=PLu71SKxNbfoBuX3f4EOACle2y-tRC5Q37 , https://www.youtube.com/playlist?list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI
