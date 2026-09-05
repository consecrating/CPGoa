<?php
/**
 * Sanctify Falcon — Uninstall
 * Removes plugin options and the scheduled sweep. Leaves the log file in
 * uploads/ so historical evidence is preserved.
 */
if (!defined('WP_UNINSTALL_PLUGIN')) {
    exit;
}

delete_option('sanctify_falcon_events');
delete_option('sanctify_falcon_last_scan');
delete_option('sanctify_falcon_last_run');

$ts = wp_next_scheduled('sanctify_falcon_hourly');
if ($ts) {
    wp_unschedule_event($ts, 'sanctify_falcon_hourly');
}
