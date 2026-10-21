# Spec for extra interview Q&A authors

Read /Users/tagline/Documents/fullstack-ai-roadmap/INTERVIEW_QA.md first. It already has Q&A per section (numbered ## 1 ... ## 19). You write ADDITIONAL questions only: do NOT repeat or rephrase any existing question.

Output file: the one named in your assignment, under /Users/tagline/Documents/fullstack-ai-roadmap/qa_extra/.

Format (strict, a script merges it):
- For each assigned section start with exactly: `## <N>. <Same Title As Base File>` (for new sections use the title given).
- Inside, group by sub-topic with `### Sub-topic name` headings (e.g. `### Closures and scope`), 3-10 questions each.
- Each question is exactly two lines:
  `**Q: question text?**`
  `A: short answer.`
  followed by a blank line. Answers are SHORT: 1-3 sentences (code examples only when essential, inline backticks; at most a 1-3 line fenced block). No tables, no images, no emoji, no raw HTML, no nested lists.
- Cover beginner, intermediate and advanced/tricky questions that real interviews ask (including "output of this code" style questions where the answer is a few words, and "what is wrong with this" style).
- Accuracy matters more than volume. Where something is version-sensitive (Next.js caching, React 19 APIs, FastAPI/Pydantic versions, LLM provider APIs/parameters, AWS service status), keep the answer generic or say "check current docs for your version". Do not invent facts. You may spot-check official docs with WebFetch, but this is mainly a write-from-expertise task; do not spend long researching.
- Plain, simple English for a React/Next.js developer in India preparing for full-stack, Python backend and AI application engineer roles.
- Do NOT write to any other file. Do not modify INTERVIEW_QA.md.
When done, reply with: file path, number of questions written per section, and any answers you are unsure about.
