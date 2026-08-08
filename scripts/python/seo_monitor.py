#!/usr/bin/env python3
"""
Casino Pride SEO Monitoring Script
Automated health checks for cpofficial.in

Run weekly via cron or manually to track SEO health.
Requirements: pip install requests beautifulsoup4
"""

import requests
import json
import re
import base64
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
WP_URL = "https://www.cpofficial.in"
WP_USER = "sanctifygoa"
WP_APP_PASSWORD = "BwVg tpE8 dHG4 82Tn 0AXz CWU9"

credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()
HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# Key pages to monitor
KEY_PAGES = [
    "/",
    "/casino-2/",
    "/tariffs/",
    "/contact-us/",
    "/events/",
    "/faqs/",
    "/casino-games/",
    "/best-floating-casino-in-goa/",
    "/blog/",
    "/best-casino-in-india/",
]

# Target keywords to check in titles/meta
TARGET_KEYWORDS = [
    "best casino in goa",
    "best casino for entertainment in goa",
    "top rated casino in goa",
    "casino pride",
    "casino in north goa",
    "casino cruise in goa",
    "casino pride entry fee",
    "floating casino in goa",
    "goa casino games",
]


def check_page_seo(url: str) -> Dict:
    """Check SEO elements for a given page."""
    result = {
        "url": url,
        "status": None,
        "title": None,
        "meta_description": None,
        "h1_count": 0,
        "schema_count": 0,
        "schema_types": [],
        "canonical": None,
        "issues": []
    }
    
    try:
        response = requests.get(url, timeout=15)
        result["status"] = response.status_code
        
        if response.status_code != 200:
            result["issues"].append(f"HTTP {response.status_code}")
            return result
        
        html = response.text
        
        # Title
        title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
        if title_match:
            result["title"] = title_match.group(1).strip()
            if len(result["title"]) > 60:
                result["issues"].append(f"Title too long ({len(result['title'])} chars)")
            if len(result["title"]) < 30:
                result["issues"].append(f"Title too short ({len(result['title'])} chars)")
        else:
            result["issues"].append("Missing title tag")
        
        # Meta Description
        meta_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        if meta_match:
            result["meta_description"] = meta_match.group(1)
            if len(result["meta_description"]) > 160:
                result["issues"].append(f"Meta description too long ({len(result['meta_description'])} chars)")
            if len(result["meta_description"]) < 70:
                result["issues"].append(f"Meta description too short ({len(result['meta_description'])} chars)")
        else:
            result["issues"].append("Missing meta description")
        
        # H1 tags
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
        result["h1_count"] = len(h1_matches)
        if len(h1_matches) == 0:
            result["issues"].append("No H1 tag found")
        elif len(h1_matches) > 2:
            result["issues"].append(f"Multiple H1 tags ({len(h1_matches)})")
        
        # Schema markup
        schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        result["schema_count"] = len(schemas)
        for s in schemas:
            try:
                data = json.loads(s.strip())
                schema_type = data.get("@type", "Unknown")
                result["schema_types"].append(schema_type)
                
                # Check for old domain in schema
                if "casinoprideofficial.com" in s:
                    result["issues"].append("OLD DOMAIN in schema (casinoprideofficial.com)")
            except:
                pass
        
        if len(schemas) == 0 and url == WP_URL + "/":
            result["issues"].append("No schema markup on homepage")
        
        # Canonical
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html)
        if canonical_match:
            result["canonical"] = canonical_match.group(1)
        else:
            result["issues"].append("Missing canonical tag")
        
        # Image alt text check
        imgs_total = len(re.findall(r'<img[^>]*>', html))
        imgs_no_alt = len(re.findall(r'<img(?![^>]*alt=)[^>]*>', html))
        imgs_empty_alt = len(re.findall(r'<img[^>]*alt=""[^>]*>', html))
        if imgs_no_alt > 0:
            result["issues"].append(f"{imgs_no_alt} images without alt attribute")
        if imgs_empty_alt > 3:
            result["issues"].append(f"{imgs_empty_alt} images with empty alt text")
            
    except requests.RequestException as e:
        result["issues"].append(f"Connection error: {str(e)[:50]}")
    
    return result


def check_sitemap():
    """Check sitemap for issues."""
    issues = []
    
    try:
        response = requests.get(f"{WP_URL}/sitemap.xml", timeout=15)
        if response.status_code != 200:
            issues.append(f"Sitemap returned HTTP {response.status_code}")
            return issues
        
        content = response.text
        urls = re.findall(r'<loc>(.*?)</loc>', content)
        
        # Check for problematic URLs
        respond_urls = [u for u in urls if '#respond' in u]
        pagination_urls = [u for u in urls if '/page/' in u]
        tag_urls = [u for u in urls if '/tag/' in u]
        
        if respond_urls:
            issues.append(f"{len(respond_urls)} comment anchor (#respond) URLs in sitemap - remove these")
        if pagination_urls:
            issues.append(f"{len(pagination_urls)} pagination URLs in sitemap - consider removing")
        if len(tag_urls) > 20:
            issues.append(f"{len(tag_urls)} tag archive URLs in sitemap - too many thin pages")
        
        issues.append(f"Total URLs in sitemap: {len(urls)}")
        
    except requests.RequestException as e:
        issues.append(f"Could not fetch sitemap: {str(e)[:50]}")
    
    return issues


def check_robots_txt():
    """Check robots.txt configuration."""
    issues = []
    
    try:
        response = requests.get(f"{WP_URL}/robots.txt", timeout=10)
        if response.status_code != 200:
            issues.append("robots.txt not accessible")
            return issues
        
        content = response.text.lower()
        
        if "sitemap:" not in content:
            issues.append("robots.txt missing sitemap reference")
        if "disallow: /wp-admin/" not in content:
            issues.append("robots.txt not blocking wp-admin")
        
    except requests.RequestException:
        issues.append("Could not fetch robots.txt")
    
    return issues


def check_page_speed():
    """Basic page load time check."""
    results = {}
    
    for page in ["/", "/casino-2/", "/tariffs/", "/blog/"]:
        url = f"{WP_URL}{page}"
        try:
            response = requests.get(url, timeout=30)
            load_time = response.elapsed.total_seconds()
            results[page] = {
                "load_time": round(load_time, 2),
                "size_kb": round(len(response.content) / 1024, 1),
                "status": "Good" if load_time < 3 else "Slow" if load_time < 5 else "Critical"
            }
        except:
            results[page] = {"load_time": None, "status": "Error"}
    
    return results


def check_internal_links():
    """Check that key internal links exist on homepage."""
    issues = []
    
    try:
        response = requests.get(WP_URL, timeout=15)
        html = response.text
        
        required_links = [
            ("/tariffs/", "Packages/Tariffs"),
            ("/casino-2/", "Casino page"),
            ("/contact-us/", "Contact page"),
            ("/events/", "Events page"),
            ("/blog/", "Blog page"),
        ]
        
        for link_path, name in required_links:
            if link_path not in html and f"cpofficial.in{link_path}" not in html:
                issues.append(f"Missing internal link to {name} ({link_path}) on homepage")
                
    except:
        issues.append("Could not check internal links")
    
    return issues


def generate_report():
    """Generate complete SEO health report."""
    
    report = []
    report.append("=" * 70)
    report.append(f"  CASINO PRIDE SEO HEALTH REPORT")
    report.append(f"  Website: {WP_URL}")
    report.append(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)
    
    # 1. Page SEO Checks
    report.append("\n" + "─" * 70)
    report.append("  1. PAGE SEO AUDIT")
    report.append("─" * 70)
    
    total_issues = 0
    for page in KEY_PAGES:
        url = f"{WP_URL}{page}"
        result = check_page_seo(url)
        
        status_emoji = "✅" if not result["issues"] else "⚠️"
        report.append(f"\n  {status_emoji} {page}")
        report.append(f"     Status: {result['status']} | Schemas: {result['schema_count']} ({', '.join(result['schema_types'])})")
        
        if result["title"]:
            report.append(f"     Title ({len(result['title'])}ch): {result['title'][:70]}")
        if result["meta_description"]:
            report.append(f"     Meta Desc ({len(result['meta_description'])}ch): {result['meta_description'][:70]}...")
        
        if result["issues"]:
            for issue in result["issues"]:
                report.append(f"     ❗ {issue}")
                total_issues += 1
    
    # 2. Sitemap Check
    report.append("\n" + "─" * 70)
    report.append("  2. SITEMAP HEALTH")
    report.append("─" * 70)
    
    sitemap_issues = check_sitemap()
    for issue in sitemap_issues:
        report.append(f"  {'ℹ️' if 'Total' in issue else '⚠️'} {issue}")
    
    # 3. Robots.txt Check
    report.append("\n" + "─" * 70)
    report.append("  3. ROBOTS.TXT")
    report.append("─" * 70)
    
    robots_issues = check_robots_txt()
    if not robots_issues:
        report.append("  ✅ robots.txt looks good")
    else:
        for issue in robots_issues:
            report.append(f"  ⚠️ {issue}")
    
    # 4. Page Speed
    report.append("\n" + "─" * 70)
    report.append("  4. PAGE LOAD TIMES")
    report.append("─" * 70)
    
    speed_results = check_page_speed()
    for page, data in speed_results.items():
        if data["load_time"]:
            status_emoji = "✅" if data["status"] == "Good" else "⚠️" if data["status"] == "Slow" else "❌"
            report.append(f"  {status_emoji} {page:20} | {data['load_time']}s | {data['size_kb']}KB | {data['status']}")
        else:
            report.append(f"  ❌ {page:20} | Error")
    
    # 5. Internal Links
    report.append("\n" + "─" * 70)
    report.append("  5. INTERNAL LINKING")
    report.append("─" * 70)
    
    link_issues = check_internal_links()
    if not link_issues:
        report.append("  ✅ All key internal links present on homepage")
    else:
        for issue in link_issues:
            report.append(f"  ⚠️ {issue}")
    
    # Summary
    report.append("\n" + "═" * 70)
    report.append(f"  SUMMARY: {total_issues} issues found across {len(KEY_PAGES)} pages")
    report.append("═" * 70)
    
    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # Save report to file
    filename = f"seo-report-{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "w") as f:
        f.write(report)
    print(f"\n📄 Report saved to: {filename}")
