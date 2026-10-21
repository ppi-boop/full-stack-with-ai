# MASTER PROMPT (user's original brief, saved for agents)

Act as a senior software engineer, technical mentor, curriculum designer, and technical learning researcher. Create a complete beginner-to-job-ready learning roadmap handbook for ~24 weeks (8–10 h/week, full-time job). Cover fundamentals to production, including small prerequisites beginners miss. Detailed, not a list of technologies.

## 1. Background and objective
- Full-stack developer in Surat, Gujarat, India. Main experience: JavaScript, React, Next.js, frontend.
- Knows some Node.js/backend; wants stronger fundamentals. Used MongoDB, authentication, API development.
- Wants: Python, FastAPI, Generative AI, RAG, Agentic AI, cloud deployment, production engineering.
- Has access to Claude / AI tools. Prefers easy English, practical examples, step-by-step, direct honest advice.
- Goal: strong engineer who can independently design, build, test, deploy, secure, maintain AI-powered apps.
- Target roles: (1) Full-Stack Engineer with AI integration (2) Python/FastAPI Backend Engineer (3) AI Application / GenAI Engineer (4) Agentic AI Engineer after enough practical experience.
- Does NOT want to abandon JS/React. Build on them. Never promise any technology guarantees employment or immunity from AI automation.

## 2. Research requirements
For every major topic find: best official docs; at least one good video lesson/course; a beginner-friendly explanation when useful; a practical exercise/project; prerequisites and when to move forward.

### Video verification rules
- Direct links to actual YouTube videos, playlists, or course lesson pages. Never a YouTube search-results page.
- Prefer reputable channels/official channels/well-established instructors; recent for fast-changing tools; older OK for stable fundamentals if still accurate.
- Prefer simple English; include Hindi when a genuinely good resource exists.
- Include actual title, creator/channel, language when known, approximate duration when verifiable, direct URL.
- Open/inspect the resource to confirm the link matches title/topic. DO NOT invent titles, channels, durations, URLs, contents, or claim a video was verified when it was not.
- If no suitable video can be verified, say so plainly and give official docs instead.
- Avoid several overlapping full courses for the same topic. Use official docs as source of truth when a video is outdated.
- Document needs a research date and source list.

## 4. Learning plan
24-week plan. For EACH week specify: learning objectives; topics/subtopics; small prerequisite concepts; recommended order; estimated hours; reading resources; video resources; hands-on exercises; what to build; completion checklist; short self-test; common mistakes; definition of "ready to continue". Identify core vs optional vs advanced-to-postpone. Include a slower-track option. Start with a short prerequisite assessment (skip only what can be demonstrated).

## 5. Required curriculum (cover EVERY bullet; do not silently omit)

### PHASE 0 — Developer foundations and setup
How websites/browsers/servers/APIs work. Frontend, backend, database, deployment. What happens after entering a URL. HTTP request/response lifecycle. JSON, REST, DNS, ports, HTTPS. Client-server architecture. Terminal/CLI. Files, folders, paths, permissions, environment variables. Installing/updating Node.js, Python, Git, VS Code, tools. Package managers, npm, npx, virtual environments, Python package management. Git repos, commits, branches, merging, pull requests, .gitignore. .env files, secret management, why API keys must not be committed. Reading error messages, debugging, docs, asking technical questions. Basic software development workflow. Clean dev environment setup on macOS, Windows, Linux where steps differ.

### PHASE 1 — JavaScript fundamentals
let/const/var. Primitive vs reference values. Strings, numbers, booleans, null, undefined. Operators, comparisons, truthy/falsy, coercion. Conditions, loops, iteration. Functions, params, return, scope. Declarations, expressions, arrow functions. Arrays and objects. Destructuring, spread, rest, optional chaining. map/filter/reduce/find/some/every. Object methods and immutability. Callbacks, higher-order functions, closures. this, binding, prototypes, classes. Modules import/export. try/catch. Promises and async/await. Event loop, call stack, microtasks. Promise.all, Promise.allSettled, concurrency basics. Fetch API and HTTP error handling. CommonJS vs ES modules. Memory basics, common mistakes. Debugging with browser dev tools. Basic JS testing. For every major concept: simple example, practical exercise, common interview questions.

### PHASE 2 — TypeScript
Why TS exists. Inference vs explicit types. Primitive, array, tuple, object, function types. Interfaces vs type aliases. Optional/readonly. Union/intersection. Literal types, discriminated unions. Narrowing, type guards. Generics. Utility types. Enums and alternatives. unknown/any/never/void. Null safety. Typing API responses and errors. Typing React props/state/events/custom hooks. Typing async functions. tsconfig and compiler errors. Project organization. Say which topics are essential vs can wait.

### PHASE 3 — HTML, CSS, browser, web fundamentals
Semantic HTML. Forms, inputs, labels, validation, accessibility. CSS selectors, specificity, inheritance, box model. Display, positioning, stacking context, overflow. Flexbox, Grid, responsive, media queries. Typography, spacing, layout systems, reusable styles. CSS variables/design tokens. Tailwind fundamentals. Responsive nav, tables, forms, dashboards. Browser rendering and devtools. DOM events, bubbling, delegation. Accessibility, keyboard navigation. Performance basics, lazy loading, image optimization. HTTP status codes, headers, cookies, caching, CORS.

### PHASE 4 — React
Components/JSX. Props/state. Rendering/re-rendering. Event handlers. Conditional rendering, lists. Keys and reconciliation. Controlled/uncontrolled inputs. Forms/validation. Lifting state, composition. Hooks: useState, useEffect, useRef, useMemo, useCallback, custom hooks. Effect dependencies/cleanup. Avoiding unnecessary effects. Context API and state-management decisions. Error boundaries. Reusable components, folder structure. Data fetching with loading/error/empty states. API integration and cancellation. Performance and memoization. React testing fundamentals. Accessibility, maintainability. Common mistakes and when NOT to memoize.

### PHASE 5 — Next.js and frontend architecture (App Router)
Install/setup. Folder structure. Pages, layouts, route groups, dynamic routes. Navigation, loading states. Server vs Client Components. SSR, static rendering, CSR. Data fetching and caching. Server Functions/Actions and Route Handlers. Forms and mutations. Authentication and protected pages. Metadata, SEO, image optimization. Error handling, not-found. Env variables. API integration. Pagination, search, filters, URL query params. Deployment and production builds. Performance troubleshooting. Clearly distinguish Next.js-specific vs general React concepts.

### PHASE 6 — Backend with Node.js and Express
Node runtime and event-driven architecture. npm. HTTP server basics. Express install and routing. Request, response, middleware. Controllers/services/repositories/route organization. Input and schema validation. Centralized error handling. Authentication vs authorization. Password hashing. Sessions, cookies, JWT, refresh tokens, expiry. RBAC and permissions. REST design and status codes. Pagination, filtering, sorting, search. File uploads and validation. Logging and env config. CORS and security headers. Rate limiting and brute-force protection. API tests and mocking. WebSockets and SSE basics. Background tasks and queues conceptually. Async errors and resource cleanup. Explain when a separate backend is useful instead of Next.js Route Handlers.

### PHASE 7 — Databases and data modeling (PostgreSQL main + MongoDB)
SQL/PostgreSQL: tables, rows, columns, schemas, data types. PK/FK. Constraints, normalization. 1-1, 1-N, M-N. CRUD. Filtering, sorting, grouping, aggregates. Joins. Subqueries and CTEs at appropriate level. Indexes and query plans. Transactions and ACID. Isolation and concurrent updates. Migrations. Connection pooling. Pagination. Backups and restores.
MongoDB: documents, collections, BSON. CRUD. Schema design and validation. Embedding vs referencing. Indexes. Aggregation pipelines. Relationships and consistency. MongoDB vs PostgreSQL suitability.
Also: ORM concepts, SQLAlchemy, database access patterns, basic data-access testing.

### PHASE 8 — Python from absolute basics (for a JS dev)
Install and run scripts. REPL/CLI. Indentation/syntax. Variables/naming. Strings, numbers, booleans, None. Type conversion, operators. Conditions, loops. Lists, tuples, sets, dicts. Slicing, comprehensions. Functions, params, defaults, keyword args. *args/**kwargs. Scope and mutability. References and copying. f-strings. Modules/imports/packages. File handling, context managers. JSON and CSV. Exceptions and custom exceptions. Classes, objects, methods, inheritance, composition. Dataclasses, enums. Iterators, generators. Decorators (practical). Type hints, unions, generics, static checking basics. Logging. Virtual environments and dependency management. pip and pyproject.toml basics. async functions, coroutines, asyncio. HTTP requests. Unit testing and pytest. Project structure. JS-vs-Python differences. Include JS-to-Python comparison tables and small exercises per topic. Do not force data science / NumPy / pandas / advanced maths.

### PHASE 9 — FastAPI and production backend
Create/run app. ASGI, Uvicorn roles. Routes and methods. Path/query params, request bodies. Pydantic models/validation. Response models, status codes. OpenAPI docs. Routers and modular structure. Dependencies/DI. Configuration/settings. PostgreSQL integration. SQLAlchemy vs SQLModel and how to choose. Sessions and transactions. Alembic migrations. Authentication and authorization. Password hashing and tokens. RBAC and resource-level permissions. Async vs sync. Error handling/custom exceptions. Pagination/filtering/sorting. File uploads. Background tasks and queues. WebSockets and streaming responses. Logging and request tracing. pytest and API integration tests. Dependency overrides, test DBs. CORS and security. Timeouts, retries, connection pooling. Health checks, graceful shutdown. Production config and deployment. Explain a maintainable project structure and why each folder exists.

### PHASE 10 — AI/ML foundations for application engineers
AI vs ML vs deep learning vs generative AI. What an LLM is. Training vs inference. Tokens/tokenization. Context windows. Embeddings. Model APIs and inference providers. Temperature/sampling conceptually. System instructions and prompt design. Hallucinations and limits. Latency, cost, rate limits, quotas. Hosted vs local models. Privacy and data handling. Model selection and benchmarking. Explain which concepts need maths vs intuition.

### PHASE 11 — LLM APIs and GenAI application development
Calling model APIs from Python. API keys/secrets. Chat messages and history. Structured outputs and JSON schemas. Tool/function calling. Streaming. Timeouts, retries, rate limits, provider errors. Token counting and usage tracking. Prompt templates. Context management. Model selection. Cost/latency optimization. Guardrails and input/output validation. Evaluation and regression tests. Logging and tracing. Unsupported requests. Provider APIs vs abstractions. Use CURRENT official API docs; mark deprecated/legacy approaches.

### PHASE 12 — Embeddings, vector DBs, RAG
Why keyword search fails. Semantic search and embeddings. Similarity metrics conceptually. Ingestion pipelines. PDF/text extraction. Cleaning. Chunking strategies and overlap. Metadata. Embedding generation. Vector indexing/retrieval. Filtering and permissions. Vector DB fundamentals. Choosing storage. PostgreSQL + pgvector. Top-k. Similarity thresholds. Reranking and hybrid search conceptually. Prompt construction with retrieved passages. Source citations and grounded answers. Missing information. RAG evaluation and retrieval metrics. Chunking/retrieval experiments. Prompt injection in documents. Cross-user document isolation. Cost, latency, observability. Explain RAG with a small example BEFORE frameworks.

### PHASE 13 — Agentic AI
Concepts first: LLM apps vs workflows vs agents. Tool calling and execution. Tool schemas and argument validation. Model-selected actions vs fixed logic. Agent state. History and memory. Planning and bounded execution. Tool-result handling. State transitions and stopping conditions. Retries and recovery. Human-in-the-loop approval. Permissions and authorization. Audit trails. Idempotency and duplicate actions. Timeouts and execution budgets. Agent evaluation. Tracing and debugging. Prompt injection and unsafe tool calls. Multi-agent systems and when unnecessary.
Then LangGraph: models and tools; graphs, nodes, edges, state; conditional routing; checkpointing and persistence; interrupts and human approval; state management and memory; error recovery; streaming; testing and observability; deployment. Compare LangGraph with simple direct tool-calling and other frameworks only where useful. Do not make the learner learn every framework.

### PHASE 14 — Architecture, testing, security
Clean code, separation of concerns. Layered architecture. SOLID with practical examples. DI. Modular monolith vs microservices. API contracts. Unit/integration/e2e tests. Mocking, fixtures. Coverage vs useful quality. Input validation. AuthN/AuthZ. OWASP basics. SQL injection, parameterized queries. XSS, CSRF, CORS, cookie security. Secrets. Rate limiting, abuse prevention. Secure file uploads. Logging without leaking secrets. Migrations and backup/restore tests. AI-specific prompt injection and data leakage. Safe execution of AI-requested actions. Error handling, incident debugging. Provide a PRIORITIZED security checklist for a small production app.

### PHASE 15 — Docker, Linux, cloud, DevOps
Linux commands, processes, permissions, logs. Networking, DNS, ports, TLS, reverse proxies. Docker images/containers, Dockerfiles, layers, volumes, networking, Compose. Containerize Next.js + FastAPI. Env config and secrets. Dev vs prod config. GitHub Actions CI/CD. Automated tests and build pipelines. Cloud fundamentals: compute, storage, managed DBs, networking, IAM. Object storage for uploads. HTTPS and domains. Deployment options. DB backups and migrations. Logs, monitoring, alerts, health checks. Cost monitoring. Rollbacks and basic DR. IaC concepts high level. Choose ONE cloud (preferably AWS); core services first; postpone Kubernetes until a real need. Include a deployment project step-by-step checklist.

### PHASE 16 — Production AI engineering
Evaluating outputs. Building an eval dataset. Groundedness and citation correctness. Retrieval quality. Tool-call correctness. Regression tests after prompt/model changes. Tracing multi-step AI requests. Logging model/tool failures. Rate limits and usage budgets. Latency optimization. Caching. Retry strategies. Human approval for consequential actions. Access control for AI tools. Data privacy. Model/provider fallbacks. Versioning prompts and eval datasets. Monitoring cost and quality. Provider outages. Safe failure modes. Explain how this differs from a chatbot demo.

### PHASE 17 — System design and interview prep
Requirements gathering. Functional/non-functional. API design. DB schema design. Indexes and query performance. Caching and queues. Pagination of large datasets. AuthN/AuthZ. Reliability and availability. Scaling basics. Rate limiting. Idempotency. Logging and observability. Monolith vs microservices. Design: AI document assistant; order management system; AI support assistant with approval workflows. Interview topics: JS, React, TS, Python, SQL, FastAPI, AI. Basic DSA. Coding practice strategy (realistic for full-stack/backend/AI-app roles, not ML research). Resume and GitHub portfolio. Project explanation practice. Mock interview Q&A.

## 6. Projects (increasing difficulty). For EACH include:
Problem statement and real-world use case; requirements and user stories; MVP vs advanced features; suggested architecture; folder structure; DB schema/ERD; API endpoints; packages and setup; implementation milestones; test cases; security checklist; deployment plan; README structure; acceptance criteria; common mistakes; interview questions. Do NOT dump full project code; teach in manageable milestones.
1. Frontend admin dashboard — React/Next.js, TS, responsive UI, forms, pagination, search, API integration, loading/error states, tests.
2. Business order management API — Node/Express, DB design, auth, authorization, CRUD, validation, pagination, tests.
3. Python data utility — CSV/JSON, validate, summaries, call an API, log errors, tests.
4. FastAPI order management backend — FastAPI, PostgreSQL, SQLAlchemy or SQLModel, migrations, auth, roles, tests, logging, API docs.
5. AI document assistant — upload, extraction, chunking, embeddings, retrieval, RAG, grounded answers, citations, access control, evaluation, cost tracking.
6. AI order/refund workflow assistant — tool calling, order lookup, policy retrieval, stateful workflow, permission checks, human approval, audit logs, retries, safe execution.
7. Production portfolio application — frontend, backend, DB, AI, tests, Docker, CI/CD, cloud deployment, monitoring, docs, security controls.

## 7. AI-assisted learning workflow (with Claude)
Teach: explanation before code; hints not full solutions; break features into small tasks; AI code review and trade-offs; generate tests and edge cases; systematic debugging; verify AI code against official docs; check security and dependencies; rebuild features from memory; avoid dependence; track what I can independently explain/implement. Reusable prompts for: (1) learning a topic (2) understanding existing code (3) hint without full solution (4) debugging an error (5) architecture review (6) generating/reviewing tests (7) security review (8) project milestone planning (9) interview practice (10) weekly progress review. When AI boilerplate is OK vs when to implement core logic myself.

## 8. Career strategy (India)
Build on React/Next.js. Compare Full-Stack+AI, Python Backend, GenAI App Engineering, Agentic AI, DevOps/Cloud: prerequisites per role. Research CURRENT job descriptions and recurring skill requirements from reliable recent sources; distinguish evidence from speculation. Best portfolio projects. Resume and GitHub strategy. When to start applying (not after the whole roadmap). Transferable skills. What to postpone. NO promises of jobs, salary, or security.

## 9. Resource table format per phase (all URLs clickable, limited high-quality resources, verified videos)
| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
State clearly when duration, language, or availability could not be verified.

## 10. Progress tracking
24-week master calendar; daily/weekly study template; checkboxes for every topic; project tracker; concepts to revise weekly; revision schedule; skills self-assessment matrix; job-readiness checklist; notes/mistakes/questions section; optional advanced topics. Each phase: checkpoint with practical questions (explain, modify code, debug, write tests). Advance by demonstrating the skill, not by watching videos.

## 11. Style
Simple clear English. Everyday analogies and small code examples. Honest and practical, no exaggeration. Do not skip prerequisites; do not assume React experience means all basics are known. Organize in learning order. Label each item: **Must learn now** / **Learn during projects** / **Learn later if needed**. Prefer official docs and reliable educators; flag outdated approaches. Feels like a personal curriculum/handbook, not marketing.
