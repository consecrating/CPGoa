// CP SEO - H1 + Canonical normalisation (main pages)
// Ensures exactly ONE keyword-optimized H1 per page and a self-referencing
// canonical on /blog/. Primary keywords: Best Casino in Goa, Top Casino in
// Goa, Casino in Goa.
//
// Strategy:
//  - Pages with NO H1 (tariffs, faqs, blog): inject one via wp_body_open.
//  - Pages with MULTIPLE H1 (home, casino-2, about-us): demote every <h1> to
//    <h2> through an output buffer, then inject one clean keyworded H1.

// ---- 1) Canonical for /blog/ (had none) ----
add_action('wp_head', function () {
    if (is_page('blog') || is_home()) {
        echo '<link rel="canonical" href="https://www.cpofficial.in/blog/" />' . "\n";
    }
}, 1);

// ---- 2) Decide the H1 text + whether to demote existing H1s ----
function cp_seo_h1_config() {
    // slug/context => array(h1_text, demote_existing_h1s)
    if (is_front_page()) {
        return array('Casino Pride — Best Casino in Goa for Gaming &amp; Entertainment', true);
    }
    if (is_page('casino-2')) {
        return array('Casino Pride Gaming Floor — Best Casino in Goa', true);
    }
    if (is_page('about-us')) {
        return array('About Casino Pride — Best Casino in Goa Since 2010', true);
    }
    if (is_page('tariffs')) {
        return array('Casino Pride Entry Fee &amp; Packages — Best Casino in Goa', false);
    }
    if (is_page('faqs')) {
        return array('Casino Pride FAQs — Best Casino in Goa', false);
    }
    if (is_page('blog') || is_home()) {
        return array('Casino Pride Blog — Tips &amp; Guides for the Best Casino in Goa', false);
    }
    return array('', false);
}

// ---- 3) Output-buffer H1->H2 demotion on multi-H1 pages ----
add_action('template_redirect', function () {
    list($h1, $demote) = cp_seo_h1_config();
    if (!$demote) {
        return;
    }
    ob_start(function ($html) {
        if (stripos($html, '<h1') === false) {
            return $html;
        }
        // 1) Mask OUR injected H1 block (class "cp-seo-h1") so the global
        //    demotion below never touches it.
        $token = '<!--CP_SEO_H1_KEEP-->';
        $saved = array();
        $html = preg_replace_callback(
            '/<h1\b[^>]*cp-seo-h1[^>]*>.*?<\/h1>/is',
            function ($m) use (&$saved, $token) {
                $saved[] = $m[0];
                return $token . (count($saved) - 1) . $token;
            },
            $html
        );
        // 2) Demote all remaining (theme/Elementor) H1s to H2.
        $html = preg_replace('/<h1(\b[^>]*)>/i', '<h2$1 data-cp-was-h1="1">', $html);
        $html = preg_replace('/<\/h1>/i', '</h2>', $html);
        // 3) Restore our protected H1(s).
        $html = preg_replace_callback(
            '/' . preg_quote($token, '/') . '(\d+)' . preg_quote($token, '/') . '/',
            function ($m) use ($saved) {
                return isset($saved[(int) $m[1]]) ? $saved[(int) $m[1]] : '';
            },
            $html
        );
        return $html;
    });
}, 1);

// ---- 4) Inject the single keyword H1 near the top of the body ----
//   On pages where we demote existing H1s, the page already has a strong visual
//   hero, so we add an ACCESSIBLE, visually-hidden H1 (present in the DOM and
//   fully crawlable — not display:none, which search engines discount).
//   On pages with no hero heading (tariffs/faqs/blog) we show a clean visible H1.
add_action('wp_body_open', function () {
    list($h1, $demote) = cp_seo_h1_config();
    if ($h1 === '') {
        return;
    }
    if ($demote) {
        // Visually-hidden but crawlable + screen-reader accessible.
        echo '<h1 class="cp-seo-h1" style="'
           . 'position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
           . 'overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;'
           . '">' . $h1 . '</h1>' . "\n";
    } else {
        echo '<h1 class="cp-seo-h1" style="'
           . 'font-size:26px;line-height:1.25;font-weight:700;color:#0b0b0b;'
           . 'text-align:center;margin:14px auto 4px;max-width:900px;padding:0 16px;'
           . '">' . $h1 . '</h1>' . "\n";
    }
}, 1);
