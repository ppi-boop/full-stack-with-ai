# Output format contract for every part file

Write ONLY to `/Users/tagline/Documents/fullstack-ai-roadmap/parts/<your-file>.md`. A converter turns these into DOCX + PDF, so use ONLY this Markdown subset:

- Headings: `#` (Part/Phase title, only once at top of each phase), `##`, `###`, `####`. Do not skip levels.
- Paragraphs, `- ` bullets (one nesting level max, indent 2 spaces), `1. ` numbered lists, `- [ ] ` checkboxes.
- Tables: standard pipe tables with a header row. Keep cells short (no line breaks; no pipes inside cells). Links inside cells are fine.
- Fenced code blocks (```), with a language tag. Inline code with backticks. **bold**, *italic*.
- Callouts: a line starting with `> ` (blockquote). Start with a bold label: `> **Honest note:**`, `> **Tip:**`, `> **Warning:**`, `> **Outdated?:**`.
- Links: `[text](https://...)` only, full URLs. No raw HTML, no images, no footnotes, no nested tables, no emoji.
- Every topic carries one of three labels in bold at its start: **[Must learn now]**, **[Learn during projects]**, **[Learn later if needed]**.
- Plain, simple English. Define jargon at first use with an everyday analogy. Write for a React/Next.js developer who knows JS but is rusty on fundamentals.

## Required sections per PHASE file (in this order)

```
# Phase N — Title
## Why this phase matters (3-5 sentences, honest)
## Prerequisites and "skip test" (what the learner must be able to DEMONSTRATE to skip)
## Concepts explained
### <topic>  (label, plain-English explanation, analogy, small code example, common mistake, interview questions)
## Resource table  (exactly these 7 columns: Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task)
## Verification notes (for each video: what you actually checked, and anything NOT verified: duration, language, availability)
## Hands-on exercises
## Checkpoint (practical questions: explain / modify code / debug / write tests; plus "ready to move on when ...")
```

## Required structure per WEEK (put weeks AFTER the phase content they belong to, under `## Week plan`)

```
### Week N — Title  (estimated hours: X)
**Learning objectives** (bullets)
**Topics and subtopics** (bullets, in recommended order, with labels)
**Small prerequisite concepts** (bullets)
**Reading** (links)  |  **Video** (links, with title/channel/language/duration-or-"duration not verified")
**Hands-on exercises** (numbered)
**What you must build** (concrete deliverable)
**Completion checklist** (- [ ] items)
**Self-test** (3-5 questions)
**Common mistakes** (bullets)
**Ready to continue when** (observable criteria)
**Slower-track option** (what to cut/stretch if this week took longer)
```

## Week allocation (24 weeks, ~8-10 h/week) — DO NOT deviate, other authors rely on it
- W1 Phase 0 + prerequisite assessment
- W2 Phase 1 (JavaScript gap-fill: closures, this, event loop, async, modules, testing)
- W3 Phase 2 (TypeScript)
- W4 Phase 3 (HTML/CSS/browser/HTTP gap-fill) + start Phase 4 React review
- W5 Phase 4 (React deep gaps) + Phase 5 start (Next.js App Router)
- W6 Phase 5 finish + Project 1 (admin dashboard) build/finish
- W7 Phase 6 (Node/Express backend) + Project 2 start
- W8 Project 2 finish (auth, RBAC, validation, tests)
- W9 Phase 7 (PostgreSQL + MongoDB data modeling, SQL, indexes, transactions)
- W10 Phase 8 Python part 1 (syntax to functions, collections, files, errors)
- W11 Phase 8 Python part 2 (OOP, typing, async, pytest) + Project 3
- W12 Phase 9 FastAPI part 1 (routes, Pydantic, DI, structure)
- W13 Phase 9 FastAPI part 2 (PostgreSQL, SQLAlchemy/SQLModel, Alembic, auth/RBAC)
- W14 Phase 9 finish (tests, logging, background tasks, WebSockets/streaming) + Project 4 finish
- W15 Phase 10 + Phase 11 (AI foundations, LLM APIs)
- W16 Phase 12 (embeddings, pgvector, RAG)
- W17 Project 5 (AI document assistant) + RAG evaluation
- W18 Phase 13 (agent concepts + LangGraph)
- W19 Project 6 (order/refund workflow assistant)
- W20 Phase 14 (architecture, testing, security)
- W21 Phase 15 (Linux, Docker, AWS, CI/CD)
- W22 Phase 16 (production AI engineering) + Project 7 start
- W23 Project 7 deploy, monitoring, docs, security hardening
- W24 Phase 17 (system design, interview prep), portfolio, resume, apply strategy

## Honesty and verification rules (non-negotiable)
- Every URL you include must have been opened or fetched by you in this session and confirmed to resolve to the stated content. Official docs: fetch the page. YouTube: verify with BOTH
  `curl -s "https://www.youtube.com/oembed?url=<VIDEO_OR_PLAYLIST_URL>&format=json"` (returns real title + channel) AND, for single videos, `curl -sL "<watch url>" | grep -o '"lengthSeconds":"[0-9]*"' | head -1` for duration. Playlists: oembed title/channel only; say duration not verified.
- Never guess a video ID. Find candidates with WebSearch, then verify each with the commands above. If oembed fails or the title does not match the topic, DROP it.
- If you cannot verify a video for a topic, write exactly: "No video verified for this topic; use the official documentation above." Do not fabricate.
- Hindi resources: only include if verified, label language "Hindi" (or "Hinglish") from the title/channel evidence; otherwise say language not verified.
- Fast-changing tools (Next.js, FastAPI, OpenAI/Anthropic APIs, LangGraph, pgvector, AWS): prefer docs fetched today; flag anything in videos that may be outdated.
- Research date to use in the document: 2026-10-09.
- At the very end of each file add `## Sources` listing every URL you actually opened.
- Keep each phase's resources limited: 1-2 videos max per topic cluster, no overlapping full courses.
- No guarantees about jobs/salary. Be direct and honest.
- Be thorough: this is a study handbook. Do not pad, but do not skip any bullet in your assigned phases of MASTER_PROMPT.md. Each phase file should be long and detailed (typically 3,500-7,000 words including week plans and project specs).
