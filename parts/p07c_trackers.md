# Progress Trackers and Planning Tools

## How to use this part

This part is the control panel for the whole handbook. Print it or copy it into a notes app. You advance by demonstrating a skill (build it, explain it, debug it, test it), not by watching a video. Update the trackers once a week, on the same day, for 20 minutes. Research date for all planning assumptions: 2026-10-09. No part of this plan guarantees a job; it only keeps you honest about progress.

> **Tip:** If you only maintain two things, keep the weekly review (Section "Weekly study template") and the skills matrix. Everything else is optional bookkeeping.

## 24-week master calendar

The week allocation is fixed across the handbook. Hours are planned study and build hours, not including your job.

| Week | Phase and focus | Planned hours | Main deliverable | Checkpoint to pass |
|---|---|---|---|---|
| 1 | Phase 0: developer foundations, setup, prerequisite assessment | 8 | Clean dev environment, first Git repo with a pull request | Explain what happens after typing a URL; use Git branch and merge |
| 2 | Phase 1: JavaScript core revision (closures, this, event loop microtasks, async, testing) | 9 | Small tested JS utility module | Predict event-loop output; write async code with error handling |
| 3 | Phase 2: TypeScript (interfaces, types, generics, discriminated unions, typing APIs & hooks) | 9 | Typed API client with discriminated unions | Type an API response and a React hook without `any` |
| 4 | Phase 3: HTML, CSS, browser, HTTP gap-fill; Phase 4 React revision start | 9 | Accessible responsive form and layout | Explain specificity, cookies, CORS, caching headers |
| 5 | Phase 4: React deep gaps; Phase 5: Next.js App Router & Vercel AI SDK start | 10 | React components with tests; first App Router pages | Explain effects, keys, Server vs Client Components, useChat |
| 6 | Phase 5 finish; Project 1: admin dashboard | 10 | Project 1 running with search, pagination, tests | Project 1 acceptance criteria met |
| 7 | Phase 6: Node/Express; Project 2 start | 9 | Express API skeleton with validation and error handler | Explain middleware order and authN vs authZ |
| 8 | Project 2 finish: auth, RBAC, validation, tests | 10 | Project 2 with tests and README | Project 2 acceptance criteria met |
| 9 | Phase 7: PostgreSQL, MongoDB, SQL, indexes, transactions | 10 | Schema, queries, and EXPLAIN notes for an order database | Write joins, a transaction, and justify an index |
| 10 | Phase 8: Python part 1 from scratch (syntax to functions, collections, files, uv, ruff) | 9 | Python exercises repo | Rewrite five JS snippets in Python from memory |
| 11 | Phase 8: Python part 2 from scratch (OOP, typing, async, pytest); Project 3 | 10 | Project 3 data utility with tests | Project 3 acceptance criteria met |
| 12 | Phase 9: FastAPI part 1 from scratch (routes, Pydantic v2, DI, structure) | 9 | FastAPI app with routers and settings | Explain Depends and Pydantic validation |
| 13 | Phase 9: FastAPI part 2 from scratch (PostgreSQL, SQLAlchemy 2.0, Alembic, auth/RBAC) | 10 | DB-backed API with migrations and login | Run a migration up and down; protect a route by role |
| 14 | Phase 9 finish (tests, logging, background queues, WebSockets/streaming); Project 4 finish | 10 | Project 4 FastAPI order backend | Project 4 acceptance criteria met; start applying to backend roles |
| 15 | Phase 10 and 11: AI foundations, Reasoning models, Prompt Caching, LLM APIs from scratch | 9 | CLI chat with streaming, structured output, tool call | Explain tokens, context window, cost; handle provider errors |
| 16 | Phase 12: Embeddings, pgvector, Hybrid RAG (BM25 + Dense with RRF), Reranking from scratch | 10 | Working RAG script with citations | Explain chunking trade-offs; show retrieval results |
| 17 | Project 5: AI document assistant and Hybrid RAG evaluation | 10 | Project 5 with evaluation set | Eval numbers recorded; per-user isolation tested |
| 18 | Phase 13: Agentic AI, Model Context Protocol (MCP), LangGraph from scratch | 9 | Small stateful graph with interrupt & MCP tool | Explain workflow vs agent; resume after interrupt |
| 19 | Project 6: Order/refund workflow assistant (LangGraph + MCP + Human-in-the-Loop) | 10 | Project 6 with approval and audit log | Project 6 acceptance criteria met |
| 20 | Phase 14: Architecture, testing, OWASP & AI security | 9 | Security checklist applied to Projects 4-6 | Fix three real findings; explain OWASP basics |
| 21 | Phase 15: Linux, Docker, AWS cloud, CI/CD | 10 | Dockerised app with CI pipeline | Containers run locally; CI green |
| 22 | Phase 16: Production AI engineering, Langfuse tracing; Project 7 start | 10 | Eval, tracing, usage budgets in Project 7 | Regression eval runs after a prompt change |
| 23 | Project 7: Flagship Full-Stack AI Platform (Next.js + Vercel AI SDK + FastAPI + Cloud) | 10 | Project 7 deployed with monitoring | Public demo, health check, alert, rollback tested |
| 24 | Phase 17: System design, interview prep, portfolio, resume, apply strategy | 10 | Resume, GitHub, three designs, mock interviews | Two mock interviews scored |

Calendar checklist (tick when the checkpoint is passed, not when the week ends):

- [ ] Week 1 passed
- [ ] Week 2 passed
- [ ] Week 3 passed
- [ ] Week 4 passed
- [ ] Week 5 passed
- [ ] Week 6 passed (Project 1)
- [ ] Week 7 passed
- [ ] Week 8 passed (Project 2)
- [ ] Week 9 passed
- [ ] Week 10 passed
- [ ] Week 11 passed (Project 3)
- [ ] Week 12 passed
- [ ] Week 13 passed
- [ ] Week 14 passed (Project 4)
- [ ] Week 15 passed
- [ ] Week 16 passed
- [ ] Week 17 passed (Project 5)
- [ ] Week 18 passed
- [ ] Week 19 passed (Project 6)
- [ ] Week 20 passed
- [ ] Week 21 passed
- [ ] Week 22 passed
- [ ] Week 23 passed (Project 7)
- [ ] Week 24 passed (interview kit ready)

## Daily and weekly study template

For a full-time worker, 8 to 10 hours a week is enough only if the sessions are protected. A realistic pattern is three weekday sessions of 1 to 1.5 hours and one longer weekend block, with a short Sunday review. Adapt to your life; the structure matters more than the clock.

| Day | Block | Hours | What to do |
|---|---|---|---|
| Monday | Learn | 1 | Read the docs section and watch the video for the week's first topic; take notes in your own words |
| Tuesday | Practise | 1 to 1.5 | Do the week's exercise 1 and 2 by typing the code yourself |
| Wednesday | Rest or 20 min revision | 0 to 0.5 | Spaced revision cards for earlier weeks |
| Thursday | Build | 1 to 1.5 | Work on the week's deliverable; write one test |
| Friday | Rest | 0 | No study; protect recovery |
| Saturday | Deep build | 3 to 4 | Longer build session; one AI-off block (docs and editor only) |
| Sunday | Review and plan | 1.5 to 2 | Blank-page rebuild of one feature; self-test; weekly review; plan next week |

Daily 60 to 90 minute session structure:

1. 5 minutes: write today's single goal ("one working POST route with validation").
2. 10 minutes: revise yesterday's notes from memory (no looking first).
3. 40 to 60 minutes: focused work, phone away, 25-minute timers with 5-minute breaks.
4. 5 minutes: commit, write one sentence in the log: what worked, what is unclear.

Weekly review template (copy each Sunday):

```text
Week: __  Phase: __  Planned hours: __  Actual hours: __
Completed:
Not completed (and why):
What I can explain without notes:
What I can implement without AI:
What I needed AI help for:
3 mistakes or bugs and their root causes:
Open questions (go to the questions list):
Ready to continue? (yes / no / partly) because:
Next week: top 3 tasks, and what I will cut if I run late:
```

Weekly checkboxes:

- [ ] Planned hours were protected in the calendar
- [ ] Exercises done by typing, not pasting
- [ ] At least one test or check written for the deliverable
- [ ] Everything committed; branch or pull request opened
- [ ] Self-test answered without notes
- [ ] Blank-page rebuild of one feature done
- [ ] Mistakes log updated
- [ ] Weekly review written

## Project progress tracker

Project weeks: P1 W6, P2 W7-8, P3 W11, P4 W12-14, P5 W16-17, P6 W19, P7 W22-23. Update the status column each Sunday. Statuses: Not started, Planning, Building, Testing, Deployed, Documented, Done.

| Project | Target week | Core skills proved | Repo link | Status | README done | Tests passing | Deployed or demoed | Date finished |
|---|---|---|---|---|---|---|---|---|
| 1. Frontend admin dashboard | 6 | React/Next.js, TypeScript, forms, pagination, tests | | Not started | No | No | No | |
| 2. Order management API (Node/Express) | 7-8 | Auth, RBAC, validation, DB design, tests | | Not started | No | No | No | |
| 3. Python data utility | 11 | CSV/JSON, validation, API calls, logging, pytest | | Not started | No | No | No | |
| 4. FastAPI order management backend | 14 | FastAPI, PostgreSQL, migrations, roles, tests | | Not started | No | No | No | |
| 5. AI document assistant | 17 | RAG, citations, access control, evaluation, cost | | Not started | No | No | No | |
| 6. AI order/refund workflow assistant | 19 | Tool calling, state, approval, audit, idempotency | | Not started | No | No | No | |
| 7. Production portfolio application | 23 | Docker, CI/CD, AWS, monitoring, security, docs | | Not started | No | No | No | |

Per-project completion checklists:

- [ ] Project 1: requirements and user stories written
- [ ] Project 1: responsive layout, loading, error and empty states
- [ ] Project 1: search, filters, pagination use URL query params
- [ ] Project 1: tests for key components pass
- [ ] Project 1: README with screenshots
- [ ] Project 2: schema/ERD drawn
- [ ] Project 2: auth with hashed passwords and expiring tokens
- [ ] Project 2: roles enforced on every route and ownership checked
- [ ] Project 2: validation and central error handling
- [ ] Project 2: API tests pass; README with endpoint list
- [ ] Project 3: reads CSV and JSON, validates rows, reports errors
- [ ] Project 3: calls an API with timeout and retry; logs failures
- [ ] Project 3: pytest tests pass; clean `pyproject.toml`
- [ ] Project 4: PostgreSQL models and Alembic migrations
- [ ] Project 4: JWT login, roles, resource-level permissions
- [ ] Project 4: pagination, filtering, idempotency key on order create
- [ ] Project 4: pytest with test database and dependency overrides
- [ ] Project 4: OpenAPI docs reviewed; README done; apply-to-backend-roles trigger reached
- [ ] Project 5: upload, extraction, chunking, embeddings stored
- [ ] Project 5: grounded answers with citations; "not found" behaviour
- [ ] Project 5: per-user isolation test passes
- [ ] Project 5: evaluation set (30 or more questions) and recorded metrics
- [ ] Project 5: usage and cost tracking; apply-to-AI-roles trigger reached
- [ ] Project 6: order lookup and policy retrieval tools with validation
- [ ] Project 6: stateful workflow with human approval interrupt
- [ ] Project 6: audit log, idempotent refund, retries, step and cost limits
- [ ] Project 6: tests for unauthorised and duplicate actions pass
- [ ] Project 7: frontend, backend, DB, AI feature integrated
- [ ] Project 7: Docker, CI pipeline, deployed on AWS with HTTPS
- [ ] Project 7: logs, health check, alert, backup and restore tested
- [ ] Project 7: security checklist applied; README, architecture diagram, demo

## Weekly revision list

Revise these concepts every week on the Sunday review (10 minutes, from memory, then check). Tick when you can explain each aloud in under a minute.

- [ ] Request lifecycle: URL to rendered page, including DNS, TLS, HTTP
- [ ] Event loop and the order of sync, microtasks, macrotasks
- [ ] Closures and `this`
- [ ] Promises, `async/await`, error handling in async code
- [ ] TypeScript narrowing and why runtime validation is still needed
- [ ] React rendering, state, effects and keys
- [ ] Server vs Client Components and caching in Next.js
- [ ] HTTP status codes, cookies, CORS, caching headers
- [ ] Authentication vs authorization; where tokens are stored
- [ ] SQL joins, transactions, indexes, N+1
- [ ] Python mutability, comprehensions, generators, context managers
- [ ] FastAPI dependencies, Pydantic validation, sync vs async
- [ ] Tokens, context window, embeddings, cost
- [ ] RAG pipeline steps and typical failure points
- [ ] Workflow vs agent; tool validation; approval and idempotency
- [ ] OWASP basics, injection, prompt injection, secrets handling
- [ ] Docker image vs container; CI steps; what to monitor
- [ ] Evaluation: dataset, metric, regression after a change

## Spaced revision schedule (1-3-7-21 days)

After you pass a week's checkpoint, schedule five short revision touches. Each is 10 to 20 minutes and uses active recall (questions or rebuilding), not re-reading. The pattern: day 1, day 3, day 7, day 21 after learning. The numbers are a common starting rule, not a law; adjust if you forget faster.

| Phase and topics | Day 1 | Day 3 | Day 7 | Day 21 |
|---|---|---|---|---|
| Phase 0 foundations (Git, HTTP, env vars, terminal) | Re-run the Git workflow from memory | Explain URL lifecycle aloud | Create a repo and PR from scratch | Teach it to a friend or rubber duck |
| Phase 1 JavaScript | Predict output for 5 snippets | Rebuild a debounce and a promise helper | Write async fetch with error handling | Solve 3 interview questions aloud |
| Phase 2 TypeScript | Re-type a generic function | Convert a JS file to TS strictly | Type an API response with a union | Explain `unknown` vs `any` and narrowing |
| Phase 3 HTML, CSS, HTTP | Build a flex/grid layout blind | Explain specificity and the box model | Check keyboard access on a page | Explain CORS and cookies with a diagram |
| Phase 4 React | Rebuild a controlled form | Explain effect dependencies | Write a custom hook and test | Explain when not to memoize |
| Phase 5 Next.js | Draw route and layout tree | Explain Server vs Client Components | Add a Server Action with validation | Explain caching and rendering modes |
| Phase 6 Node/Express | Write middleware order from memory | Explain JWT and refresh flow | Add rate limit and CORS | Describe a safe error-handling design |
| Phase 7 databases | Write 3 joins from memory | Explain ACID and isolation | Add an index and read EXPLAIN | Compare PostgreSQL vs MongoDB for a case |
| Phase 8 Python | Rewrite 5 JS snippets in Python | Write a generator and decorator | Write a pytest with fixture | Explain mutability and copying |
| Phase 9 FastAPI | Rebuild a CRUD router | Explain dependency injection | Write a migration and rollback | Add a test with dependency override |
| Phase 10-11 AI and LLM APIs | Explain tokens and context | Call API with structured output | Add retry and timeout | Estimate cost for a workload |
| Phase 12 RAG | Draw the RAG pipeline | Explain chunk size trade-offs | Run a retrieval experiment | Explain prompt injection in documents |
| Phase 13 agents | Define workflow vs agent | Sketch a graph with interrupt | Write a tool schema with validation | Explain idempotent tool execution |
| Phase 14 architecture and security | List the security checklist | Explain layers and DI | Find an IDOR in your own code | Review a pull request for risks |
| Phase 15 Docker, cloud, CI | Write a Dockerfile from memory | Explain image layers and volumes | Edit a CI workflow | Explain rollback steps |
| Phase 16 production AI | Explain eval dataset design | Add one eval case | Run regression after a prompt change | Explain fallbacks and budgets |
| Phase 17 system design and interview | Redraw one design | Answer 5 mock questions aloud | Explain a project in 2 minutes | Do a full mock interview |

Revision checkboxes (copy a row per topic if you want finer tracking):

- [ ] Day 1 touches done for the current week
- [ ] Day 3 touches done
- [ ] Day 7 touches done
- [ ] Day 21 touches done for topics from three weeks ago
- [ ] Any card you missed twice moved to the mistakes log

## Skills self-assessment matrix

Levels: **0** never used, **1** can follow a tutorial, **2** can do it with docs and some AI help, **3** can do it independently without AI and explain it, **4** can teach it, review others' code and handle edge cases. Evidence means a link to a repo, commit, test, note or recorded explanation. Re-score every four weeks; be strict. A score without evidence is a guess.

| Skill | Start level | Week 8 | Week 16 | Week 24 | Evidence (link or note) |
|---|---|---|---|---|---|
| Git, terminal, environment setup | | | | | |
| JavaScript fundamentals and async | | | | | |
| TypeScript | | | | | |
| HTML, CSS, accessibility | | | | | |
| HTTP, cookies, CORS, caching | | | | | |
| React | | | | | |
| Next.js App Router | | | | | |
| Node.js and Express | | | | | |
| Authentication and authorization | | | | | |
| SQL and PostgreSQL | | | | | |
| MongoDB | | | | | |
| Python fundamentals | | | | | |
| pytest and testing habits | | | | | |
| FastAPI | | | | | |
| SQLAlchemy and Alembic | | | | | |
| LLM APIs, structured output, tool calling | | | | | |
| Embeddings, pgvector, RAG | | | | | |
| RAG evaluation | | | | | |
| Agent workflows and LangGraph | | | | | |
| Security (OWASP, prompt injection) | | | | | |
| Docker and Linux | | | | | |
| CI/CD and AWS basics | | | | | |
| Observability and monitoring | | | | | |
| System design | | | | | |
| DSA basics (easy to medium) | | | | | |
| Explaining projects and communication | | | | | |

Matrix checkboxes:

- [ ] Start-level scores entered honestly in Week 1
- [ ] Week 8 re-score done with evidence
- [ ] Week 16 re-score done with evidence
- [ ] Week 24 re-score done with evidence
- [ ] Every skill at level 3 or above has a link to proof

## Job-readiness checklist

Not all boxes are needed to start applying. The triggers: backend roles after Project 4, AI application roles after Project 5, agent-focused roles after Project 6, with Project 7 as the finishing proof (see the career strategy section).

Foundations:

- [ ] I can set up a project, use Git branches and pull requests, and keep secrets out of the repo
- [ ] I can explain HTTP, REST, cookies, CORS, and status codes
- [ ] I can write and debug asynchronous JavaScript and Python
- [ ] I can read an error and find the cause using logs, debugger, and docs

Frontend and Node:

- [ ] I can build and test a typed React/Next.js feature with loading, error, and empty states
- [ ] I can build an authenticated Express API with validation and tests

Python and data:

- [ ] I can build a FastAPI service with PostgreSQL, migrations, auth, roles, and tests
- [ ] I can write SQL joins, transactions, and justify indexes with EXPLAIN

AI engineering:

- [ ] I can call an LLM API with retries, timeouts, structured output, and cost tracking
- [ ] I can build a RAG pipeline with citations and per-user isolation
- [ ] I can build an evaluation set and explain my metrics
- [ ] I can build a tool-using workflow with approval, idempotency, and audit logging
- [ ] I can explain prompt injection and how my project defends against it

Production:

- [ ] I can containerise an app and run CI on every pull request
- [ ] I have deployed an app with HTTPS, logs, health check, and a tested rollback
- [ ] I have a prioritised security checklist applied to my project

Interview and career:

- [ ] Three pinned, documented repositories with real setup instructions
- [ ] A one-page truthful resume and a consistent LinkedIn profile
- [ ] I can explain two projects in 2 minutes and defend design choices
- [ ] I can answer common JS, React, TS, Python, SQL, FastAPI, and AI questions aloud
- [ ] I can solve easy problems reliably and medium ones with effort
- [ ] I completed at least two mock interviews and fixed the weak points
- [ ] I have a weekly application routine and a log

## Notes, mistakes and questions template

Keep these three logs in one notes file or repository. Review the mistakes log every Sunday; review the whole file monthly.

```text
=== MISTAKES LOG ===
Date | Phase/Week | What went wrong | Root cause | Fix | How I will avoid it | Revisit date
```

```text
=== QUESTIONS LIST ===
Date | Question | Where I looked (docs link) | Answer in my own words | Still unclear? (y/n)
```

```text
=== NOTES (one per topic) ===
Topic: __   Date: __   Source: __
In one sentence:
Analogy:
Smallest example:
When to use / when not to:
Common mistake:
Interview question I can now answer:
```

```text
=== AI MISTAKES (things the AI got wrong) ===
Date | Tool | Wrong claim or code | How I detected it | Doc link that proves the truth
```

Template checkboxes:

- [ ] Mistakes log created in Week 1
- [ ] Questions list created in Week 1
- [ ] AI mistakes log created in Week 1
- [ ] Monthly review done after Weeks 4, 8, 12, 16, 20, 24

## Slower-track plan (32 to 36 weeks)

If you work long hours or have family duties, stretch the handbook rather than skipping the basics. Planned hours drop to 6 to 8 per week. Do not cut checkpoints. A slower pace that sticks beats a fast one that you abandon.

| Slower-track weeks | Phase and focus | Original weeks | Notes |
|---|---|---|---|
| 1-2 | Phase 0 and prerequisite assessment | 1 | Take extra time on Git and HTTP |
| 3-4 | Phase 1 JavaScript gap-fill | 2 | Skip topics you can demonstrate |
| 5 | Phase 2 TypeScript essentials | 3 | Defer advanced generics until projects |
| 6-7 | Phase 3 and React review | 4 | Pass the checkpoints, not the whole course |
| 8-9 | Phase 4 deep gaps and Next.js start | 5 | |
| 10-11 | Next.js finish and Project 1 | 6 | Cut Project 1 to MVP |
| 12-13 | Phase 6 Express and Project 2 start | 7 | |
| 14-15 | Project 2 finish | 8 | |
| 16-17 | Phase 7 databases | 9 | Postgres first; MongoDB review only |
| 18-19 | Python part 1 | 10 | |
| 20-21 | Python part 2 and Project 3 | 11 | |
| 22-23 | FastAPI part 1 | 12 | |
| 24-25 | FastAPI part 2 | 13 | |
| 26-27 | FastAPI finish and Project 4 | 14 | Start applying to backend roles |
| 28-29 | AI foundations and LLM APIs | 15 | |
| 30-31 | RAG | 16 | |
| 32-33 | Project 5 and evaluation | 17 | Start applying to AI application roles |
| 34-35 | Agents and LangGraph, Project 6 start | 18-19 | |
| 36+ | Remaining phases at 2 weeks each: security, Docker/AWS, production AI, Project 7, Phase 17 | 20-24 | Continue until done or apply with what you have |

If you are time-poor and must cut, use this order. Cut the first items first:

1. Cut optional resources and second videos; keep official docs.
2. Cut Project 1 to a thin MVP (one list page, one form, five tests).
3. Cut MongoDB depth (keep a one-evening comparison note).
4. Cut Project 3 to a one-hour script plus pytest (keep Python practice).
5. Cut LangGraph to simple direct tool-calling with your own state table (keep approvals and idempotency).
6. Cut AWS to one deploy path (single VM or one managed service) with Docker, HTTPS, logs.
7. Never cut: Git, HTTP and security basics, SQL and PostgreSQL, Python and FastAPI, RAG basics and evaluation, tests, and Project 4 and 5.
8. Defer Phase 15 depth, Phase 16 depth, and Project 7 polish until after you begin applying.

Slower-track checkboxes:

- [ ] Chose pace (24, 30 or 36 weeks) and wrote the end date
- [ ] Reduced weekly hours to a number I can sustain
- [ ] Marked which items I cut and why
- [ ] Re-checked the calendar every four weeks
- [ ] Apply-trigger weeks written for my own pace

## Core vs optional vs postpone

Labels: **Core** means required for the target roles; **Optional** means useful, do if time allows or when a project needs it; **Postpone** means skip until the core is solid or a job requires it. The classification is the author's judgement for your goals, not an industry rule.

| Phase | Classification | Reasoning |
|---|---|---|
| 0 Developer foundations and setup | Core | Everything depends on terminal, Git, HTTP and secrets handling; skip parts you can demonstrate |
| 1 JavaScript fundamentals | Core (revision & gap-fill) | You know JS; revision needed for interview traps: closures, event loop microtasks, async |
| 2 TypeScript | Core | Standard in frontend and Node roles; generics and utility types can wait for projects |
| 3 HTML, CSS, browser, web fundamentals | Core (gap-fill) | HTTP, cookies, CORS and accessibility are asked in interviews; advanced CSS is optional |
| 4 React | Core (revision & gap-fill) | Your existing strength; revise rendering lifecycle, hooks, and memoization trade-offs |
| 5 Next.js and frontend architecture | Core | Main frontend framework; App Router, Server Components, and Vercel AI SDK streaming UI |
| 6 Node.js and Express | Core | Backend fundamentals, auth, RBAC and API design carry over to FastAPI |
| 7 Databases (PostgreSQL main, MongoDB) | Core (PostgreSQL), Beginner-to-Solid (MongoDB) | Relational design and SQL are asked everywhere; MongoDB document modeling & aggregation |
| 8 Python from basics | Core (from scratch) | Required for FastAPI and AI work; modernized with uv and ruff |
| 9 FastAPI and production backend | Core (from scratch) | Main Python backend skill; SQLAlchemy 2.0, Alembic, auth, background task queues |
| 10 AI/ML foundations for application engineers | Core (from scratch) | Concepts only; tokens, reasoning models, thinking budgets, and local Ollama testing |
| 11 LLM APIs and GenAI app development | Core (from scratch) | Structured output, tool calling, and Prompt Caching for 80-90% cost reduction |
| 12 Embeddings, vector DBs, RAG | Core (from scratch) | pgvector, Production Hybrid Search (BM25 + Dense) with RRF, and cross-encoder reranking |
| 13 Agentic AI, MCP and LangGraph | Core (from scratch) | Workflows vs agents, Model Context Protocol (MCP) tools, LangGraph checkpointers, HITL |
| 14 Architecture, testing, security | Core (from scratch) | Separates a demo from a safe product; OWASP Top 10, prompt injection defenses |
| 15 Docker, Linux, cloud, DevOps | Core (from scratch) | Deploy proof matters; Docker, AWS EC2/RDS/S3, and GitHub Actions CI/CD |
| 16 Production AI engineering | Core (from scratch) | Evaluation datasets, Langfuse tracing, regression gates, usage budgets |
| 17 System design and interview prep | Core (capstone) | Needed to convert skills into interview performance; Full-Stack AI system architectures |

Classification checkboxes (tick when you have decided what to skip):

- [ ] Phase 0 decision recorded
- [ ] Phase 1 decision recorded
- [ ] Phase 2 decision recorded
- [ ] Phase 3 decision recorded
- [ ] Phase 4 decision recorded
- [ ] Phase 5 decision recorded
- [ ] Phase 6 decision recorded
- [ ] Phase 7 decision recorded
- [ ] Phase 8 decision recorded
- [ ] Phase 9 decision recorded
- [ ] Phase 10 decision recorded
- [ ] Phase 11 decision recorded
- [ ] Phase 12 decision recorded
- [ ] Phase 13 decision recorded
- [ ] Phase 14 decision recorded
- [ ] Phase 15 decision recorded
- [ ] Phase 16 decision recorded
- [ ] Phase 17 decision recorded

## Optional advanced topics for later

None of these are required for the roadmap's goals. Each label says when it is worth doing. Do not start any of them before Project 4 is done and you are applying.

- [ ] **[Learn later if needed]** Kubernetes basics (pods, deployments, services). Do it when a job or your team actually runs it; Docker Compose and one managed container service are enough for portfolio proof.
- [ ] **[Learn later if needed]** Infrastructure as code (Terraform or similar). Do it after you have deployed manually twice and know what you would automate.
- [ ] **[Learn later if needed]** Fine-tuning or adapting models (LoRA, QLoRA). Do it only if prompting, RAG and evaluation cannot reach your quality target and you have specific domain data.
- [ ] **[Learn later if needed]** Multi-agent systems with autonomous collaboration (CrewAI, AutoGen). Do it only after single-agent workflows with human-in-the-loop approvals and MCP are rock solid.
- [ ] **[Learn later if needed]** Dedicated high-scale vector databases (Pinecone, Qdrant cluster, Weaviate). Use when dataset exceeds tens of millions of vectors beyond pgvector scale.
- [ ] **[Learn later if needed]** Advanced distributed message brokers (Kafka, RabbitMQ clustering). Do it when in-process background tasks or Redis queues are saturated.
- [ ] **[Learn later if needed]** Microservices, API gateways, service mesh. Do it when team size or scaling needs justify the operational overhead.
- [ ] **[Learn later if needed]** GraphQL or gRPC. Learn when a team or job specifically requires it.
- [ ] **[Learn later if needed]** Advanced PostgreSQL replication, multi-region partitioning, and connection pooling clusters (PgBouncer).
- [ ] **[Learn later if needed]** Cloud certification (AWS Certified Solutions Architect). Consider for cloud-heavy consulting roles; deployed projects remain the main proof.
- [ ] **[Learn later if needed]** Mobile (React Native) or desktop (Electron / Tauri). Outside the target full-stack AI roles.
- [ ] **[Learn later if needed]** Data science libraries (NumPy, pandas) and classical ML. Learn only if a role specifically needs them.
- [ ] **[Learn later if needed]** Harder DSA (dynamic programming, advanced graphs). Needed only for specific enterprise online coding assessments.
- [ ] **[Learn later if needed]** Web performance deep dive (Core Web Vitals profiling) and advanced accessibility audits.
- [ ] **[Learn later if needed]** Contributing to open source AI frameworks (LangGraph, MCP servers). Excellent for portfolio credibility.

## Sources

This file is a planning and tracking template built from the fixed week allocation in FORMAT.md and the curriculum in MASTER_PROMPT.md. It contains no external claims that need a URL beyond the following, which were opened on 2026-10-09:

- https://code.claude.com/docs/en/best-practices
- https://www.angelone.in/news/stocks/info-edge-s-naukri-jobspeak-report-white-collar-hiring-up-5-in-july-2026-ai-ml-roles-lead-growth
- https://cxotoday.com/research/skills-over-degrees-nasscom-indeed-report-reveals-indias-evolving-ai-hiring-landscape/

The spaced repetition schedule (1, 3, 7, 21 days) is a common practical rule of thumb and is offered as a starting point, not as a verified optimum; no source was consulted for it. The 8 to 10 hour weekly split is a suggestion for a full-time worker and was not taken from a study.
