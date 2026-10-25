#!/usr/bin/env python3
"""
Validate meta tags for all HTML pages on Story Hour Academy.
Checks for missing/duplicate titles, missing/duplicate descriptions,
length outliers, and og/canonical mismatch.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

TITLE_MIN_LENGTH = 30
TITLE_MAX_LENGTH = 70
DESC_MIN_LENGTH = 50
DESC_MAX_LENGTH = 170


def extract_meta_info(filepath: str) -> Dict[str, Optional[str]]:
    """Extract meta information from an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = {
        'title': None,
        'description': None,
        'canonical': None,
        'og_url': None,
        'og_title': None,
        'og_description': None,
        'has_charset': False,
        'has_viewport': False,
        'has_lang': False,
        'has_noindex': False,
        'has_og_image': False,
        'has_twitter_card': False,
    }
    
    # Extract title
    title_match = re.search(r'<title>([^<]*)</title>', content)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    # Extract meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if desc_match:
        info['description'] = desc_match.group(1).strip()
    
    # Extract canonical
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', content)
    if canonical_match:
        info['canonical'] = canonical_match.group(1).strip()
    
    # Extract og:url
    og_url_match = re.search(r'<meta\s+property="og:url"\s+content="([^"]*)"', content)
    if og_url_match:
        info['og_url'] = og_url_match.group(1).strip()
    
    # Extract og:title
    og_title_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', content)
    if og_title_match:
        info['og_title'] = og_title_match.group(1).strip()
    
    # Extract og:description
    og_desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', content)
    if og_desc_match:
        info['og_description'] = og_desc_match.group(1).strip()
    
    # Check for required elements
    info['has_charset'] = 'charset="UTF-8"' in content or "charset='UTF-8'" in content
    info['has_viewport'] = 'name="viewport"' in content
    info['has_lang'] = 'lang="en"' in content
    info['has_noindex'] = 'noindex' in content
    info['has_og_image'] = 'og:image' in content
    info['has_twitter_card'] = 'twitter:card' in content
    
    return info


def validate_files() -> Tuple[List[str], int]:
    """Validate all HTML files and return issues and duplicate count."""
    html_files = list(Path('.').glob('*.html'))
    
    issues = []
    titles = defaultdict(list)
    descriptions = defaultdict(list)
    
    for filepath in sorted(html_files):
        filename = str(filepath)
        
        # Skip template files
        if 'template' in filename.lower():
            continue
        
        info = extract_meta_info(filename)
        
        # Check for missing title
        if not info['title']:
            issues.append(f"MISSING TITLE: {filename}")
        else:
            titles[info['title']].append(filename)
            
            # Check title length
            title_len = len(info['title'])
            if title_len < TITLE_MIN_LENGTH:
                issues.append(f"SHORT TITLE ({title_len} chars): {filename} - \"{info['title']}\"")
            elif title_len > TITLE_MAX_LENGTH:
                issues.append(f"LONG TITLE ({title_len} chars): {filename} - \"{info['title']}\"")
        
        # Check for missing description
        if not info['description']:
            issues.append(f"MISSING DESCRIPTION: {filename}")
        else:
            descriptions[info['description']].append(filename)
            
            # Check description length
            desc_len = len(info['description'])
            if desc_len < DESC_MIN_LENGTH:
                issues.append(f"SHORT DESCRIPTION ({desc_len} chars): {filename}")
            elif desc_len > DESC_MAX_LENGTH:
                issues.append(f"LONG DESCRIPTION ({desc_len} chars): {filename}")
        
        # Check for missing canonical
        if not info['canonical']:
            issues.append(f"MISSING CANONICAL: {filename}")
        
        # Check og:url matches canonical
        if info['canonical'] and info['og_url']:
            if info['canonical'] != info['og_url']:
                issues.append(f"OG:URL MISMATCH: {filename} - canonical: {info['canonical']}, og:url: {info['og_url']}")
        
        # Check og:title matches title
        if info['title'] and info['og_title']:
            if info['title'] != info['og_title']:
                issues.append(f"OG:TITLE MISMATCH: {filename}")
        
        # Check og:description matches description
        if info['description'] and info['og_description']:
            if info['description'] != info['og_description']:
                issues.append(f"OG:DESCRIPTION MISMATCH: {filename}")
        
        # Check for required elements
        if not info['has_charset']:
            issues.append(f"MISSING CHARSET: {filename}")
        
        if not info['has_viewport']:
            issues.append(f"MISSING VIEWPORT: {filename}")
        
        if not info['has_lang']:
            issues.append(f"MISSING HTML LANG: {filename}")
        
        # Check noindex is only on specific pages
        is_noindex_page = filename in ['404.html', 'complete.html', 'thanks.html']
        if info['has_noindex'] and not is_noindex_page:
            issues.append(f"UNEXPECTED NOINDEX: {filename}")
        elif not info['has_noindex'] and is_noindex_page:
            issues.append(f"MISSING NOINDEX: {filename}")
        
        # Check for OG image
        if not info['has_og_image']:
            issues.append(f"MISSING OG:IMAGE: {filename}")
        
        # Check for Twitter card
        if not info['has_twitter_card']:
            issues.append(f"MISSING TWITTER:CARD: {filename}")
    
    # Check for duplicate titles
    duplicate_titles = 0
    for title, files in titles.items():
        if len(files) > 1:
            duplicate_titles += len(files) - 1
            issues.append(f"DUPLICATE TITLE: \"{title}\" in {len(files)} files: {', '.join(files)}")
    
    # Check for duplicate descriptions
    duplicate_descs = 0
    for desc, files in descriptions.items():
        if len(files) > 1:
            duplicate_descs += len(files) - 1
            issues.append(f"DUPLICATE DESCRIPTION in {len(files)} files: {', '.join(files)}")
    
    return issues, duplicate_titles + duplicate_descs


def main():
    """Main function to validate all HTML files."""
    print("=" * 60)
    print("Meta Tags Validation Report")
    print("=" * 60)
    print()
    
    issues, duplicates = validate_files()
    
    # Count files
    html_files = [f for f in Path('.').glob('*.html') if 'template' not in str(f).lower()]
    total_files = len(html_files)
    
    print(f"Total HTML files checked: {total_files}")
    print(f"Total issues found: {len(issues)}")
    print(f"Duplicate titles/descriptions: {duplicates}")
    print()
    
    if issues:
        print("Issues:")
        print("-" * 60)
        for issue in sorted(issues):
            print(f"  - {issue}")
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if len(issues) == 0:
        print("✓ All checks passed!")
        print(f"✓ {total_files} pages validated")
        print(f"✓ {duplicates} duplicates (expected: 0)")
        return 0
    else:
        print(f"✗ {len(issues)} issues found")
        print(f"  Duplicates remaining: {duplicates}")
        return 1


if __name__ == '__main__':
    exit(main())
