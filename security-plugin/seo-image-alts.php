// CP SEO - Fill empty image ALT text (context-aware)
// Adds descriptive, keyword-aware alt text to CONTENT images that currently have
// empty alt="", improving image SEO + accessibility. Decorative assets (icons,
// dummy/lazy placeholders, logos, spacers, svg) are intentionally skipped.
// Primary keywords: Best Casino in Goa, Top Casino in Goa, Casino in Goa.

add_action('template_redirect', function () {
    // Per-page base alt phrase.
    if (is_front_page())                 { $base = 'Casino Pride — best casino in Goa'; }
    elseif (is_page('casino-2'))         { $base = 'Casino Pride gaming floor — best casino in Goa'; }
    elseif (is_page('events'))           { $base = 'Casino Pride event — top casino in Goa'; }
    elseif (is_page('tariffs'))          { $base = 'Casino Pride package — best casino in Goa'; }
    elseif (is_page('about-us'))         { $base = 'Casino Pride — best casino in Goa since 2010'; }
    elseif (is_page('casino-games'))     { $base = 'Casino games at Casino Pride Goa'; }
    elseif (is_page('best-floating-casino-in-goa')) { $base = 'Best floating casino in Goa — Casino Pride'; }
    elseif (is_page('best-casino-in-india'))        { $base = 'Casino Pride — best casino in India and Goa'; }
    else { return; }

    ob_start(function ($html) use ($base) {
        if (stripos($html, '<img') === false) {
            return $html;
        }
        // Skip decorative filenames.
        $skip = '/(dummy|icon-|icon_|wired-outline|logo|placeholder|spacer|blank|1x1|\.svg)/i';
        $n = 0;
        $html = preg_replace_callback('/<img\b[^>]*>/i', function ($m) use ($base, $skip, &$n) {
            $tag = $m[0];
            // Only touch images with an explicitly empty alt.
            if (!preg_match('/\salt\s*=\s*(""|\'\')/i', $tag)) {
                return $tag;
            }
            // Identify the file (src or lazy data-src) and skip decorative ones.
            if (preg_match('/(?:data-)?src\s*=\s*"([^"]+)"/i', $tag, $s)) {
                if (preg_match($skip, $s[1])) {
                    return $tag;
                }
            }
            $n++;
            $alt = $base . ($n > 1 ? ' ' . $n : '');
            return preg_replace('/\salt\s*=\s*(""|\'\')/i', ' alt="' . esc_attr($alt) . '"', $tag, 1);
        }, $html);
        return $html;
    });
}, 2);
