#!/usr/bin/env python3
"""Independently re-check every URL in combined.md. YouTube via oembed, others via GET."""
import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent
text = (ROOT / "combined.md").read_text(encoding="utf-8")
urls = sorted(set(u.rstrip(".,;:") for u in re.findall(r"https?://[^\s)>\]|`\"']+", text)))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"}


def check(u):
    host = urllib.parse.urlparse(u).netloc
    try:
        if "youtube.com" in host or "youtu.be" in host:
            if "results?search_query" in u:
                return u, "BAD: search results page", ""
            # www.youtube.com is unreachable from this machine; noembed.com relays YouTube's oembed data
            q = "https://noembed.com/embed?url=" + urllib.parse.quote(u, safe="")
            with urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=20) as r:
                j = json.load(r)
            if j.get("error") or not j.get("title"):
                return u, "BAD: no video found", str(j.get("error"))
            return u, "OK", f"{j.get('title')} | {j.get('author_name')}"
        req = urllib.request.Request(u, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            return u, f"OK {r.status}", ""
    except urllib.error.HTTPError as e:
        # 403/429 from bot-protection is "reachable but blocked", flag separately
        return u, f"HTTP {e.code}", ""
    except Exception as e:  # noqa
        return u, "ERR", str(e)[:90]


with ThreadPoolExecutor(12) as ex:
    results = list(ex.map(check, urls))
bad = [r for r in results if not r[1].startswith("OK")]
(ROOT / "link_report.txt").write_text(
    "\n".join(f"{s}\t{u}\t{n}" for u, s, n in results), encoding="utf-8")
print(f"{len(results)} urls, {len(results)-len(bad)} ok, {len(bad)} flagged")
for u, s, n in bad:
    print(s, u, n)
