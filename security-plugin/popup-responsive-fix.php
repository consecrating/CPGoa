<?php
/**
 * CP Fix - Homepage Calendar Popup (Responsive)
 *
 * Purpose: fixes the "website-animation" calendar popup (#cp-ov / #cp-box / #cp-frame)
 * that opens on the homepage. Addresses:
 *   1. The forced ".home #cp-ov{display:flex !important}" rule that kept the popup
 *      permanently open and made the close (x) button useless.
 *   2. Missing responsive sizing on phones/tablets (fixed 90vw/90vh + desktop iframe).
 *   3. The mobile 100vh / address-bar clipping (uses dvh with vh fallback).
 *   4. Close button size/position on small screens.
 *
 * Loads late in wp_footer so it overrides the earlier inline + Headers&Footers CSS.
 * Deactivate this snippet to fully revert. No page content is modified.
 */

add_action('wp_footer', function () {
    // Only on the front page where the popup runs.
    if (!is_front_page() && !is_home()) {
        return;
    }
    ?>
<style id="cp-popup-responsive-fix">
/* --- Reset the broken forced-open rule: popup is controlled by JS (.is-open) only ---
   Higher specificity (html body ...) so this wins even though the broken
   ".home #cp-ov{display:flex!important}" rule is printed later in the footer. */
/* Specificity note: the broken rule is ".home #cp-ov" = (1 id,1 class,0 el).
   We use "html body.home #cp-ov" = (1 id,1 class,2 el) which OUTRANKS it,
   and the .is-open opener adds another class = (1 id,2 class,2 el) to win. */
html body.home #cp-ov,
html body.frontpage #cp-ov,
html body.home #cp-ov[hidden],
html body.frontpage #cp-ov[hidden]{
    display:none !important;          /* hidden by default; JS adds .is-open to show */
    align-items:center !important;
    justify-content:center !important;
}
html body.home #cp-ov.is-open,
html body.frontpage #cp-ov.is-open{
    display:flex !important;          /* only shown when JS opens it */
    visibility:visible !important;
    opacity:1 !important;
}

/* --- Responsive box sizing --- */
#cp-box{
    width:90vw;
    height:90vh;
    height:90dvh;                     /* dvh avoids mobile address-bar clipping */
    max-width:1100px;                 /* don't over-stretch on large desktops */
    border-radius:10px;
    box-shadow:0 10px 40px rgba(0,0,0,.45);
}
html body.home #cp-box,
html body.frontpage #cp-box{
    width:90vw !important;
    height:90dvh !important;
    max-width:1100px !important;
}
#cp-frame{ border-radius:10px; }

/* Tablet */
@media (max-width:1024px){
    html body.home #cp-box, html body.frontpage #cp-box{
        width:94vw !important;
        height:90dvh !important;
    }
}

/* Phones: use (almost) full screen so the embedded page has room to reflow */
@media (max-width:768px){
    html body.home #cp-box, html body.frontpage #cp-box{
        width:100vw !important;
        height:100dvh !important;
        max-width:none !important;
        border-radius:0 !important;
    }
    #cp-frame{ border-radius:0 !important; }
    /* Bigger, thumb-friendly close button, safe-area aware, always tappable */
    #cp-close{
        top:max(10px, env(safe-area-inset-top)) !important;
        right:12px !important;
        width:48px !important;
        height:48px !important;
        font-size:30px !important;
        line-height:48px !important;
        z-index:2147483647 !important;
    }
}

/* Very small phones */
@media (max-width:400px){
    #cp-close{ width:44px !important; height:44px !important; font-size:26px !important; line-height:44px !important; }
}
</style>
<script id="cp-popup-responsive-fix-js">
(function(){
    // Make sure the close (x) and Esc/backdrop reliably hide the popup even though
    // the original forced-open CSS existed. We remove the class AND set hidden.
    function hardClose(ov){
        ov.classList.remove('is-open');
        ov.setAttribute('hidden','');
        document.documentElement.classList.remove('cp-lock');
        var f = document.getElementById('cp-frame');
        if (f) { try { f.src = 'about:blank'; } catch(e){} }
    }
    function wire(){
        var ov = document.getElementById('cp-ov');
        if (!ov) return;
        var closeBtn = document.getElementById('cp-close');
        if (closeBtn && !closeBtn.dataset.cpFixed){
            closeBtn.dataset.cpFixed = '1';
            closeBtn.addEventListener('click', function(e){ e.preventDefault(); e.stopPropagation(); hardClose(ov); }, true);
        }
        ov.addEventListener('click', function(e){ if (e.target === ov) hardClose(ov); }, true);
        document.addEventListener('keydown', function(e){ if (e.key === 'Escape') hardClose(ov); });
    }
    (document.readyState === 'loading')
        ? document.addEventListener('DOMContentLoaded', wire, {once:true})
        : wire();
    // re-wire briefly in case the popup markup is injected late by Elementor
    var tries = 0, iv = setInterval(function(){ wire(); if (++tries > 10) clearInterval(iv); }, 500);
})();
</script>
    <?php
}, 9999);
