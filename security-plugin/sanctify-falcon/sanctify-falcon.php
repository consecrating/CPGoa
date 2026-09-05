<?php
/**
 * Plugin Name: Sanctify Falcon
 * Plugin URI:  https://www.sanctify.in
 * Description: Active malware defense for WordPress. Detects and auto-removes self-healing infections (auto_prepend loaders, fake "backup" mu-plugins, rogue-hex cron hooks, backdoor admins, and known dropper seeds), hardens PHP execution in wp-content/uploads, and logs every action. Built in response to the "Smooth Backup Ink" (SCV) infection family.
 * Version:     1.1.0
 * Author:      Sanctify (Antigravity AI)
 * License:     GPL2
 * Text Domain: sanctify-falcon
 */

if (!defined('ABSPATH')) {
    exit;
}

define('SANCTIFY_FALCON_VERSION', '1.1.0');
define('SANCTIFY_FALCON_FILE', __FILE__);
define('SANCTIFY_FALCON_DIR', plugin_dir_path(__FILE__));
define('SANCTIFY_FALCON_URL', plugin_dir_url(__FILE__));
define('SANCTIFY_FALCON_LOG', WP_CONTENT_DIR . '/uploads/sanctify-falcon.log');

require_once SANCTIFY_FALCON_DIR . 'includes/class-falcon-logger.php';
require_once SANCTIFY_FALCON_DIR . 'includes/class-falcon-defense.php';
require_once SANCTIFY_FALCON_DIR . 'includes/class-falcon-scanner.php';
require_once SANCTIFY_FALCON_DIR . 'includes/class-falcon-admin.php';
require_once SANCTIFY_FALCON_DIR . 'includes/class-falcon-waf.php';

/**
 * Boot the plugin.
 */
function sanctify_falcon_boot() {
    // Active defense runs early on every request (front + admin + cron).
    $defense = new Sanctify_Falcon_Defense();
    add_action('init', array($defense, 'run_guards'), 1);
    // Also run on cron so a scheduled infection attempt is cleaned even without a page view.
    add_action('sanctify_falcon_hourly', array($defense, 'run_guards'));

    // Virtual patch / WAF for unpatched theme-bundled plugins (ThemeREX, RevSlider).
    $waf = new Sanctify_Falcon_WAF();
    $waf->hooks();

    // Admin UI.
    if (is_admin()) {
        $admin = new Sanctify_Falcon_Admin();
        $admin->hooks();
    }
}
add_action('plugins_loaded', 'sanctify_falcon_boot');

/**
 * Activation: schedule the hourly guard sweep and seed a first scan.
 */
function sanctify_falcon_activate() {
    if (!wp_next_scheduled('sanctify_falcon_hourly')) {
        wp_schedule_event(time() + 60, 'hourly', 'sanctify_falcon_hourly');
    }
    Sanctify_Falcon_Logger::log('Plugin activated (v' . SANCTIFY_FALCON_VERSION . ').');
    // Run guards immediately so activation cleans anything present right now.
    $defense = new Sanctify_Falcon_Defense();
    $defense->run_guards();
}
register_activation_hook(__FILE__, 'sanctify_falcon_activate');

/**
 * Deactivation: unschedule our cron. Leaves the log intact.
 */
function sanctify_falcon_deactivate() {
    $ts = wp_next_scheduled('sanctify_falcon_hourly');
    if ($ts) {
        wp_unschedule_event($ts, 'sanctify_falcon_hourly');
    }
    Sanctify_Falcon_Logger::log('Plugin deactivated.');
}
register_deactivation_hook(__FILE__, 'sanctify_falcon_deactivate');
