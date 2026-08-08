#!/usr/bin/env python3
"""
WordPress SEO Optimizer for Casino Pride (cpofficial.in)
Automates SEO fixes via WordPress REST API

Requirements: pip install requests
"""

import requests
import json
import base64
from typing import Optional, Dict, Any

# Configuration
WP_URL = "https://www.cpofficial.in"
WP_USER = "sanctifygoa"
WP_APP_PASSWORD = "BwVg tpE8 dHG4 82Tn 0AXz CWU9"

# Auth header
credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()
HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# =============================================================================
# SEO META DATA FOR KEY PAGES
# =============================================================================

PAGE_SEO_DATA = {
    # Homepage (if editable via page)
    "casino-pride-goas-best-and-most-famous-casino": {
        "title": "Casino Pride | Best Casino in Goa for Gaming & Entertainment",
        "meta_description": "Experience the best casino in Goa at Casino Pride. Enjoy live gaming, entertainment shows, gourmet dining & family fun on the Mandovi River. Book packages from ₹2500. Open 24/7.",
        "focus_keyword": "best casino in goa"
    },
    "casino-2": {
        "title": "Best Casino for Entertainment in Goa | Casino Pride Gaming Floor",
        "meta_description": "Explore Casino Pride's world-class gaming floor with 30+ game tables including Poker, Roulette, Blackjack & Indian games. The top rated casino in Goa with live entertainment daily.",
        "focus_keyword": "best casino for entertainment in goa"
    },
    "tariffs": {
        "title": "Casino Pride Goa Entry Fee & Packages 2026 | Book Now from ₹2500",
        "meta_description": "Casino Pride Goa packages start at ₹2500 including gaming chips, unlimited buffet & drinks. Compare Regular, Premium, Luxury & VIP packages. Best casino entry fee in Goa.",
        "focus_keyword": "casino pride entry fee"
    },
    "contact-us": {
        "title": "Contact Casino Pride Goa | Location, Directions & Booking",
        "meta_description": "Contact Casino Pride at Captain of Ports Jetty, Panjim, Goa. Call +91 9158885000 for bookings. Located on Mandovi River, North Goa. Open 24/7, 365 days.",
        "focus_keyword": "casino pride goa contact"
    },
    "events": {
        "title": "Casino Pride Events 2026 | Live Shows, Parties & Entertainment in Goa",
        "meta_description": "Discover upcoming events at Casino Pride Goa. Live music, celebrity performances, themed parties, poker tournaments & New Year celebrations. Book your casino entertainment experience.",
        "focus_keyword": "casino pride events goa"
    },
    "faqs": {
        "title": "Casino Pride FAQs | Entry Rules, Age Limit, Dress Code & More",
        "meta_description": "Find answers to frequently asked questions about Casino Pride Goa. Entry age 21+, dress code, packages, timings, games available, kids zone, and booking information.",
        "focus_keyword": "casino pride faq"
    },
    "casino-games": {
        "title": "Casino Games at Casino Pride Goa | Poker, Roulette, Blackjack & More",
        "meta_description": "Play 30+ casino games at Casino Pride Goa including Poker, Roulette, Blackjack, Teen Patti, Andar Bahar, Baccarat & slot machines. Learn rules and strategies.",
        "focus_keyword": "goa casino games"
    },
    "best-casino-in-india": {
        "title": "Best Casino in India | Casino Pride - Premium Gaming Experience",
        "meta_description": "Casino Pride is rated among the best casinos in India. Located in Goa on the Mandovi River, offering world-class gaming, entertainment, dining & luxury packages.",
        "focus_keyword": "best casino in india"
    },
    "best-floating-casino-in-goa": {
        "title": "Best Floating Casino in Goa | Casino Pride on Mandovi River",
        "meta_description": "Experience Goa's best floating casino at Casino Pride. Cruise on the Mandovi River with live gaming, entertainment, unlimited food & drinks. Top offshore casino in Goa.",
        "focus_keyword": "best floating casino in goa"
    },
    "blog": {
        "title": "Casino Pride Blog | Casino Tips, Goa Guides & Gaming News",
        "meta_description": "Read the latest from Casino Pride - casino game guides, Goa travel tips, entertainment updates, winning strategies & insider knowledge about the best casino in Goa.",
        "focus_keyword": "casino pride blog"
    }
}

# Blog posts SEO optimization
POST_SEO_DATA = {
    "best-casino-in-goa-why-casino-pride-is-the-ultimate-live-gaming-experience": {
        "title": "Best Casino in Goa: Why Casino Pride Is the Ultimate Gaming Experience [2026]",
        "meta_description": "Discover why Casino Pride is voted the best casino in Goa. Compare games, packages, entertainment & dining. Complete 2026 guide to Goa's top rated casino.",
        "focus_keyword": "best casino in goa"
    },
    "best-floating-casino-in-goa-what-makes-river-casinos-more-premium": {
        "title": "Best Floating Casino in Goa: What Makes River Casinos Premium [2026]",
        "meta_description": "Explore why floating casinos on the Mandovi River offer a premium experience. Casino Pride's offshore gaming, dining & entertainment make it Goa's top floating casino.",
        "focus_keyword": "best floating casino in goa"
    },
    "casino-cruise-in-goa-tips": {
        "title": "Casino Cruise in Goa 2026: Packages, Games & Expert Tips",
        "meta_description": "Complete guide to casino cruises in Goa. Entry fees from ₹2500, game options, dress code tips, best times to visit & how to maximize your casino cruise experience.",
        "focus_keyword": "casino cruise in goa"
    },
    "casino-in-north-goa": {
        "title": "Casino in North Goa 2026: Complete Guide to Gaming & Entertainment",
        "meta_description": "Everything about casinos in North Goa - entry fees, games, entertainment, locations & tips. Casino Pride leads as the best casino experience in North Goa.",
        "focus_keyword": "casino in north goa"
    },
    "goa-casino-games": {
        "title": "Goa Casino Games: Complete Guide to Games at Casino Pride",
        "meta_description": "Learn about all casino games available in Goa - Poker, Roulette, Blackjack, Teen Patti, Andar Bahar, slots & more. Rules, strategies & tips for Casino Pride.",
        "focus_keyword": "goa casino games"
    },
    "casino-pride-vs-big-daddy-casino": {
        "title": "Casino Pride vs Big Daddy Casino: Honest Comparison [2026]",
        "meta_description": "Detailed comparison of Casino Pride and Big Daddy Casino in Goa. Compare entry fees, games, entertainment, food, ambiance & value for money. Which casino is better?",
        "focus_keyword": "casino pride vs big daddy"
    },
    "family-friendly-casinos-in-goa": {
        "title": "Family Friendly Casinos in Goa: Casino Pride's Kids Zone & More",
        "meta_description": "Looking for family-friendly casinos in Goa? Casino Pride offers a dedicated kids zone, family entertainment & safe environment. Best casino for families in Goa.",
        "focus_keyword": "family friendly casino goa"
    },
    "casino-dress-code-what-to-wear": {
        "title": "Casino Dress Code in Goa: What to Wear at Casino Pride [2026 Guide]",
        "meta_description": "Complete dress code guide for Casino Pride Goa. What to wear, what's not allowed, smart casual tips for men & women visiting Goa's best casino.",
        "focus_keyword": "casino dress code goa"
    },
    "teen-patti-rules-explained-how-to-play-teen-patti-at-goas-top-casino": {
        "title": "Teen Patti Rules: How to Play at Casino Pride Goa [Complete Guide]",
        "meta_description": "Learn Teen Patti rules, hand rankings & winning strategies. Play Teen Patti live at Casino Pride, Goa's top rated casino. Beginner-friendly guide with pro tips.",
        "focus_keyword": "teen patti rules casino goa"
    },
    "celebrate-new-year-2025-at-goas-casino-pride": {
        "title": "New Year 2026 at Casino Pride Goa: Celebrate at the Best Casino",
        "meta_description": "Ring in New Year 2026 at Casino Pride Goa! Live music, celebrity performances, gaming, unlimited drinks & food. Book your New Year casino party in Goa now.",
        "focus_keyword": "new year casino goa"
    }
}


def get_all_pages():
    """Fetch all pages from WordPress."""
    pages = []
    page_num = 1
    while True:
        response = requests.get(
            f"{WP_URL}/wp-json/wp/v2/pages",
            headers=HEADERS,
            params={"per_page": 50, "page": page_num}
        )
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        pages.extend(data)
        page_num += 1
    return pages


def get_all_posts():
    """Fetch all posts from WordPress."""
    posts = []
    page_num = 1
    while True:
        response = requests.get(
            f"{WP_URL}/wp-json/wp/v2/posts",
            headers=HEADERS,
            params={"per_page": 50, "page": page_num}
        )
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        posts.extend(data)
        page_num += 1
    return posts


def update_page_title(page_id: int, new_title: str) -> bool:
    """Update a page's title via REST API."""
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/pages/{page_id}",
        headers=HEADERS,
        json={"title": new_title}
    )
    return response.status_code == 200


def update_post_title(post_id: int, new_title: str) -> bool:
    """Update a post's title via REST API."""
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=HEADERS,
        json={"title": new_title}
    )
    return response.status_code == 200


def optimize_pages():
    """Optimize all pages with SEO titles."""
    print("\n" + "="*60)
    print("OPTIMIZING PAGES")
    print("="*60)
    
    pages = get_all_pages()
    optimized = 0
    
    for page in pages:
        slug = page.get("slug", "")
        if slug in PAGE_SEO_DATA:
            seo = PAGE_SEO_DATA[slug]
            page_id = page["id"]
            current_title = page["title"]["rendered"]
            new_title = seo["title"]
            
            if current_title != new_title:
                print(f"\n  Page: {slug} (ID: {page_id})")
                print(f"  Current: {current_title}")
                print(f"  New:     {new_title}")
                
                if update_page_title(page_id, new_title):
                    print(f"  ✅ Updated successfully")
                    optimized += 1
                else:
                    print(f"  ❌ Failed to update")
            else:
                print(f"  ⏭️  Page '{slug}' already optimized")
    
    print(f"\n  Total pages optimized: {optimized}")


def optimize_posts():
    """Optimize blog post titles."""
    print("\n" + "="*60)
    print("OPTIMIZING BLOG POSTS")
    print("="*60)
    
    posts = get_all_posts()
    optimized = 0
    
    for post in posts:
        slug = post.get("slug", "")
        if slug in POST_SEO_DATA:
            seo = POST_SEO_DATA[slug]
            post_id = post["id"]
            current_title = post["title"]["rendered"]
            new_title = seo["title"]
            
            if current_title != new_title:
                print(f"\n  Post: {slug} (ID: {post_id})")
                print(f"  Current: {current_title}")
                print(f"  New:     {new_title}")
                
                if update_post_title(post_id, new_title):
                    print(f"  ✅ Updated successfully")
                    optimized += 1
                else:
                    print(f"  ❌ Failed to update")
            else:
                print(f"  ⏭️  Post '{slug}' already optimized")
    
    print(f"\n  Total posts optimized: {optimized}")


def generate_meta_description_snippet():
    """Generate code snippet for adding meta descriptions via theme functions.php or Code Snippets plugin."""
    
    print("\n" + "="*60)
    print("META DESCRIPTION CODE SNIPPET")
    print("="*60)
    print("""
Add this to your theme's functions.php or use the Code Snippets plugin:

```php
// Casino Pride SEO - Custom Meta Descriptions
function cp_custom_meta_descriptions() {
    if (is_front_page() || is_home()) {
        echo '<meta name="description" content="Experience the best casino in Goa at Casino Pride. Enjoy live gaming, entertainment shows, gourmet dining & family fun on the Mandovi River. Book packages from ₹2500. Open 24/7." />' . "\\n";
        echo '<meta name="keywords" content="best casino in goa, casino pride, top rated casino goa, casino entertainment goa, casino cruise goa" />' . "\\n";
    }
}
add_action('wp_head', 'cp_custom_meta_descriptions', 1);
```
""")


def print_schema_markup():
    """Print the corrected schema markup to be added to the site."""
    
    print("\n" + "="*60)
    print("CORRECTED SCHEMA MARKUP (Replace existing)")
    print("="*60)
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Casino",
        "name": "Casino Pride",
        "alternateName": "Casino Pride Goa",
        "description": "Casino Pride is the best casino in Goa, offering world-class gaming, live entertainment, gourmet dining, and family-friendly experiences on the Mandovi River in Panjim.",
        "image": "https://www.cpofficial.in/wp-content/uploads/2025/12/casino-pride-logo.png",
        "@id": "https://www.cpofficial.in/#casino",
        "url": "https://www.cpofficial.in/",
        "telephone": "+919158885000",
        "priceRange": "₹₹₹",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Captain Of Ports Jetty, Dayanand Bandodkar Marg",
            "addressLocality": "Panjim",
            "addressRegion": "Goa",
            "postalCode": "403001",
            "addressCountry": "IN"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 15.5014118,
            "longitude": 73.8278192
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.5",
            "reviewCount": "1200",
            "bestRating": "5"
        },
        "sameAs": [
            "https://www.facebook.com/casinoprideofficial/",
            "https://x.com/CasinoPrideGoa",
            "https://www.instagram.com/casinoprideofficial/",
            "https://www.tripadvisor.com/Attraction_Review-g303877-d3822485-Reviews-Casino_Pride-Panjim_North_Goa_District_Goa.html"
        ]
    }
    
    print(json.dumps(schema, indent=2))


def main():
    print("="*60)
    print("  CASINO PRIDE SEO OPTIMIZER")
    print("  Website: https://www.cpofficial.in/")
    print("="*60)
    
    print("\n1. Optimizing Page Titles...")
    optimize_pages()
    
    print("\n2. Optimizing Post Titles...")
    optimize_posts()
    
    print("\n3. Meta Description Snippet...")
    generate_meta_description_snippet()
    
    print("\n4. Schema Markup...")
    print_schema_markup()
    
    print("\n" + "="*60)
    print("  SEO OPTIMIZATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
