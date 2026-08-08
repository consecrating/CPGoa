<?php
/**
 * Casino Pride - Complete SEO Schema Markup
 * 
 * INSTALLATION: Add via WordPress Admin > Code Snippets plugin
 * Or paste into theme's functions.php (child theme recommended)
 * 
 * Includes:
 * - Casino Schema (homepage)
 * - Organization Schema (sitewide)
 * - WebSite Schema with SearchAction
 * - FAQ Schema (FAQ page)
 * - BreadcrumbList Schema (all pages except homepage)
 * - Article Schema (blog posts)
 */

// =====================================================
// 1. CASINO + ORGANIZATION + WEBSITE SCHEMA (Homepage)
// =====================================================
function cp_seo_homepage_schema() {
    if (!is_front_page() && !is_home()) return;
    ?>
    <script type="application/ld+json">
    {
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
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
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
    </script>
    <script type="application/ld+json">
    {
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
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "Casino Pride - Best Casino in Goa",
      "url": "https://www.cpofficial.in/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://www.cpofficial.in/?s={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>
    <?php
}
add_action('wp_head', 'cp_seo_homepage_schema', 2);


// =====================================================
// 2. FAQ SCHEMA (FAQ Page)
// =====================================================
function cp_seo_faq_schema() {
    if (!is_page('faqs')) return;
    ?>
    <script type="application/ld+json">
    {
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
            "text": "The minimum age to enter Casino Pride's gaming area is 21 years. Valid government-issued photo ID is required. A dedicated kids zone is available for children."
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
            "text": "Casino Pride is located at Captain of Ports Jetty, Dayanand Bandodkar Marg, Panjim, Goa 403001. It is a floating casino on the Mandovi River in North Goa."
          }
        },
        {
          "@type": "Question",
          "name": "Is Casino Pride suitable for families?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Yes! Casino Pride has a dedicated kids zone with games, entertainment, and caretakers. While the gaming floor requires age 21+, families can enjoy dining, entertainment shows, and the kids area together."
          }
        },
        {
          "@type": "Question",
          "name": "How can I book Casino Pride online?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "You can book Casino Pride online through their official website cpofficial.in, or through travel partners like Thrillophilia and Klook. Walk-in entry is also available subject to capacity."
          }
        }
      ]
    }
    </script>
    <?php
}
add_action('wp_head', 'cp_seo_faq_schema', 3);


// =====================================================
// 3. BREADCRUMB SCHEMA (All pages except homepage)
// =====================================================
function cp_seo_breadcrumb_schema() {
    if (is_front_page() || is_home()) return;
    
    $breadcrumbs = array();
    $breadcrumbs[] = array(
        "@type" => "ListItem",
        "position" => 1,
        "name" => "Home",
        "item" => "https://www.cpofficial.in/"
    );
    
    if (is_page()) {
        global $post;
        $breadcrumbs[] = array(
            "@type" => "ListItem",
            "position" => 2,
            "name" => get_the_title(),
            "item" => get_permalink()
        );
    } elseif (is_single()) {
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
    } elseif (is_category()) {
        $breadcrumbs[] = array(
            "@type" => "ListItem",
            "position" => 2,
            "name" => single_cat_title('', false),
            "item" => get_category_link(get_queried_object_id())
        );
    }
    
    $schema = array(
        "@context" => "https://schema.org",
        "@type" => "BreadcrumbList",
        "itemListElement" => $breadcrumbs
    );
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}
add_action('wp_head', 'cp_seo_breadcrumb_schema', 4);


// =====================================================
// 4. ARTICLE SCHEMA (Blog Posts)
// =====================================================
function cp_seo_article_schema() {
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
    
    if (has_post_thumbnail()) {
        $schema["image"] = get_the_post_thumbnail_url($post, 'full');
    }
    
    echo '<script type="application/ld+json">' . wp_json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
}
add_action('wp_head', 'cp_seo_article_schema', 5);


// =====================================================
// 5. META DESCRIPTIONS (Custom per page)
// =====================================================
function cp_seo_meta_descriptions() {
    // Homepage
    if (is_front_page() || is_home()) {
        echo '<meta name="description" content="Experience the best casino in Goa at Casino Pride. Enjoy live gaming, entertainment shows, gourmet dining &amp; family fun on the Mandovi River. Book packages from ₹2500. Open 24/7." />' . "\n";
        return;
    }
    
    // Pages
    if (is_page()) {
        global $post;
        $descriptions = array(
            'casino-2' => 'Explore Casino Pride\'s world-class gaming floor with 30+ game tables including Poker, Roulette, Blackjack &amp; Indian games. The top rated casino in Goa with live entertainment daily.',
            'tariffs' => 'Casino Pride Goa packages start at ₹2500 including gaming chips, unlimited buffet &amp; drinks. Compare Regular, Premium, Luxury &amp; VIP packages. Best casino entry fee in Goa.',
            'contact-us' => 'Contact Casino Pride at Captain of Ports Jetty, Panjim, Goa. Call +91 9158885000 for bookings. Located on Mandovi River, North Goa. Open 24/7, 365 days.',
            'events' => 'Discover upcoming events at Casino Pride Goa. Live music, celebrity performances, themed parties, poker tournaments &amp; New Year celebrations. Book your casino entertainment experience.',
            'faqs' => 'Find answers about Casino Pride Goa - entry fee, age limit, dress code, packages, timings, games available, kids zone, and online booking information.',
            'casino-games' => 'Play 30+ casino games at Casino Pride Goa including Poker, Roulette, Blackjack, Teen Patti, Andar Bahar, Baccarat &amp; slot machines. Learn rules and strategies.',
            'best-casino-in-india' => 'Casino Pride is rated among the best casinos in India. Located in Goa on the Mandovi River, offering world-class gaming, entertainment, dining &amp; luxury packages.',
            'best-floating-casino-in-goa' => 'Experience Goa\'s best floating casino at Casino Pride. Cruise on the Mandovi River with live gaming, entertainment, unlimited food &amp; drinks. Top offshore casino.',
            'blog' => 'Read the latest from Casino Pride - casino game guides, Goa travel tips, entertainment updates, winning strategies &amp; insider knowledge about the best casino in Goa.',
            'casino-pride-goas-best-and-most-famous-casino' => 'Casino Pride is Goa\'s best and most famous casino on the Mandovi River. Live gaming, entertainment, dining &amp; family fun. Top rated casino experience in North Goa.',
        );
        
        if (isset($descriptions[$post->post_name])) {
            echo '<meta name="description" content="' . esc_attr($descriptions[$post->post_name]) . '" />' . "\n";
        }
    }
}
add_action('wp_head', 'cp_seo_meta_descriptions', 1);


// =====================================================
// 6. OPEN GRAPH META TAGS (Enhanced Social Sharing)
// =====================================================
function cp_seo_og_tags() {
    if (is_front_page() || is_home()) {
        echo '<meta property="og:type" content="website" />' . "\n";
        echo '<meta property="og:title" content="Casino Pride | Best Casino in Goa for Gaming &amp; Entertainment" />' . "\n";
        echo '<meta property="og:description" content="Experience the best casino in Goa at Casino Pride. Live gaming, entertainment, dining &amp; family fun on the Mandovi River." />' . "\n";
        echo '<meta property="og:url" content="https://www.cpofficial.in/" />' . "\n";
        echo '<meta property="og:site_name" content="Casino Pride" />' . "\n";
        echo '<meta property="og:image" content="https://www.cpofficial.in/wp-content/uploads/2025/12/casino-pride-og-image.jpg" />' . "\n";
        echo '<meta property="og:locale" content="en_IN" />' . "\n";
    }
}
add_action('wp_head', 'cp_seo_og_tags', 2);
