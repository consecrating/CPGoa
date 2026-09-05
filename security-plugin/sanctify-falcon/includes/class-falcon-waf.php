<?php
/**
 * Sanctify Falcon — Virtual Patch / WAF
 *
 * Blocks known-vulnerable, unauthenticated attack surfaces on theme-bundled
 * plugins that cannot be updated from WordPress.org, until the licensed patched
 * versions are installed:
 *
 *  - ThemeREX Addons  CVE-2024-13448 / CVE-2026-1969  (arbitrary file upload via
 *    unauthenticated AI-helper AJAX actions reaching trx_addons_uploads_save_data)
 *  - Slider Revolution CVEs (6.0.0–6.7.55): block unauthenticated RevSlider AJAX.
 *
 * This is a virtual patch: it denies the exploit path without touching plugin
 * files. Once ThemeREX Addons >= 2.45 and Slider Revolution >= 6.7.58 are
 * installed, these blocks are harmless (belt-and-braces) and can stay.
 */
if (!defined('ABSPATH')) {
    exit;
}

class Sanctify_Falcon_WAF {

    public function hooks() {
        // Run before admin-ajax dispatches the action.
        add_action('admin_init', array($this, 'guard_admin_ajax'), 0);
        add_action('init', array($this, 'guard_admin_ajax'), 0);
    }

    public function guard_admin_ajax() {
        if (!defined('DOING_AJAX') || !DOING_AJAX) {
            return;
        }
        // Only police UNAUTHENTICATED requests. Logged-in editors/admins keep full
        // access to legitimate plugin functionality.
        if (is_user_logged_in()) {
            return;
        }
        $action = isset($_REQUEST['action']) ? (string) $_REQUEST['action'] : '';
        if ($action === '') {
            return;
        }

        // ThemeREX Addons: unauthenticated actions that lead to file writes /
        // uploads / remote fetches (the CVE-2024-13448 / CVE-2026-1969 surface).
        $trx_blocked = array(
            'trx_addons_ai_helper_igenerator',
            'trx_addons_ai_helper_igenerator_fetch',
            'trx_addons_ai_helper_tgenerator',
            'trx_addons_ai_helper_tgenerator_fetch',
            'trx_addons_ai_helper_process_selection_fetch',
            'trx_addons_ai_helper_fetch_images',
            'trx_addons_ai_helper_chat',
            'trx_addons_ai_helper_chat_fetch',
            'trx_addons_uploads_save_data',
            'trx_addons_uploads_save_file',
        );

        $blocked = false;
        if (in_array($action, $trx_blocked, true)) {
            $blocked = true;
        }
        // Slider Revolution: block unauthenticated revslider_ajax_action calls
        // (the auth-bypass / info-disclosure surface on <= 6.7.55).
        if (!$blocked && (strpos($action, 'revslider') !== false)) {
            $blocked = true;
        }

        if ($blocked) {
            if (class_exists('Sanctify_Falcon_Logger')) {
                Sanctify_Falcon_Logger::log(
                    'WAF blocked unauthenticated AJAX action: ' . $action
                    . ' from ' . ($this->client_ip()),
                    'critical'
                );
            }
            status_header(403);
            wp_die('Forbidden', 'Forbidden', array('response' => 403));
        }
    }

    private function client_ip() {
        foreach (array('HTTP_CF_CONNECTING_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR') as $k) {
            if (!empty($_SERVER[$k])) {
                $ip = explode(',', $_SERVER[$k]);
                return trim($ip[0]);
            }
        }
        return 'unknown';
    }
}
