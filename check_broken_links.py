#!/usr/bin/env python3
"""
Check for broken internal links in HTML files.
"""

import os
import re
import glob
from collections import defaultdict

def get_all_html_files():
    """Get all HTML files in the project"""
    html_files = []
    for root, dirs, files in os.walk('.'):
        if root.startswith('./.'):
            continue
        if 'node_modules' in root or 'attached_assets' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_internal_links(html_content):
    """Extract all internal links from HTML content"""
    pattern = r'href="(/[^"#]*)"'
    links = re.findall(pattern, html_content)
    return links

def check_link_exists(link):
    """Check if a link target exists"""
    if link.endswith('/'):
        path = '.' + link + 'index.html'
    elif link.endswith('.xml') or link.endswith('.json') or link.endswith('.css') or link.endswith('.js') or link.endswith('.svg') or link.endswith('.png') or link.endswith('.jpg'):
        path = '.' + link
    else:
        path = '.' + link + '/index.html'
        if not os.path.exists(path):
            path = '.' + link
    
    return os.path.exists(path)

def main():
    print("=" * 70)
    print("Checking for broken internal links")
    print("=" * 70)
    
    html_files = get_all_html_files()
    print(f"Found {len(html_files)} HTML files to check\n")
    
    broken_links = defaultdict(list)
    all_links = set()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = extract_internal_links(content)
        
        for link in links:
            all_links.add(link)
            if not link.startswith('/assets/') and not link == '/sitemap.xml' and not link == '/manifest.json' and not link == '/robots.txt':
                if not check_link_exists(link):
                    broken_links[link].append(html_file)
    
    print(f"Total unique internal links found: {len(all_links)}")
    print(f"Broken links found: {len(broken_links)}\n")
    
    if broken_links:
        print("=" * 70)
        print("BROKEN LINKS (404)")
        print("=" * 70)
        
        for link, files in sorted(broken_links.items()):
            print(f"\n{link}")
            print(f"  Missing: .{link}/index.html or .{link}")
            print(f"  Referenced in {len(files)} file(s):")
            for f in files[:5]:
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... and {len(files) - 5} more")
    else:
        print("No broken links found!")
    
    return broken_links

if __name__ == "__main__":
    broken = main()
    print(f"\n\nSummary: {len(broken)} broken link(s) found")
