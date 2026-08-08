#!/usr/bin/env python3
"""
Schema Markup Updater for Casino Pride (cpofficial.in)
Injects corrected schema markup via WordPress Code Snippets or direct injection.

This script creates a PHP code snippet that adds proper JSON-LD schema to the site.
"""

import requests
import json
import base64

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


# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

CASINO_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Casino",
    "name": "Casino Pride",
    "alternateName": "Casino Pride Goa",
    "description": "Casino Pride is the best casino in Goa offering world-class gaming, live entertainment, gourmet dining, and family-friendly experiences on the Mandovi River.",
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
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Casino Pride Packages",
        "itemListElement": [
            {
                "@type": "Offer",
                "name": "Regular Package",
                "price": "2500",
                "priceCurrency": "INR",
                "description": "Promotional vouchers worth ₹500, unlimited food buffet, house brand drinks, weather deck access"
            },
            {
                "@type": "Offer",
                "name": "Premium Package",
                "price": "3000",
                "priceCurrency": "INR",
                "description": "Promotional vouchers worth ₹1000, unlimited food buffet, house brand drinks, weather deck access"
            },
            {
                "@type": "Offer",
                "name": "Luxury Package",
                "price": "4000",
                "priceCurrency": "INR",
                "description": "Promotional vouchers worth ₹1500, unlimited IMFL & exotic dishes, weather deck access"
            },
            {
                "@type": "Offer",
                "name": "VIP Package",
                "price": "5500",
                "priceCurrency": "INR",
                "description": "Promotional vouchers worth ₹1500, premium imported liquor, à la carte menu, front row seating"
            }
        ]
    }
}

ORGANIZATION_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Casino Pride",
    "url": "https://www.cpofficial.in/",
    "logo": "https://www.cpofficial.in/wp-content/uploads/2025/12/casino-pride-logo.png",
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+919158885000",
        "contactType": "reservations",
        "areaServed": "IN",
        "availableLanguage": ["English", "Hindi"]
    },
    "sameAs": [
        "https://www.facebook.com/casinoprideofficial/",
        "https://x.com/CasinoPrideGoa",
        "https://www.instagram.com/casinoprideofficial/"
    ]
}

WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Casino Pride",
    "url": "https://www.cpofficial.in/",
    "potentialAction": {
        "@type": "SearchAction",
        "target": "https://www.cpofficial.in/?s={search_term_string}",
        "query-input": "required name=search_term_string"
    }
}

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "What is the entry fee for Casino Pride Goa?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Casino Pride offers four packages: Regular (₹2500), Premium (₹3000), Luxury (₹4000), and VIP (₹5500). All packages include gaming chips, unlimited food buffet, and drinks."
            }
        },
        {
            "@type": "Question",
            "name": "What is the age limit for Casino Pride?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "The minimum age to enter Casino Pride's gaming area is 21 years. Valid government-issued photo ID is required. Kids zone is available for children."
            }
        },
        {
            "@type": "Question",
            "name": "What games are available at Casino Pride?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Casino Pride offers 30+ games including Poker, Roulette, Blackjack, Baccarat, Teen Patti, Andar Bahar, Casino War, Dragon Tiger, Mini Flush, King of Spades, and slot machines."
            }
        },
        {
            "@type": "Question",
            "name": "What is the dress code for Casino Pride Goa?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Casino Pride follows a smart casual dress code. Avoid wearing shorts, slippers, or beachwear. Collared shirts, trousers, and closed shoes are recommended for men."
            }
        },
        {
            "@type": "Question",
            "name": "Is Casino Pride open 24 hours?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes, Casino Pride operates 24 hours a day, 7 days a week, 365 days a year. You can visit anytime for gaming, entertainment, and dining."
            }
        },
        {
            "@type": "Question",
            "name": "Where is Casino Pride located?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Casino Pride is located at Captain of Ports Jetty, Dayanand Bandodkar Marg, Panjim, Goa 403001. It's a floating casino on the Mandovi River in North Goa."
            }
        },
        {
            "@type": "Question",
            "name": "Is Casino Pride good for families?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes! Casino Pride has a dedicated kids zone with games, entertainment, and caretakers. While the gaming floor requires age 21+, families can enjoy dining, entertainment shows, and the kids area together."
            }
        },
        {
            "@type": "Question",
            "name": "How do I book Casino Pride?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "You can book Casino Pride online through their website cpofficial.in, or through partners like Thrillophilia and Klook. Walk-in entry is also available subject to capacity."
            }
        }
    ]
}


def generate_php_snippet():
    """Generate PHP code to inject all schema markups."""
    
    casino_json = json.dumps(CASINO_SCHEMA, indent=2)
    org_json = json.dumps(ORGANIZATION_SCHEMA, indent=2)
    website_json = json.dumps(WEBSITE_SCHEMA, indent=2)
    faq_json = json.dumps(FAQ_SCHEMA, indent=2)
    
    php_code = f'''<?php
/**
 * Casino Pride - SEO Schema Markup Injection
 * Add this via Code Snippets plugin or theme functions.php
 * 
 * Adds: Casino Schema, Organization Schema, Website Schema, FAQ Schema
 * Target: https://www.cpofficial.in/
 */

// Remove old/incorrect schema if present
function cp_remove_old_schema() {{
    // This runs early to prevent duplicate schemas
    remove_action('wp_head', 'old_schema_function');
}}
add_action('init', 'cp_remove_old_schema');

// Add corrected Casino + Organization + Website Schema (Homepage)
function cp_add_homepage_schema() {{
    if (is_front_page() || is_home()) {{
        ?>
        <script type="application/ld+json">
{casino_json}
        </script>
        <script type="application/ld+json">
{org_json}
        </script>
        <script type="application/ld+json">
{website_json}
        </script>
        <?php
    }}
}}
add_action('wp_head', 'cp_add_homepage_schema', 5);

// Add FAQ Schema on FAQ page and relevant posts
function cp_add_faq_schema() {{
    if (is_page('faqs')) {{
        ?>
        <script type="application/ld+json">
{faq_json}
        </script>
        <?php
    }}
}}
add_action('wp_head', 'cp_add_faq_schema', 5);

// Add Breadcrumb Schema on all pages
function cp_add_breadcrumb_schema() {{
    if (is_front_page()) return;
    
    $breadcrumbs = array(
        array(
            "@type" => "ListItem",
            "position" => 1,
            "name" => "Home",
            "item" => "https://www.cpofficial.in/"
        )
    );
    
    if (is_page()) {{
        global $post;
        $breadcrumbs[] = array(
            "@type" => "ListItem",
            "position" => 2,
            "name" => get_the_title(),
            "item" => get_permalink()
        );
    }} elseif (is_single()) {{
        $breadcrumbs[] = array(
            "@type" => "ListItem",
            "position" => 2,
            "name" => "Blog",
            "item" => "https://www.cpofficial.in/blog/"
        );
        $breadcrumbs[] = array(
            "@type" => "ListItem",
            "position" => 3,
            "name" => get_the_title(),
            "item" => get_permalink()
        );
    }}
    
    $schema = array(
        "@context" => "https://schema.org",
        "@type" => "BreadcrumbList",
        "itemListElement" => $breadcrumbs
    );
    
    echo '<script type="application/ld+json">' . json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\\n";
}}
add_action('wp_head', 'cp_add_breadcrumb_schema', 6);

// Add Article Schema on blog posts
function cp_add_article_schema() {{
    if (!is_single()) return;
    
    global $post;
    $schema = array(
        "@context" => "https://schema.org",
        "@type" => "Article",
        "headline" => get_the_title(),
        "datePublished" => get_the_date('c'),
        "dateModified" => get_the_modified_date('c'),
        "author" => array(
            "@type" => "Organization",
            "name" => "Casino Pride"
        ),
        "publisher" => array(
            "@type" => "Organization",
            "name" => "Casino Pride",
            "logo" => array(
                "@type" => "ImageObject",
                "url" => "https://www.cpofficial.in/wp-content/uploads/2025/12/casino-pride-logo.png"
            )
        ),
        "mainEntityOfPage" => array(
            "@type" => "WebPage",
            "@id" => get_permalink()
        )
    );
    
    // Add featured image if exists
    if (has_post_thumbnail()) {{
        $schema["image"] = get_the_post_thumbnail_url($post, 'full');
    }}
    
    echo '<script type="application/ld+json">' . json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\\n";
}}
add_action('wp_head', 'cp_add_article_schema', 6);
'''
    
    return php_code


def generate_meta_description_php():
    """Generate PHP code for meta descriptions."""
    
    meta_data = {**PAGE_SEO_DATA_META, **POST_SEO_DATA_META}
    
    php_code = '''<?php
/**
 * Casino Pride - Custom Meta Descriptions
 * Add this via Code Snippets plugin or theme functions.php
 */

function cp_custom_meta_descriptions() {
    // Homepage
    if (is_front_page() || is_home()) {
        echo '<meta name="description" content="Experience the best casino in Goa at Casino Pride. Enjoy live gaming, entertainment shows, gourmet dining & family fun on the Mandovi River. Book packages from ₹2500. Open 24/7." />' . "\\n";
        return;
    }
    
    // Pages
    if (is_page()) {
        global $post;
        $descriptions = array(
            'casino-2' => 'Explore Casino Pride\\'s world-class gaming floor with 30+ game tables including Poker, Roulette, Blackjack & Indian games. The top rated casino in Goa with live entertainment daily.',
            'tariffs' => 'Casino Pride Goa packages start at ₹2500 including gaming chips, unlimited buffet & drinks. Compare Regular, Premium, Luxury & VIP packages. Best casino entry fee in Goa.',
            'contact-us' => 'Contact Casino Pride at Captain of Ports Jetty, Panjim, Goa. Call +91 9158885000 for bookings. Located on Mandovi River, North Goa. Open 24/7, 365 days.',
            'events' => 'Discover upcoming events at Casino Pride Goa. Live music, celebrity performances, themed parties, poker tournaments & New Year celebrations. Book your casino entertainment experience.',
            'faqs' => 'Find answers about Casino Pride Goa. Entry age 21+, dress code, packages, timings, games available, kids zone, and booking information.',
            'casino-games' => 'Play 30+ casino games at Casino Pride Goa including Poker, Roulette, Blackjack, Teen Patti, Andar Bahar, Baccarat & slot machines.',
            'best-casino-in-india' => 'Casino Pride is rated among the best casinos in India. Located in Goa on the Mandovi River, offering world-class gaming, entertainment, dining & luxury packages.',
            'best-floating-casino-in-goa' => 'Experience Goa\\'s best floating casino at Casino Pride. Cruise on the Mandovi River with live gaming, entertainment, unlimited food & drinks.',
            'blog' => 'Read the latest from Casino Pride - casino game guides, Goa travel tips, entertainment updates, winning strategies & insider knowledge about the best casino in Goa.',
        );
        
        if (isset($descriptions[$post->post_name])) {
            echo '<meta name="description" content="' . esc_attr($descriptions[$post->post_name]) . '" />' . "\\n";
        }
    }
}
add_action('wp_head', 'cp_custom_meta_descriptions', 1);
'''
    
    return php_code


# Additional page meta data for the PHP generator
PAGE_SEO_DATA_META = {
    "casino-2": "Explore Casino Pride's world-class gaming floor with 30+ game tables including Poker, Roulette, Blackjack & Indian games. The top rated casino in Goa with live entertainment daily.",
    "tariffs": "Casino Pride Goa packages start at ₹2500 including gaming chips, unlimited buffet & drinks. Compare Regular, Premium, Luxury & VIP packages. Best casino entry fee in Goa.",
    "contact-us": "Contact Casino Pride at Captain of Ports Jetty, Panjim, Goa. Call +91 9158885000 for bookings. Located on Mandovi River, North Goa. Open 24/7, 365 days.",
}

POST_SEO_DATA_META = {}


def main():
    print("="*60)
    print("  CASINO PRIDE SCHEMA MARKUP GENERATOR")
    print("="*60)
    
    # Generate schema PHP snippet
    schema_php = generate_php_snippet()
    
    # Save to file
    with open("../schemas/casino-pride-schema.php", "w") as f:
        f.write(schema_php)
    
    print("\n✅ Schema PHP file saved to: schemas/casino-pride-schema.php")
    print("   → Add this code via Code Snippets plugin in WordPress admin")
    
    # Generate meta description PHP
    meta_php = generate_meta_description_php()
    with open("../schemas/meta-descriptions.php", "w") as f:
        f.write(meta_php)
    
    print("✅ Meta descriptions PHP file saved to: schemas/meta-descriptions.php")
    print("   → Add this code via Code Snippets plugin in WordPress admin")
    
    # Print schema for verification
    print("\n" + "-"*60)
    print("CASINO SCHEMA (for Google Rich Results Test):")
    print("-"*60)
    print(json.dumps(CASINO_SCHEMA, indent=2))
    
    print("\n" + "-"*60)
    print("FAQ SCHEMA:")
    print("-"*60)
    print(json.dumps(FAQ_SCHEMA, indent=2))


if __name__ == "__main__":
    main()
