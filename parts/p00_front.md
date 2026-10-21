# How to Use This Handbook

## Who this is for

This handbook is written for one person: a full-stack developer in Surat, Gujarat, India. Your exact learning profile is:

1. **JavaScript and React [Revision & Gap-Fill]:** You already build UIs. Your goal here is not to start from scratch, but to systematically revise core mechanics, fill interview gaps (closures, event loop, prototype inheritance, async microtasks, reconciliation, hook rules, memoization trade-offs), and build rock-solid architectural instincts.
2. **Next.js, Node.js and MongoDB [Beginner to Solid]:** You have beginner-level experience. We allocate dedicated weeks to build real mastery: Next.js App Router (Server vs Client Components, Server Actions, Route Handlers, data caching, and modern Vercel AI SDK streaming), Node.js/Express backend architecture (middleware pipelines, JWT/cookies, RBAC, error handling), and MongoDB schema modeling and aggregation pipelines.
3. **Python, FastAPI, PostgreSQL, GenAI, RAG, Agentic AI, MCP, Cloud & DevOps [Taught from Scratch]:** You have zero prior experience in these topics. Every concept will be taught step-by-step from first principles, with clear analogies, internal mechanics, and practical code—with zero hand-waving or assumed knowledge.

You study about 8 to 10 hours a week for 24 weeks while keeping your full-time job. That is roughly 200 to 240 hours in total. Be honest with yourself: that is enough to learn a lot, and not enough to master everything. The plan therefore labels every topic so you know where to spend your limited hours.

## Key additions in this updated handbook

To reflect the reality of modern full-stack and AI engineering, this edition incorporates:
- **Vercel AI SDK and Streaming UI:** Connecting Next.js App Router directly to streaming model responses and Generative UI widgets (`useChat`, `streamText`).
- **Model Context Protocol (MCP):** The industry standard developed by Anthropic for exposing tools, database queries, and context to LLM agents.
- **Prompt and Context Caching:** Slashing token costs by 70 to 90 percent and cutting latency across Anthropic, Gemini, and OpenAI APIs.
- **Reasoning Models and Thinking Budgets:** Operating models with extended reasoning tokens (Claude 3.7 Thinking, o1/o3-mini, Gemini Flash Thinking).
- **Production Hybrid RAG:** Moving beyond toy vector search to real-world dense vector + BM25 keyword search with Reciprocal Rank Fusion (RRF), cross-encoder reranking, and table parsing.
- **Modern Python Tooling:** Using Astral's `uv` and `ruff` for fast dependency management and reproducible environments.
- **Local LLMs for Zero-Cost Dev:** Using Ollama for unit tests and local iteration without eating API budgets.

## Research date and how to trust the links

- Research date: **9 October 2026**.
- Official documentation pages were opened on that date. Videos were checked against YouTube's own title and channel data. Where a duration, language or availability could not be confirmed, the document says so in the "Verification notes" of that phase.
- Tools such as Next.js, FastAPI, the Claude and OpenAI APIs, LangGraph and AWS change quickly. **Official documentation is the source of truth. If a video disagrees with the docs, follow the docs.**
- Links die and videos get removed. If one fails, search the official documentation for the topic name instead of searching random tutorials.

## The three labels

Every topic carries one of these labels:

- **[Must learn now]**: You need this to continue. Do not skip it unless you pass the skip test.
- **[Learn during projects]**: Learn it when the project needs it. Do not study it in isolation first.
- **[Learn later if needed]**: Useful, but postponing it will not block you. Come back after you have shipped something.

## The rule that matters most

> **Honest note:** You do not advance because you watched a video. You advance when you can **demonstrate** the skill: explain it in your own words, modify working code, debug a broken version, and write a test for it. Every phase ends with a checkpoint that tests exactly this.

## What this handbook does not promise

- It does not promise a job, a salary or a promotion. Hiring depends on the market, your portfolio, your interviews and luck.
- It does not claim that any technology makes you immune to AI automation. The goal is to become an engineer who can design, build, test, deploy, secure and maintain real systems, and who uses AI tools well. That is a better position than the alternative, but it is not a guarantee.
- It does not teach everything. Machine-learning research, model training, Kubernetes and many advanced topics are deliberately postponed. See the "Core vs optional vs postpone" section in the trackers.

## How the document is organised

1. The prerequisite assessment, so you can skip what you already know (only if you can prove it).
2. Phases 0 to 17, in the order you should learn them. Each phase has explained concepts, a resource table, verification notes, exercises and a checkpoint.
3. Week plans, placed after the phase content they belong to.
4. Seven projects, increasing in difficulty.
5. How to learn with Claude and other AI tools, and the career strategy for India.
6. Trackers: the 24-week calendar, revision schedule, self-assessment matrix and job-readiness checklist.
7. The full source list.

## The 24-week map at a glance

| Weeks | Focus | Learning tier | Output |
|---|---|---|---|
| 1 | Developer foundations, setup, assessment | Gap-fill | Clean environment, assessment result |
| 2 | JavaScript core mechanics, async, event loop | Revision | JS exercises with tests |
| 3 | TypeScript fundamentals, generics, typing APIs | Gap-fill | Typed utility library |
| 4 | HTML/CSS/HTTP gap-fill; React revision start | Revision | Accessible responsive page |
| 5-6 | React depth, Next.js App Router, Vercel AI SDK | Beginner to solid | Project 1: admin dashboard |
| 7-8 | Node.js, Express, auth, RBAC, API architecture | Beginner to solid | Project 2: order management API |
| 9 | PostgreSQL (relational/ACID) and MongoDB (docs) | Beginner to solid | Schema, queries, indexes, transactions |
| 10-11 | Python from scratch (syntax, OOP, async, uv/ruff) | From scratch | Project 3: Python data utility |
| 12-14 | FastAPI from scratch, SQLAlchemy 2.0, Alembic | From scratch | Project 4: FastAPI order backend |
| 15 | AI foundations, Reasoning models, Caching, LLM APIs | From scratch | Working LLM scripts, streaming chat |
| 16-17 | Embeddings, pgvector, Hybrid RAG, Reranking | From scratch | Project 5: AI document assistant |
| 18-19 | Agentic AI, Model Context Protocol (MCP), LangGraph | From scratch | Project 6: refund workflow assistant |
| 20 | Architecture, testing, OWASP & AI security | From scratch | Security review of your own code |
| 21 | Docker, Linux, AWS deployment, CI/CD | From scratch | Containerised, deployed service |
| 22-23 | Production AI engineering, Langfuse tracing | From scratch | Project 7: production portfolio app |
| 24 | System design, interviews, applying | Capstone | Resume, portfolio, mock interviews |

> **Tip:** Start applying for roles earlier than week 24. The career strategy section gives concrete triggers, for example after Project 4 for backend roles and after Project 5 for AI application roles.

## Weekly rhythm (suggested)

| Day | Time | Activity |
|---|---|---|
| Monday | 1 hour | Read the week plan, watch the main video at 1x or 1.25x |
| Tuesday | 1.5 hours | Hands-on exercises |
| Wednesday | 1 hour | Revision of earlier topics, short self-test |
| Thursday | 1.5 hours | Build the week's deliverable |
| Saturday | 3 hours | Build session, no videos, only docs and debugging |
| Sunday | 1.5 hours | Checklist, notes, mistakes log, weekly review with Claude |

If you miss a week, do not try to double up. Use the slower-track plan in the trackers section.
