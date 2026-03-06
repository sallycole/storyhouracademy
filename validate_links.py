#!/usr/bin/env python3
"""Validate links in Story Hour Academy HTML files."""
import re, sys
from pathlib import Path

PROJECT = Path(__file__).parent
LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
S3_PREFIX = "https://storyhouracademy.s3.us-east-1.amazonaws.com/"

html_files = sorted(PROJECT.glob("*.html")) + sorted((PROJECT / "includes").glob("*.html"))
all_filenames = {f.name for f in html_files}
errors = []

for path in html_files:
    lines = path.read_text().splitlines()
    rel = path.relative_to(PROJECT)
    for lineno, line in enumerate(lines, 1):
        for url in LINK_RE.findall(line):
            # Skip external, protocol-relative, and template URLs
            if url.startswith(("http://", "https://", "//", "mailto:", "javascript:",
                               "data:")) or "${" in url:
                pass
            # Root-relative internal links
            elif url.startswith("/"):
                if url.endswith(".html"):
                    target = url.lstrip("/").split("?")[0].split("#")[0]
                    if target and target not in all_filenames:
                        errors.append(f"{rel}:{lineno}  broken root-relative link: {url}")
            # Bare relative internal links
            elif not url.startswith("#"):
                target = url.split("?")[0].split("#")[0]
                if target and target not in all_filenames and not Path(PROJECT / target).exists():
                    errors.append(f"{rel}:{lineno}  broken internal link: {url}")

            # S3 URL format
            if "storyhouracademy" in url and "amazonaws" in url and not url.startswith(S3_PREFIX):
                errors.append(f"{rel}:{lineno}  bad S3 URL: {url}")

            # Mobile Wikipedia
            if "en.m.wikipedia.org" in url:
                errors.append(f"{rel}:{lineno}  mobile Wikipedia URL: {url}")


if errors:
    print(f"Link validation failed ({len(errors)} issues):\n")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print(f"All links valid across {len(html_files)} files.")
