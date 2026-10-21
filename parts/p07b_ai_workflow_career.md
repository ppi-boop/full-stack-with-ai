# Learning with Claude and AI

## Why this section matters

You have a very strong tutor available all day. Used well, it makes you faster and helps you understand more. Used badly, it writes code you cannot explain, and that shows in the first interview or the first production bug. The 2025 Stack Overflow Developer Survey (blog summary opened 2026-10-09) reports that about 80 percent of developers now use AI tools, while trust in the accuracy of AI output fell to about 29 percent, down from 40 percent. Developers use it a lot and do not fully trust it. That is the right attitude for you too: use it often, verify it always. The goal of this roadmap is a person who can design, build, test, deploy and secure AI-powered apps independently. Every rule below serves that goal.

> **Honest note:** Anthropic's own Claude Code guide says the same thing in different words: give the tool a way to verify its work (tests, build, screenshots), and "if you can't verify it, don't ship it". Source: [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices), opened 2026-10-09.

## The core rules

### Explanation before code

**[Must learn now]** Ask for the idea first, then the code. A good order is: (1) explain the concept with an everyday analogy, (2) show the smallest example, (3) ask you a question to check understanding, (4) only then give or review real code. If you start with "write me X", you get an answer without the model in your head. Practise the habit: before asking for code, write two sentences in your own words about how you think it should work. Then ask Claude to find the gaps in your two sentences.

### Hints, not full solutions

**[Must learn now]** Use a hint ladder. Stay on each level for at least 10 to 15 minutes of your own effort before climbing.

1. Level 0: you try alone (25 minutes, with docs and the debugger).
2. Level 1: ask which concept or doc page is relevant. No code.
3. Level 2: ask for a pointer to where the bug likely is ("check the dependency array", "look at the second query").
4. Level 3: ask for pseudo-code of the approach.
5. Level 4: ask for one small snippet for just the stuck part.
6. Level 5: full solution, only to study after you finished your own, and then close it and retype it from memory.

If you are always at Level 5, you are not learning; you are copying.

### Break features into small tasks

**[Must learn now]** Big prompts produce big, unreviewable diffs. Split a feature into steps you can test in under 30 minutes each: model, route, validation, happy-path test, error path, UI. Claude Code's guide recommends the same four phases: explore, plan, implement, commit, and says to skip the plan only when you could describe the diff in one sentence (same source as above). Ask for the plan first, edit the plan yourself, then implement one step at a time and run the tests after each step.

### AI code review and trade-offs

**[Must learn now]** Ask Claude to review your code, not to write it. Ask for trade-offs, not "the best way": "give me two designs, with when each is wrong". Ask it to argue against your design. Treat answers as a second opinion. A fresh conversation reviews more honestly than the one that wrote the code (the Claude Code guide describes a writer/reviewer pattern with separate sessions for this reason). Tell the reviewer to flag only real problems (bugs, security, requirements) so you are not pushed into needless complexity.

### Generate tests and edge cases

**[Must learn now]** AI is very good at listing edge cases you forgot: empty input, huge input, unicode, negative numbers, duplicates, concurrent calls, timeouts, permission failures. Ask for a list of cases first, choose the ones that matter, write one test yourself, then let AI draft the rest in the same style. Run the tests and also break the code on purpose to see them fail. A test that never fails proves nothing. Do not accept tests that mock away the thing you wanted to test.

### Systematic debugging

**[Must learn now]** Give the full error, the smallest code that reproduces it, what you expected, what happened, and what you already tried. Ask for hypotheses ranked by likelihood and a way to test each, before any fix. Then test one hypothesis at a time with logging, a debugger or a failing test. Ask for root cause, not a patch that hides the error. If two rounds of suggestions have failed, start a clean conversation with a better description; long conversations full of failed ideas make answers worse (also noted in the Claude Code best practices).

### Verify AI code against official docs

**[Must learn now]** Models can write code for old library versions, invented function names, or deprecated patterns. This is a real risk in this roadmap because Next.js, FastAPI, LangGraph, pgvector, and the Anthropic/OpenAI SDKs change fast. Rule: for every API you did not know before, open the official docs page and confirm the function name, arguments and version. Ask Claude to cite the doc page or section, then open it yourself. If the model cannot point to a doc, treat the code as a guess. Pin versions in `package.json` and `pyproject.toml` and read release notes before upgrading.

### Check security and dependencies

**[Must learn now]** AI code often skips authorization checks, trusts user input, logs secrets, or suggests packages you have never heard of. Before accepting code: run the security review prompt below, search for hard-coded keys, run `npm audit` or `pip-audit`, check that every new package exists, is maintained, and is the one you intended (watch for look-alike names), and keep secrets out of prompts: never paste real API keys, production data, customer data or private company code into a tool you are not allowed to use for that data. Follow your employer's policy; your day job code may not be allowed in any external AI tool.

### Rebuild from memory

**[Must learn now]** Once a week choose one feature you built with help (a login route, a custom hook, a RAG retrieval function). Close everything, and rebuild it from a blank file using only official docs. Where you get stuck is exactly what you do not know yet. Add it to the mistakes log. This is the single best antidote to the illusion of understanding.

### Avoid dependence

**[Must learn now]** Simple guardrails:

- Struggle first: at least 20 to 25 minutes before asking.
- Two "AI-off" blocks per week (for example Saturday morning), using only docs and your editor.
- Typing rule: for concepts you are learning this week, type the code yourself, do not paste.
- Explain-back rule: if you cannot explain a line to a friend, you cannot keep it.
- Weekly question: "What could I do this week that I could not do last week, without AI?"

### Track what you can independently explain and implement

**[Must learn now]** Keep a one-page ledger (the self-assessment matrix in the trackers file has a full version). For each skill record three columns: can I explain it (no notes), can I implement it (no AI), can I debug it. Update it each Sunday. Evidence beats feelings: link the commit or note.

## When boilerplate is fine and when to implement it yourself

**[Must learn now]** Rule of thumb: let AI write what you have already mastered and what is repetitive; write yourself what you are trying to learn and what protects users or money.

| Task | AI boilerplate OK? | Reason |
|---|---|---|
| Project scaffolding, config files, Dockerfile first draft, eslint config | Yes, then read every line | Low learning value, easy to verify by running |
| CRUD routes after you wrote the first one by hand | Yes | Repeating a pattern you already own |
| Test data, fixtures, seed scripts | Yes | Repetitive and low risk |
| Tailwind or CSS styling tweaks | Yes | Easy to check visually |
| README drafts, docstrings | Yes, but edit for truth | Wording help only |
| Refactors with tests already passing | Yes | Tests verify behaviour |
| Authentication, sessions, password hashing, JWT handling | Write the core yourself; use AI only to review | Security and learning value are both high |
| Authorization and ownership checks | Write yourself | Most common serious bug class |
| Database schema, indexes, transactions, migrations | Write yourself, AI reviews | You must be able to reason about data |
| Chunking, embeddings, retrieval, prompt construction | Write the first version yourself | Core of your AI skill |
| Tool schemas, agent state machine, approval logic, idempotency | Write yourself | Core of agentic engineering |
| Evaluation dataset and metrics | Write the cases yourself | You must know what "good" means |
| Anything you could not explain in an interview | No, until you can | The interview is the test |

Concept to remember: **vibe coding** (accepting generated code without reading it) is fine for throwaway experiments and bad for anything you ship or must explain. In the 2025 Stack Overflow survey summary, about 72 percent of developers said vibe coding is not part of their professional work (blog summary opened 2026-10-09).

## Reusable prompts

Copy these into a notes file. Replace the text in square brackets. Each prompt is built to make Claude teach rather than only produce. Use a fresh chat per prompt when you can, and paste only the code needed (not secrets).

### Prompt 1 — Learn a topic

```text
I am a full-stack developer (JavaScript, React, Next.js, some Node.js and MongoDB) learning [TOPIC]
as part of a 24-week roadmap towards Python/FastAPI and AI application engineering.
My current level in this topic: [none / basic / some experience: describe].

Teach me in this order, and stop after each numbered step so I can answer:
1. A plain-English explanation with an everyday analogy (max 150 words).
2. The 5 prerequisite concepts I must already know. Ask me a one-line question about each so you can find gaps.
3. The smallest runnable example (under 25 lines) and explain every line.
4. Two common beginner mistakes, with a tiny example of each.
5. Three questions to check my understanding. Wait for my answers and correct them honestly.
6. A practice task that takes 30-45 minutes, without giving the solution.
7. The official documentation pages I should read, with section names. Tell me if you are unsure a page exists.
Do not give me a long lecture. If something changed in recent versions of [TOOL/VERSION], say so and tell me to verify in the docs.
```

### Prompt 2 — Understand existing code

```text
Here is code from my project (secrets removed): 
[PASTE CODE]
Context: [what the app does, framework and versions].
Explain it for someone who knows JavaScript and React but is new to [Python/FastAPI/SQLAlchemy/etc.]:
1. What is the overall purpose in 2 sentences?
2. Walk through the execution flow step by step, naming each function called and when.
3. List every external dependency or assumption (env vars, database tables, other files).
4. Point out anything unusual, risky, or outdated, and why.
5. Draw a small text diagram of the data flow.
Then ask me 3 questions to test whether I understood, and wait for my answers.
Do not rewrite the code unless I ask.
```

### Prompt 3 — Hint without full solution

```text
I am practising [PROBLEM / FEATURE]. I must write the solution myself.
My attempt so far: [PASTE CODE OR DESCRIBE]. What I expected: [..]. What happens: [..]. Time spent: [N] minutes.
Give me hints in levels. Start with Level 1 only: name the concept or documentation topic I should review. Do not show code.
I will reply "next hint" if I need more. The levels are:
Level 1 concept, Level 2 where the problem likely is, Level 3 pseudo-code, Level 4 one small snippet for only the stuck part.
Never give the full solution unless I write "show full solution". When I do, explain why each part exists and then give me a variation exercise.
```

### Prompt 4 — Debug an error

```text
Help me debug systematically. Do not jump to a fix.
Environment: [OS, Node/Python version, framework versions].
What I am trying to do: [..]
Expected: [..]   Actual: [..]
Full error / stack trace:
[PASTE]
Smallest code that reproduces it:
[PASTE]
What I already tried: [..]
Please:
1. Explain in plain English what the error message means.
2. List the 3 most likely root causes, ranked, with one cheap check I can run for each (log line, test, command).
3. Wait for my results, then narrow down.
4. When we find the root cause, explain why it happened, give the minimal fix, and write one regression test that would have caught it.
5. Tell me what I should log or assert so I find this class of bug faster next time.
```

### Prompt 5 — Architecture review

```text
Act as a senior engineer reviewing my design. Be honest and direct; do not just praise.
Project: [what and for whom]. Scale now / in 12 months: [users, data size, requests per second estimates].
Stack: [..]. Team size: [..]. Deadline/budget: [..].
My design: [DESCRIBE OR PASTE DIAGRAM / FOLDER STRUCTURE / SCHEMA / API LIST]
Review for: 1) requirement gaps, 2) data model and indexes, 3) auth and authorization, 4) failure modes and what happens when a dependency is down,
5) security, 6) cost and operational complexity, 7) things I over-engineered.
For each finding give: severity (high/medium/low), why it matters, and the simplest fix.
Then list two alternative designs, and when each would be the wrong choice. End with the 3 things I should do first.
If you are unsure about a framework fact, say so and tell me which doc to check.
```

### Prompt 6 — Generate or review tests

```text
Here is the function/endpoint and what it should do:
[PASTE CODE + REQUIREMENTS]
Test framework: [pytest / Vitest / Jest / React Testing Library].
1. First, list test cases in a table: case name, input, expected output, why it matters. Include happy path, validation errors, boundary values, empty input, permission failures, duplicate/idempotent calls, and concurrency or timeout where relevant.
2. Wait for me to choose which to implement.
3. Write tests for the ones I choose. Do not mock the code under test. Mock only external services (HTTP, LLM calls, email).
4. Tell me which bug each test would catch, and suggest one small mutation of the code that should make a test fail so I can verify the tests are real.
If I paste my own tests instead, review them: what is missing, which are brittle, which assert nothing useful.
```

### Prompt 7 — Security review

```text
Do a security review of this code as if it will run in production with real users.
Context: [framework, authentication method, what data is sensitive, who the users are].
Code: [PASTE FILES; secrets removed]
Check against: authentication and session handling, authorization / ownership checks (IDOR), input validation, SQL/NoSQL injection, XSS, CSRF and CORS, cookie flags, secrets in code or logs,
rate limiting and abuse, file upload handling, error messages leaking information, dependency risks, and (if AI is used) prompt injection, cross-user data leakage in retrieval, and unsafe tool execution.
Output a table: finding, where (file/line), severity, how an attacker would exploit it, the fix. Then give a prioritised top-5 fix list.
Do not invent vulnerabilities. If the code is fine in an area, say so. Mark anything you cannot judge without seeing more code.
```

### Prompt 8 — Project milestone planning

```text
I am building [PROJECT NAME]: [one-paragraph description]. I can work [N] hours per week for [N] weeks, with a full-time job.
Stack: [..]. What I already know well: [..]. What is new to me: [..].
Break this into milestones. For each milestone give: goal, tasks (each under 90 minutes), definition of done (observable and testable), the test I will write, the risk, and what I can cut if I fall behind.
Rules: build a thin end-to-end slice first; add auth, validation and tests early, not at the end; flag tasks where I should write the core code myself instead of using AI; keep a "later" list for nice-to-haves.
End with the first 3 tasks for this week, and questions you need answered before planning further.
```

### Prompt 9 — Interview practice

```text
Be my technical interviewer for a [role: Full-Stack Engineer with AI / Python FastAPI Backend Engineer / GenAI Application Engineer] position in India.
My background: [years, stack, projects]. Mode: [project deep-dive / JS+React / Python / SQL / FastAPI / AI+RAG+agents / system design / DSA].
Ask ONE question at a time. Start easy and increase difficulty based on my answers. Wait for my answer before continuing.
After each answer give: a score from 1 to 5, what was correct, what was missing or wrong, and a model answer in under 120 words. If I am vague, ask a follow-up like a real interviewer.
For project deep-dives, probe: why this choice, what failed, how it was tested, security, scaling, and what I would change.
After 10 questions, give a summary: strengths, weak topics, and a 7-day practice plan. Do not be gentle; be accurate.
```

### Prompt 10 — Weekly progress review

```text
Be my learning coach for the week that just ended. Here is my data:
Week number / phase: [..]. Planned hours: [..]. Actual hours: [..].
What I completed: [list]. What I did not complete: [list].
What I can explain without notes: [list]. What I can implement without AI: [list]. What I only got working with AI help: [list].
Mistakes and bugs this week (with root causes): [list]. Questions still open: [list].
Please: 1) tell me honestly whether I am ready to continue using the "ready to continue when" criteria: [PASTE FROM THE WEEK PLAN],
2) list the top 3 gaps, 3) give me 5 revision questions for tomorrow, 4) suggest what to cut or stretch next week using a slower-track option if I am behind,
5) warn me about signs of over-reliance on AI that you see in my notes. Keep it under 300 words and be direct.
```

## Working with Claude Code (optional, after Week 6)

**[Learn during projects]** If you use an agentic tool such as Claude Code, the documented habits are the same as the learning rules above. A `CLAUDE.md` file holds short project rules (commands, code style, test runner) that load every session; keep it short and prune it, because a bloated file gets ignored. Use plan mode to explore and plan before editing. Give it tests or a build to run so it can check itself. Clear context between unrelated tasks. Use a separate session or sub-agent to review a diff. All from [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices) (opened 2026-10-09). For prompt craft see the [prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and the note on defining success criteria and evaluations first ([Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests)); both are pages you will use again in Phase 11 and Phase 16.

> **Warning:** Agentic coding tools can edit many files and run commands. Use version control, review every diff, keep secrets out of the working directory when possible, and do not give such tools production credentials.

## Weekly AI-learning routine (15 minutes on Sunday)

- [ ] Run Prompt 10 with your real data.
- [ ] Do one blank-page rebuild of a feature from this week.
- [ ] Update the "explain / implement / debug" ledger.
- [ ] Add every AI mistake you caught (wrong API, insecure code, invented function) to the mistakes log; this trains your suspicion.
- [ ] Decide next week's two AI-off blocks.

## Verification notes

All three Anthropic documentation pages were fetched on 2026-10-09 and read. The Stack Overflow numbers (80 percent use, 29 percent trust, 72 percent not vibe coding) come from the Stack Overflow blog post summary of the 2025 survey. Different press summaries of the same survey quote slightly different percentages for the "almost right" frustration, so no exact figure for that item is given here. The prompts are original templates written for this handbook and are not from a vendor guide. No videos are included in this section.

# Career Strategy for India

## Honest framing first

This section separates three things: **evidence** (a source I opened, with date), **interpretation** (my reading of the evidence), and **speculation** (a guess about the future, labelled). Nothing here is a promise of a job, an interview or a salary. Hiring depends on your experience, the city, the company, the economy and luck. I could not open Naukri, Indeed or LinkedIn listing pages directly (Naukri returned HTTP 403 and several other listing pages were closed or removed), so the job-description evidence below comes from company career pages, Wellfound, Cutshort, and job-aggregator pages that I could open. A small sample of listings is a sample, not a survey. Salary figures are deliberately left out: the only salary data I found was on aggregator pages where most postings do not disclose pay, which is not a reliable basis.

## Evidence: the market picture (opened 2026-10-09)

| Claim | Source and date | Quality note |
|---|---|---|
| White-collar hiring up 5 percent year on year in July 2026; AI/ML roles up 33 percent; IT/software services up 6 percent; hiring for up to 3 years of experience up 6 percent | Naukri JobSpeak July 2026, as reported by [Angel One](https://www.angelone.in/news/stocks/info-edge-s-naukri-jobspeak-report-white-collar-hiring-up-5-in-july-2026-ai-ml-roles-lead-growth), published 3 Aug 2026 | Secondary report of a private Info Edge index built from its own listings. Direction is useful; it is not a government statistic. The Naukri original returned 403 to me. |
| India job postings rose 1.2 percent in July 2026 but software development postings fell 18 percent and IT infrastructure/support postings fell 24 percent in the period the article describes | Indeed data, reported by [CXOToday](https://cxotoday.com/research/indias-job-postings-rebound-8-3-yoy-snapping-three-month-decline/), 26 Aug 2026 | Reported via a news site, not Indeed Hiring Lab directly. The article gives the period loosely ("past three months"); read as a trend signal. |
| 349 job titles (about 6.6 percent of titles tracked) had meaningful AI mentions in the March 2026 quarter; non-tech occupations are 42 percent of those titles | Same CXOToday article citing Indeed | Same caveat. AI mentions are spreading beyond tech roles. |
| Tech-sector headcount grew about 2.3 percent in FY26 (59.5 lakh vs 58.2 lakh); industry still a net hirer; Nasscom estimates AI revenue of 10 to 12 billion US dollars | Nasscom Annual Strategic Review 2026 as reported by [The Core](https://www.thecore.in/business/ai-dampens-tech-hiring-in-india-23-growth-in-fy26-vs-fy25-859053), 24 Feb 2026 | Industry body figures via a news site. |
| 40 percent of surveyed employers prefer demonstrable AI skills or certifications over degrees; demand centres on cloud, generative AI and LLMs, MLOps and deployment, data analytics; software engineering roles prioritise Agile, communication, APIs, Git | Nasscom and Indeed report "India's AI Talent Inflection Point", as reported by [CXOToday](https://cxotoday.com/research/skills-over-degrees-nasscom-indeed-report-reveals-indias-evolving-ai-hiring-landscape/), 21 May 2026 | Employer survey and posting analysis, secondhand; sample details not given in the article. |
| 80 percent of developers use AI tools; Python usage up 7 percentage points in a year; Docker 71 percent, PostgreSQL 56 percent, JavaScript 66 percent, Python 58 percent, React 45 percent, Node.js 49 percent, TypeScript 44 percent, FastAPI 15 percent, Next.js 21 percent usage among all respondents | [Stack Overflow Developer Survey 2025](https://stackoverflow.blog/2025/07/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/) and its [technology page](https://survey.stackoverflow.co/2025/technology) | Global, self-selected respondents, not India-specific. Shows what developers use, not what employers pay for. |

Interpretation (mine): the evidence points the same way across sources. AI/ML hiring is growing faster than overall hiring, while general software postings are soft. That does not mean general full-stack work is disappearing (it is still the larger market, and my evidence cannot quantify it). It does suggest that adding demonstrable AI-application skills on top of solid engineering is a sensible way to stand out. **Speculation:** whether the AI-hiring growth continues, and whether it favours experienced engineers over new entrants, cannot be known from this data.

> **Warning on low-quality statistics:** while researching, I saw claims like "freshers with AI skills earn 56 percent more", "20 to 25 percent of freshers will face longer job hunts", and "58 percent of hiring managers reject qualified candidates for poor communication". These appeared on education/blog/SEO pages with no traceable primary source, and I did not rely on them. Treat any such statistic the same way unless it links to a named survey with sample size and date.

## Evidence: what job descriptions recurringly ask for

Sample of postings I could open (2026-10-09). Posting dates are as shown on the page; "not shown" means the page did not state one.

| Role family | Listing and source | Date | Experience | Skills named |
|---|---|---|---|---|
| Full-Stack + AI | [Full-Stack AI Engineer, Beroe, India remote](https://www.beroeinc.com/careers-vacancies/full-stack-ai-engineer/) | 28 Sep 2026 | fresh graduates to experienced | React, Next.js, Python, Node.js, LangChain/LlamaIndex/Haystack, uses AI to write and test code |
| Full-Stack + AI | [Full Stack Engineer, EngineerBabu, Indore](https://jobs.recooty.com/engineerbabu-it-services-pvt-ltd-/full-stack-engineer-en334) | 1 Jun 2026 | 1 to 4 years | React/Next.js, Node.js, PostgreSQL/MongoDB, REST, AWS/GCP basics, OpenAI/Anthropic APIs, Cursor/Copilot, Git, CI/CD |
| Full-Stack + AI | [Senior Full Stack Engineer, Arbor, India remote](https://jobs.645ventures.com/companies/arbor-2-c1cd2b7f-56ad-4ca3-ad99-6f2ac9e0fb62/jobs/52964763-senior-full-stack-engineer) | about 6+ months old, page says no longer accepting | 2 to 10 years | React, Next.js, Python, Node.js, AI/ML in production |
| Python Backend | [Python Backend Developer, Deloitte, remote Bangalore](https://southasiacareers.deloitte.com/job/Bengaluru-Senior-Associate-Engineering-Foundry-&-Managed-Services-Bengaluru-Engineering-as-a-Service-Op/50759144/) | not shown | 4 to 8 years | Python, FastAPI, PostgreSQL, Docker, AWS, Go; Kubernetes good-to-have |
| GenAI App Engineer | [Generative AI Engineer, Gravity Engineering Services, many cities (Cutshort)](https://cutshort.io/job/Generative-AI-Engineer-Bengaluru-Bangalore-Delhi-Gurugram-Noida-Ghaziabad-Faridabad-Hyderabad-Mumbai-Chennai-Pune-Gravity-Engineering-Services-Pvt-Ltd-tKcXpfK5) | 5 Oct 2026 | 1 to 10 years | LangChain, RAG, vector database, prompt engineering, LlamaIndex |
| Agentic AI | [Agentic AI Engineer, Fx31 Labs (Wellfound)](https://wellfound.com/jobs/4691299-agentic-ai-engineer) | about 4 weeks old at fetch | 4 years | Python, LangGraph/LangChain/Semantic Kernel, RAG with hybrid retrieval, reranking, chunking, vector DBs, memory and state management, Azure/AWS/GCP, GitHub, CI/CD |

Counts from job aggregator pages (page date 9 Oct 2026, from [Weekday backend jobs](https://www.weekday.works/jobs/backend-developer-jobs-in-india), [Weekday ML/AI jobs](https://www.weekday.works/jobs/ml-ai-engineering-jobs) and [Weekday DevOps jobs](https://www.weekday.works/jobs/devops-engineer-jobs-in-india-18)):

| Page | Total shown | Experience filter counts shown | Note |
|---|---|---|---|
| Backend developer jobs, India | 1,020 | 0 to 1 yr: 25; 2 to 3: 108; 4 to 6: 263; 7 to 10: 127; 11+: 10 | The filters sum to 533, so they cover only part of the listings |
| ML / AI / GenAI engineering jobs | 3,134 | 0 to 1 yr: 80; 2 to 3: 492; 4 to 6: 742; 7 to 10: 291; 11+: 124 | The filters sum to 1,729. Most common tags in the 20 visible listings: Machine Learning, LLM, RAG, MLOps, Python |
| DevOps engineer jobs, India | 2,486 | most common bands: 4 to 6 yrs (600) and 7 to 10 yrs (327) | Mostly hybrid or on-site; skill tags: DevOps, Cloud, Python, AWS |

My calculation from those filter counts: the 0 to 1 year band is about 5 percent of the filtered backend listings (25 of 533) and about 5 percent of the filtered ML/AI listings (80 of 1,729). Caveats: aggregator data, partial filters, one platform, one day. **Interpretation:** most listings on this platform ask for experience. For you, with working experience as a full-stack developer, this is useful: you can apply as an experienced developer who is adding Python and AI skills, not as a fresher. **Speculation:** other portals may show a different mix.

Recurring requirements I can honestly state from the sample above:

1. Python is named in 4 of the 6 listings (Beroe, Arbor, Deloitte, Fx31 Labs); FastAPI is named only in the Deloitte listing. The EngineerBabu and Gravity listings, as shown on the page, do not name Python.
2. Retrieval-augmented generation (RAG) with vector databases appears in the GenAI and Agentic listings (Gravity, Fx31) and indirectly in Beroe (LlamaIndex/Haystack/LangChain).
3. LLM orchestration frameworks (LangChain, LangGraph, LlamaIndex, Haystack) are named in 3 of 6 (Beroe, Gravity, Fx31 Labs). Interpretation: learn the underlying ideas, and one framework, rather than all of them (this roadmap's Phase 13 does exactly that).
4. Cloud and delivery basics (AWS/Azure/GCP, Docker, CI/CD, Git) appear in 3 of 6 (EngineerBabu, Deloitte, Fx31 Labs).
5. React/Next.js plus Node.js appears in the full-stack AI listings, so your existing stack is a strength there, not something to throw away.
6. SQL databases (PostgreSQL named in Deloitte and EngineerBabu) and REST APIs are baseline.
7. "Uses AI tools to write, test and debug code" is stated explicitly by Beroe and EngineerBabu (Cursor/Copilot). Interpretation: AI-assisted work is becoming expected, which makes the ability to verify and explain AI-written code more important, not less.
8. Evaluation, tracing and monitoring of AI systems were not prominent in the six listings I could open. Search-result snippets for other listings (not opened by me, so not used as evidence) suggested they appear in more senior roles. This roadmap covers them in Phase 16 because production quality is what separates a demo from a product; treat it as differentiation, not as a proven hiring requirement.

What I could not verify: Kubernetes, Terraform and Kubernetes-heavy DevOps requirements. The DevOps individual listings that I tried to open were removed, closed, or blocked. The aggregator tags (DevOps, Cloud, Python, AWS) and the heavy lean towards 4 to 10 years of experience are the only DevOps evidence I have. Search snippets repeatedly mentioned AWS, Terraform, Kubernetes, CI/CD and monitoring, but I did not open those pages.

## Role comparison

Prerequisite phases refer to this handbook's phase numbers. "Typical entry point from your background" is my interpretation, not data.

| Role | What you do | Prerequisites (phases) | Strongest evidence in listings I opened | Fit with your background | Not needed early |
|---|---|---|---|---|---|
| Full-Stack Engineer with AI integration | Build product UIs and APIs, add chat, search, summarisation, structured extraction | 1 to 7, 11, 12, 14, 15 basics; Python optional | Beroe, EngineerBabu | Strongest. You already have React, Next.js, Node, MongoDB, auth. | Kubernetes, fine-tuning, multi-agent systems |
| Python / FastAPI Backend Engineer | Design APIs, databases, queues, auth, deployment | 0, 7 to 9, 14, 15; 17 | Deloitte | Good, needs Python and PostgreSQL depth. Your Node backend knowledge transfers. | LLM frameworks, GPU topics |
| GenAI Application Engineer | RAG, LLM APIs, evaluation, guardrails, cost control | 8 to 12, 14, 16 | Gravity, Beroe | Good once Projects 4 and 5 are done | Training models, advanced maths |
| Agentic AI Engineer | Tool-using workflows, state, human approval, reliability | 8 to 13, 14, 16 | Fx31 Labs (asks 4 years) | Later step. Needs Project 6 and production habits. Listings tend to want proven experience. | Multi-agent frameworks beyond one |
| DevOps / Cloud Engineer | CI/CD, infrastructure, monitoring, cost, reliability | 0, 15, strong Linux, networking, security | Aggregator counts only | A different career track. Phase 15 gives the base; real DevOps needs on-call and infrastructure experience. | Everything application-AI specific |

> **Honest note:** "Agentic AI Engineer" is a young title. In the one listing I could open, the required skills are Python, a graph/orchestration framework, RAG, and cloud basics with 4 years of experience. It is mostly strong backend engineering plus LLM-workflow discipline. That is why this roadmap puts it after backend, RAG and security.

## Building on React and Next.js

**[Must learn now]** Do not restart as a beginner. Position yourself as "a frontend-strong full-stack engineer who builds AI features end to end". Things that are naturally yours:

- Streaming chat and answer UIs (server-sent events, partial rendering), loading, error and empty states.
- Citation display, document viewers, approval dashboards for staff (Project 6 needs one).
- Evaluation dashboards for retrieval quality and cost, built with the same React skills.
- Next.js Route Handlers for thin backends, with a FastAPI service for AI workloads when you need Python libraries or heavy background work.

This is interpretation, not evidence, but it is a coherent story that matches the Full-Stack AI listings above.

## Best portfolio projects

**[Must learn now]** Use the handbook's seven projects, but present them as three stories:

1. **Backend credibility (Projects 2 and 4):** an order-management API with auth, roles, migrations, tests and docs. Shows the basics every backend listing asks for.
2. **AI application credibility (Project 5):** a document assistant with per-user access control, citations, an evaluation set with real numbers, and cost tracking.
3. **Production and agent credibility (Projects 6 and 7):** an order/refund assistant with approval workflow and audit logs, deployed with Docker, CI/CD and monitoring. This is the strongest single signal because it shows safety thinking.

Projects 1 and 3 support the story but should not lead. For each pinned project: live demo or short video, architecture diagram, tests, a "decisions and trade-offs" section, an honest "limitations" section, and (for AI projects) evaluation results. Quality of explanation beats quantity of repos.

## Resume and GitHub strategy

**[Must learn now]** Full details and templates are in Phase 17 (Week 24). Key rules for the Indian market:

- One page. Lead with a two-line summary naming target role and stack. List skills you can discuss for ten minutes; remove the rest.
- Use the exact tool names from the job post where true (FastAPI, PostgreSQL, Docker, AWS, LangGraph, RAG). Many Indian employers use applicant-tracking filters and recruiters search by keyword; this is common knowledge in hiring, but I did not find an authoritative source I could open, so treat it as practical advice, not a measured fact.
- Describe results with real numbers or leave numbers out.
- Keep a short LinkedIn profile consistent with the resume, with pinned projects linked. Update the headline to the role you want.
- GitHub: pinned repositories, profile README, clean commits, working setup instructions, no secrets in history.
- Prepare a 2-minute explanation for each pinned project.

## When to start applying

**[Must learn now]** Do not wait for the whole roadmap. Evidence from the listings is that many roles ask for several years of experience; you have real work experience, so apply as an experienced developer expanding into Python and AI. Use these triggers (my recommendation, not a rule from a source):

| Trigger | What you can apply for | Also do |
|---|---|---|
| After Phase 8 and Project 3 (about Week 11) | Nothing yet. Start networking and updating profiles. | Update resume with Node/React work; ask about internal AI projects at your current employer |
| After Project 4 (FastAPI order backend, about Week 14) | Python/FastAPI backend and full-stack roles that list Python | Apply to 3 to 5 roles a week; use rejections to find gaps; practise SQL and API design |
| After Project 5 (document assistant with evaluation, about Week 17) | Full-Stack + AI and GenAI Application roles | Add the project and eval numbers to the resume; start system design answers |
| After Project 6 (workflow assistant with approvals, about Week 19) | GenAI Application and early Agentic AI roles that accept your experience level | Add safety and audit-log story |
| After Project 7 (deployed, monitored, about Week 23) | All of the above with a production-grade proof; cloud-heavy roles | Use deployment evidence (CI link, uptime, logs) |
| Phase 17 (Week 24) | Full intensity application and interview practice | DSA 4 to 5 problems a week |

Because you work full time: you can apply while employed, schedule interviews carefully, and keep your learning pace. Ask your current manager whether there is an AI feature you could build at work; real production experience at your own company is worth more than any course project (interpretation).

## Transferable skills

**[Must learn now]** What you already have that employers want, based on the listings and surveys above: React/Next.js; REST API design; authentication; MongoDB and database basics; Git and code review habits; debugging production issues; working with product managers and designers; frontend performance; deployment awareness. The Nasscom-Indeed summary says software engineering roles prioritise communication, APIs and Git, which you already have. Your gaps are: Python, PostgreSQL depth, AI application patterns, evaluation, cloud deployment, and system design vocabulary. Those are what the roadmap fills.

## What to postpone

**[Learn later if needed]** Do these only after the core is solid, or when a specific job demands them:

- Kubernetes and heavy infrastructure as code (Docker Compose and one cloud are enough for portfolio-level proof).
- Model fine-tuning, training, GPU serving, and ML research mathematics.
- Multiple agent frameworks and multi-agent systems; one framework plus a solid grasp of the concepts is enough.
- Many certifications; the Nasscom-Indeed summary says employers prefer demonstrable skills or certifications over degrees, and your projects are the demonstration. A single cloud certification can help for cloud roles, but do not collect them instead of building.
- Microservices, Kafka and event-driven architecture; a modular monolith is the honest default.
- Chasing every new AI tool announced each week.
- Competitive programming and hard dynamic programming.

## Weekly job-search routine (once applying)

- [ ] 5 targeted applications to roles where the posted stack matches at least 60 percent of what you have shown.
- [ ] 2 messages to people at target companies (engineers or recruiters), asking a specific question, not for a job.
- [ ] 4 to 5 DSA problems and 1 mock interview.
- [ ] 1 improvement to a pinned project from interview feedback.
- [ ] Log every application: company, role, date, stack, result, lesson.

## Verification notes and limits

- Pages opened and read on 2026-10-09: Angel One summary of Naukri JobSpeak July 2026; CXOToday articles on Indeed (26 Aug 2026) and the Nasscom-Indeed report (21 May 2026); The Core article on the Nasscom review (24 Feb 2026); Stack Overflow 2025 survey blog and technology page; the six job listings and three aggregator pages in the tables.
- Not accessible: Naukri JobSpeak original blog (HTTP 403); a government Indbiz page summarising Indeed's September 2025 AI-posting share (host not reachable); LinkedIn and Naukri listing pages; several search-result listings (Siemens, DXC, Wellfound AI/ML, Lever DevOps, Hirist) returned 404, 410, or empty pages, so they are not used.
- The numbers from news summaries were not cross-checked against the primary reports, except where noted.
- The sample is small (six listings plus three aggregator pages) and mixes company career pages, startup boards and aggregators. Do not generalise to the whole market.
- Salary: omitted on purpose. Role and location affect pay heavily, and the only figures available to me were from aggregator pages where most listings hide pay.

## Sources

Opened or fetched in this session (research date 2026-10-09):

- https://code.claude.com/docs/en/best-practices
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- https://stackoverflow.blog/2025/07/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/
- https://survey.stackoverflow.co/2025/technology
- https://www.angelone.in/news/stocks/info-edge-s-naukri-jobspeak-report-white-collar-hiring-up-5-in-july-2026-ai-ml-roles-lead-growth
- https://cxotoday.com/research/indias-job-postings-rebound-8-3-yoy-snapping-three-month-decline/
- https://cxotoday.com/research/skills-over-degrees-nasscom-indeed-report-reveals-indias-evolving-ai-hiring-landscape/
- https://www.thecore.in/business/ai-dampens-tech-hiring-in-india-23-growth-in-fy26-vs-fy25-859053
- https://www.beroeinc.com/careers-vacancies/full-stack-ai-engineer/
- https://jobs.recooty.com/engineerbabu-it-services-pvt-ltd-/full-stack-engineer-en334
- https://jobs.645ventures.com/companies/arbor-2-c1cd2b7f-56ad-4ca3-ad99-6f2ac9e0fb62/jobs/52964763-senior-full-stack-engineer
- https://southasiacareers.deloitte.com/job/Bengaluru-Senior-Associate-Engineering-Foundry-&-Managed-Services-Bengaluru-Engineering-as-a-Service-Op/50759144/
- https://cutshort.io/job/Generative-AI-Engineer-Bengaluru-Bangalore-Delhi-Gurugram-Noida-Ghaziabad-Faridabad-Hyderabad-Mumbai-Chennai-Pune-Gravity-Engineering-Services-Pvt-Ltd-tKcXpfK5
- https://wellfound.com/jobs/4691299-agentic-ai-engineer
- https://www.weekday.works/jobs/backend-developer-jobs-in-india
- https://www.weekday.works/jobs/ml-ai-engineering-jobs
- https://www.weekday.works/jobs/devops-engineer-jobs-in-india-18
