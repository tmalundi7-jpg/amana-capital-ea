#!/usr/bin/env python3
"""Regenerate sitemap.xml for the Amana Capital EA GitHub Pages site.

Scans all public *.html files, excludes drafts/backups/fragments/utility
pages, and writes sitemap.xml with lastmod from git history (fallback: mtime).

Usage:
    python3 generate_sitemap.py [--dry-run] [--output sitemap.xml]

--dry-run prints what would change without writing.
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date, datetime
from xml.sax.saxutils import escape

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://www.amana-capital-ea.co.tz/"

# Substring patterns (matched against the repo-relative path) to exclude.
EXCLUDE_PATTERNS = [
    ".bak", "_old", "temp_", "test_", "scratch", "drafts",
    "temp_clone/", "temp_revert/", "_includes/", "templates/", "docs/",
    "mammoth_output/", "live_site/",
]

# Explicit non-public utility/fragment pages served at repo root.
EXCLUDE_FILES = {
    "carousel.html",
    "footer.html",
    "linkedin-banner.html",
    "linkedin-profile-pic.html",
    "monitoring.html",
    "stationery.html",
    "404.html",
}

# (changefreq, priority) by page family.
def freq_priority(path):
    name = os.path.basename(path)
    if name == "index.html":
        return "daily", "1.0"
    if name.startswith("dse-wrap-"):
        return "daily", "0.8"
    if name in ("current-prices.html", "market-intelligence.html"):
        return "daily", "0.9"
    if name.startswith("article-"):
        return "weekly", "0.6"
    if name in ("about.html", "contact.html"):
        return "monthly", "0.9"
    return "weekly", "0.5"


def git_lastmod(path):
    """Last commit date for path (YYYY-MM-DD), or None."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", path],
            capture_output=True, text=True, cwd=REPO_DIR, timeout=15,
        ).stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", out):
            return out
    except (subprocess.SubprocessError, OSError):
        pass
    return None


def mtime_lastmod(path):
    ts = os.path.getmtime(os.path.join(REPO_DIR, path))
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def public_pages():
    try:
        out = subprocess.run(
            ["git", "ls-files", "*.html"],
            capture_output=True, text=True, cwd=REPO_DIR, timeout=15,
        ).stdout.splitlines()
    except (subprocess.SubprocessError, OSError):
        out = []
        for root, _dirs, files in os.walk(REPO_DIR):
            if "/.git" in root:
                continue
            for f in files:
                if f.endswith(".html"):
                    out.append(os.path.relpath(os.path.join(root, f), REPO_DIR))
    pages = []
    for p in sorted(out):
        low = p.lower()
        if any(pat in low for pat in EXCLUDE_PATTERNS):
            continue
        if os.path.basename(p) in EXCLUDE_FILES:
            continue
        pages.append(p)
    return pages


def build_urls():
    urls = []
    for p in public_pages():
        loc = BASE_URL if p == "index.html" else BASE_URL + p
        lastmod = git_lastmod(p) or mtime_lastmod(p)
        # Never claim a future date (clock skew guard).
        if lastmod > date.today().isoformat():
            lastmod = date.today().isoformat()
        freq, prio = freq_priority(p)
        urls.append((loc, lastmod, freq, prio))
    return urls


def render(urls):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, prio in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--output", default=os.path.join(REPO_DIR, "sitemap.xml"))
    args = ap.parse_args()

    urls = build_urls()
    xml = render(urls)

    if args.dry_run:
        print(f"Would write {len(urls)} URLs to {args.output}")
        return 0

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(xml)
    print(f"Wrote {len(urls)} URLs to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
