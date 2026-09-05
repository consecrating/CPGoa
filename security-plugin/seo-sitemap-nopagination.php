// CP SEO - Remove pagination URLs from XML sitemap
// SEO Boost includes paginated archive URLs (/blog/page/2/ ... /page/12/) in
// sitemap.xml. These are thin/duplicate and shouldn't be in the sitemap.
// This strips any <url> block whose <loc> contains "/page/" from the sitemap
// output, without touching the plugin. Runs ONLY on the sitemap request.

// Start the buffer as early as possible (init, priority 0) so it wraps SEO
// Boost's render() output regardless of which later hook that plugin uses.
add_action('init', function () {
    $uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    // Match sitemap.xml (and any sitemap-*.xml the plugin may serve).
    if (strpos($uri, 'sitemap') === false || strpos($uri, '.xml') === false) {
        return;
    }
    ob_start(function ($xml) {
        if (stripos($xml, '<loc>') === false || strpos($xml, '/page/') === false) {
            return $xml;
        }
        // Remove each <url>...</url> block that contains a /page/ loc.
        $xml = preg_replace(
            '/\s*<url>(?:(?!<\/url>).)*?<loc>[^<]*\/page\/[0-9]+\/?[^<]*<\/loc>(?:(?!<\/url>).)*?<\/url>/is',
            '',
            $xml
        );
        return $xml;
    });
}, 0);
