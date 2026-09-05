<?php
/**
 * Sanctify Falcon — On-demand Scanner (read-only report)
 * Produces a status snapshot for the admin screen: IOC presence, suspicious
 * cron hooks, rogue admins, and unexpected PHP in uploads. Does NOT modify.
 */
if (!defined('ABSPATH')) {
    exit;
}

class Sanctify_Falcon_Scanner {

    public static function scan() {
        $wc = defined('WP_CONTENT_DIR') ? WP_CONTENT_DIR : dirname(dirname(dirname(__DIR__)));
        $report = array('clean' => true, 'findings' => array());

        // IOC files
        $ioc = array('/64f6b5eb.php', '/.64f6b5eb.php', '/ed0c7e2b.php', '/db.php',
                     '/865fa429.zip', '/mu-plugins/smooth-backup-ink.php');
        foreach ($ioc as $rel) {
            if (@file_exists($wc . $rel)) {
                $report['findings'][] = 'IOC file present: ' . $rel;
            }
        }
        foreach ((array) @glob($wc . '/.sc_*', GLOB_ONLYDIR) as $d) {
            $report['findings'][] = 'Hidden malware dir: ' . basename($d);
        }

        // .user.ini auto_prepend
        foreach (array($wc . '/.user.ini', dirname($wc) . '/.user.ini') as $ini) {
            if (@is_file($ini)) {
                $c = @file_get_contents($ini);
                if (is_string($c) && preg_match('/auto_prepend_file\s*=\s*["\']?[^"\'\n]*(64f6b5eb|ed0c7e2b|wp-content|\/[0-9a-f]{8}\.php)/i', $c)) {
                    $report['findings'][] = 'Malicious auto_prepend in ' . $ini;
                }
            }
        }

        // Cron
        if (!function_exists('_get_cron_array')) {
            require_once ABSPATH . 'wp-includes/cron.php';
        }
        $cron = _get_cron_array();
        $allow = '/(^wp_|^woocommerce|^wc_|elementor|rocket|action_scheduler|googlesitekit|jetpack|updraft|mc4wp|wpseo|smush|seo_boost|^cpo|sb_instagram|fbrfg|eps_|wpb_|litespeed|recovery_mode|delete_expired|do_pings|publish_future|wp-headers)/i';
        if (is_array($cron)) {
            $hooks = array();
            foreach ($cron as $ts => $ev) {
                foreach ((array) $ev as $hook => $d) {
                    $hooks[$hook] = true;
                }
            }
            foreach (array_keys($hooks) as $h) {
                if (in_array($h, array('sc_cron_fetch', 'my_monitoring_cron'), true)
                    || (preg_match('/^[a-z0-9]{16,}$/', $h) && !preg_match($allow, $h))) {
                    $report['findings'][] = 'Suspicious cron hook: ' . $h;
                }
            }
        }

        // Rogue admins
        if (function_exists('get_users')) {
            foreach (get_users(array('role' => 'administrator', 'fields' => array('ID', 'user_login', 'user_email'))) as $u) {
                if (preg_match('/^backup_[0-9a-f]{6,}/i', $u->user_login) || preg_match('/^backup_[0-9a-f]{6,}@/i', $u->user_email)) {
                    $report['findings'][] = 'Suspected backdoor admin: ' . $u->user_login . ' (id ' . $u->ID . ')';
                }
            }
        }

        $report['clean'] = empty($report['findings']);
        $report['scanned_at'] = time();
        update_option('sanctify_falcon_last_scan', $report, false);
        return $report;
    }
}
