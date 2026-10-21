#!/usr/bin/env python3
"""Merge INTERVIEW_QA.md + qa_extra/extra_*.md, number every question, write INTERVIEW_QA_FULL.md and a PDF."""
import html
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
BASE = ROOT / "INTERVIEW_QA.md"
EXTRA = sorted((ROOT / "qa_extra").glob("extra_*.md"))
OUT_MD = ROOT / "INTERVIEW_QA_FULL.md"
OUT_HTML = ROOT / "_qa.html"
OUT_PDF = ROOT / "Interview-Questions-and-Answers.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SEC = re.compile(r"^## (\d+)\.\s+(.*?)\s*$")


def split_blocks(text):
    """-> list of (num|None, title, body_lines) split on '## ' headings; '---' lines dropped."""
    blocks, cur = [], (None, "header", [])
    in_code = False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and ln.startswith("## "):
            blocks.append(cur)
            m = SEC.match(ln)
            cur = (int(m.group(1)) if m else None, m.group(2) if m else ln[3:].strip(), [])
            continue
        if not in_code and ln.strip() == "---":
            continue
        cur[2].append(ln)
    blocks.append(cur)
    return blocks


def main():
    base = split_blocks(BASE.read_text(encoding="utf-8"))
    extras = {}
    for f in EXTRA:
        for num, title, body in split_blocks(f.read_text(encoding="utf-8")):
            if num is not None:
                extras.setdefault(num, (title, []))[1].extend(body + [""])
    sections, tail = [], []
    for num, title, body in base:
        if num is None and title == "header":
            continue
        if num is None:
            tail.append((title, "\n".join(body).strip()))
            continue
        text = "\n".join(body).strip()
        first_q = text.find("**Q:")
        topics, qs = (text[:first_q].strip(), text[first_q:]) if first_q >= 0 else (text, "")
        parts = [topics, "### Essential questions", qs.strip()]
        if num in extras:
            parts.append("\n".join(extras[num][1]).strip())
        sections.append((num, title, "\n\n".join(p for p in parts if p)))
    base_nums = {n for n, _, _ in sections}
    for num, (title, body) in sorted(extras.items()):
        if num not in base_nums:
            sections.append((num, title, "\n".join(body).strip()))
    sections.sort(key=lambda s: s[0])

    qn, out, counts = 0, [], {}
    for num, title, body in sections:
        def number(m):
            nonlocal qn
            qn += 1
            return f"**Q{qn}. "
        body, c = re.subn(r"\*\*Q:\s*", number, body)
        counts[num] = c
        out.append(f"## {num}. {title}\n\n{body}\n")
    for title, body in tail:
        out.append(f"## {title}\n\n{body}\n")
    md = "\n".join(out)
    md = re.sub(r"^(\s*)([-*])\s+\[ \]\s+", lambda m: f"{m.group(1)}{m.group(2)} \u2610 ", md, flags=re.M)
    OUT_MD.write_text(md, encoding="utf-8")

    body_html = markdown.markdown(md, extensions=["fenced_code", "toc", "sane_lists", "nl2br"])
    body_html = re.sub(r"<p><strong>Q(\d+)\.", r'<p class="qa"><strong>Q\1.', body_html)
    toc = []
    for num, title, _ in sections:
        hid = re.search(r'<h2 id="([^"]+)">%d\.' % num, body_html)
        if hid:
            toc.append(f'<li><a href="#{hid.group(1)}">{num}. {html.escape(title)}</a> <span>{counts[num]} questions</span></li>')
    css = """
@page { size: A4; margin: 15mm 14mm 17mm 14mm; @bottom-center { content: counter(page); font: 9pt Helvetica, Arial, sans-serif; color: #666; } }
body { font: 10pt/1.45 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1c1c1c; }
h1 { font-size: 28pt; color: #12355b; margin: 0 0 6px; }
h2 { font-size: 17pt; color: #12355b; border-bottom: 2px solid #12355b; padding-bottom: 3px; margin-top: 0; page-break-before: always; }
h3 { font-size: 11.5pt; color: #1b4f8a; margin: 16px 0 6px; page-break-after: avoid; }
p { margin: 4px 0 8px; }
p.qa { border-left: 3px solid #1b4f8a; padding: 3px 0 3px 9px; background: #f6f9fc; page-break-inside: avoid; }
p.qa strong { color: #12355b; }
code { font: 8.8pt Menlo, Consolas, monospace; background: #eef1f4; padding: 0 3px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #d8dee4; border-radius: 4px; padding: 6px 9px; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
a { color: #0b5cc2; text-decoration: none; }
ul { padding-left: 20px; }
blockquote { margin: 8px 0; padding: 5px 11px; background: #fff7e0; border-left: 4px solid #e0a800; }
.cover { margin-top: 70mm; }
.cover p { font-size: 12.5pt; color: #444; }
.toc h2 { page-break-before: always; }
.toc ul { list-style: none; padding: 0; columns: 1; }
.toc li { margin: 4px 0; font-size: 11pt; }
.toc li span { color: #777; font-size: 9pt; margin-left: 8px; }
"""
    total = qn
    cover = (f'<div class="cover"><h1>Interview Questions and Answers</h1>'
             f'<p>Full-stack, Python/FastAPI and AI engineering: {total} short Q&amp;As across {len(sections)} sections</p>'
             f'<p>Companion to the 24-week Full-Stack to AI Engineer Roadmap. Prepared 12 October 2026.</p>'
             f'<p>How to use: read the question, answer out loud in your own words, then compare. '
             f'Where an answer says "check the docs", the topic changes with versions.</p></div>')
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Interview Questions and Answers</title>'
            f'<style>{css}</style></head><body>{cover}<div class="toc"><h2 id="contents">Contents</h2><ul>{"".join(toc)}</ul></div>{body_html}</body></html>')
    OUT_HTML.write_text(page, encoding="utf-8")
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--generate-pdf-document-outline",
                        f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], capture_output=True, text=True, timeout=300)
    OUT_HTML.unlink(missing_ok=True)
    print("questions:", total, "| per section:", counts)
    print("PDF ok" if OUT_PDF.exists() else "PDF FAILED: " + r.stderr[-400:])


if __name__ == "__main__":
    sys.exit(main())
