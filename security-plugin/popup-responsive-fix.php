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

/*
 * Part A — Calendar mobile CSS for the EMBEDDED animation page.
 * Page 27675 is built with Elementor, so edits to the classic content field are
 * not rendered. We inject the mobile fix directly when the page is loaded in the
 * popup iframe (?cp_embed=1) or normally. This fixes the big empty gap on phones.
 */
add_action('wp_head', function () {
    if (!is_page('website-animation')) {
        return;
    }
    ?>
<style id="cp-calendar-mobile-fix">
/* --- Header row: fix the distorted / overlapping "SURPRISE GIFTS" ---
   The original uses a rigid 7-col grid where .surprise (47px) and .gifts (57px)
   with white-space:nowrap overflow their single-column cells and collide.
   Switch the header to a flex row so DAILY | SURPRISE GIFTS space out cleanly and
   the text scales to available width instead of overlapping. */
.headerrow{
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    gap:24px !important;
    flex-wrap:nowrap !important;
}
.headerrow .daily{
    grid-column:auto !important;
    flex:0 1 auto !important;
    white-space:nowrap !important;
    font-size:clamp(16px,2.2vw,28px) !important;
    letter-spacing:10px !important;
    padding:8px 18px !important;
}
.headerrow .surprise,
.headerrow .gifts{
    grid-column:auto !important;
    flex:0 0 auto !important;
    white-space:nowrap !important;
    text-align:center !important;
    overflow:visible !important;
}
.headerrow .surprise{ font-size:clamp(20px,2.6vw,40px) !important; }
.headerrow .gifts{ font-size:clamp(24px,3.2vw,50px) !important; margin-left:-8px !important; }

@media(max-width:680px){
  /* 7-column weekday strip doesn't align with the 2-column mobile card grid and
     just creates a confusing gap under the header — hide it on phones. */
  .weekdays{display:none !important;}
  /* Leading blank offset cells each reserve a full square (~2 empty rows),
     producing a large void before day 1 on the 2-col grid — collapse them. */
  .calendar-grid .blank{display:none !important;}
  /* Tighten header spacing so cards start right after the GIFTS banner. */
  .headerrow{margin:6px 0 12px !important; gap:10px !important; flex-wrap:wrap !important;}
  .headerrow .daily{ flex:1 0 100% !important; }
  .headerrow .surprise{ font-size:22px !important; }
  .headerrow .gifts{ font-size:26px !important; margin-left:0 !important; }
}
</style>
    <?php
}, 99);

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
    width:92vw;
    height:90vh;
    height:90dvh;                     /* dvh avoids mobile address-bar clipping */
    max-width:1500px;                 /* wide layout on desktop for the 7-col calendar */
    border-radius:10px;
    box-shadow:0 10px 40px rgba(0,0,0,.45);
}
html body.home #cp-box,
html body.frontpage #cp-box{
    width:92vw !important;
    height:90dvh !important;
    max-width:1500px !important;
}
#cp-frame{ border-radius:10px; }

/* Tablet */
@media (max-width:1024px){
    html body.home #cp-box, html body.frontpage #cp-box{
        width:94vw !important;
        height:90dvh !important;
        max-width:none !important;
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

/* --- Fix the stray "X": the WPFront notification-bar close button renders as a
   bare serif letter in the top-right and collides with the popup. Restyle it into
   a subtle, properly-shaped close control (and keep it out of the popup's way). --- */
.wpfront-notification-bar .wpfront-close,
.wpfront-notification-bar a.wpfront-close{
    font-size:0 !important;            /* hide the stray "X" glyph */
    width:22px !important; height:22px !important;
    line-height:22px !important; text-align:center !important;
    border-radius:50% !important;
    background:rgba(0,0,0,.28) !important;
    opacity:.85 !important;
}
.wpfront-notification-bar .wpfront-close::before{
    content:"\00d7" !important;         /* clean multiplication-sign × */
    font-size:16px !important; font-family:Arial,Helvetica,sans-serif !important;
    color:#fff !important; line-height:22px !important;
}
/* While the popup is open, don't let the notice-bar X sit on top of the popup. */
html body.home #cp-ov.is-open ~ * .wpfront-notification-bar,
.cp-lock .wpfront-notification-bar{ z-index:1 !important; }
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
