# Security Hardening Status — cpofficial.in

**Date:** 5 September 2026 · **By:** Sanctify

Follow-up to the malware incident. This documents what has been hardened and the
**owner-only actions** that remain (things that require credentials or the admin UI
and cannot/should not be automated remotely).

---

## ✅ Done (applied to the live site)

### Plugin updates (18 WP.org plugins)
All outdated WordPress.org plugins updated to current versions, including the
security-relevant ones:
- **Elementor** 4.1.5 → 4.2.4
- **WP Hide & Security Enhancer** 2.8.9 → 2.9.1
- Code Snippets 3.9.6 → 3.10.2, Jeg Kit 3.2.11 → 3.2.16, Site Kit 1.181 → 1.186,
  WP-Optimize 4.5.5 → 4.6.1, Redirection 5.6.1 → 5.10, Contact Form 7, Akismet,
  MC4WP, 301 Redirects, Duplicate Page, Favicon, Firebox, Use Any Font, WP Carousel,
  WP Headers & Footers, Filester.

### Virtual patch for the two critical bundled plugins
`ThemeREX Addons 2.29.0` and `Slider Revolution 6.6.20` are **theme-bundled** (no
WordPress.org update path), so **Sanctify Falcon v1.1.0** now virtually-patches them:
it returns **403** to unauthenticated requests hitting the vulnerable AJAX actions
- ThemeREX: `trx_addons_ai_helper_igenerator/tgenerator/chat/*_fetch`,
  `trx_addons_uploads_save_data`, `trx_addons_uploads_save_file`
  (blocks **CVE-2024-13448** & **CVE-2026-1969** — the arbitrary-file-upload path
  that was the likely original breach vector)
- Slider Revolution: unauthenticated `revslider*` actions
  (blocks the 6.0.0–6.7.55 auth-bypass / info-disclosure CVEs)

Verified: all three attack actions return 403 and are logged (with IP) to
`wp-content/uploads/sanctify-falcon.log`. Legitimate logged-in use is unaffected.

### Salt / key rotation
All 8 WordPress salts in `wp-config.php` were rotated (fresh values from the official
WordPress API). This **invalidates any auth cookies an attacker may have stolen** —
everyone is logged out and must log in again. DB credentials and all other config were
left untouched. Site verified healthy after rotation.

### Sitemap & stale files
- `sitemap.xml`, `url-list.txt`, `urllist.txt` cleaned of the 11 stale
  `/blog/page/N/` pagination URLs (sitemap now 83 clean URLs).

### Still in place from the incident cleanup
- Sanctify Falcon active defense (file/cron/backdoor-admin guards + hourly sweep)
- `DISALLOW_FILE_EDIT` on, wp-content PHP-execution block, malware IOCs confirmed gone.

---

## 🔴 Owner-only actions still required

These need your credentials or the WP admin UI. Please do them soon.

### 1. Apply the real ThemeREX/RevSlider version updates (2 clicks) — HIGH PRIORITY
The virtual patch protects the known exploit paths, but you should install the
actually-patched versions (updates ARE available — the theme's purchase code is
registered):
1. WP Admin → **ThemeREX Updater** (or Appearance → Install Plugins / theme dashboard)
2. Click **Update Plugins** — it will update:
   - ThemeREX Addons **2.29.0 → 2.45.0**
   - Slider Revolution **6.6.20 → 6.7.58**
3. After updating, the Falcon WAF blocks become harmless belt-and-braces (safe to keep).

### 2. Rotate ALL passwords — HIGH PRIORITY
The original break-in credential path is unknown, so rotate everything:
- **Every WordPress administrator** password (Users → each admin → Set New Password).
  Current admins: `admin`, `sanctifygoa`. Delete/downgrade any you don't recognise.
- **Hosting / Hostinger panel** password.
- **FTP** password (revoke the temporary FTP account used for this work).
- **Database** password — change it in Hostinger, then update `DB_PASSWORD` in
  `wp-config.php` to match (do these together or the site goes down).
- Regenerate the WordPress **application password** used for the REST work.

### 3. Reinstall WordPress core — MEDIUM
To guarantee core file integrity, reinstall the same WP version:
WP Admin → Dashboard → Updates → **Re-install version x.x.x** (or Hostinger's tool).

### 4. Submit the cleaned sitemap to Google — MEDIUM
- Google Search Console → Sitemaps → submit `https://www.cpofficial.in/sitemap.xml`
- Search Console → Security Issues and Removals → request review if any
  "hacked/deceptive" flag remains from the infection period.
- Malwarebytes false-positive review: https://www.malwarebytes.com/false-positive
  (in case the domain is still flagged from when it was infected).

### 5. Consider removing unused high-risk plugins — LOW
`WP File Manager` (8.0.4) and `Filester` (file managers) are powerful and a common
target. If not actively needed, deactivate/remove them.

---

## Quick re-check commands (read-only)
```
python3 scripts/python/seo_monitor.py          # SEO + sitemap health
# Falcon status: WP Admin → Sanctify Falcon (Scan Now + event log)
# Falcon log: wp-content/uploads/sanctify-falcon.log
```
