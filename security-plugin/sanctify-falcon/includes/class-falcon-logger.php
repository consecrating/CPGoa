<?php
/**
 * Sanctify Falcon — Logger
 * Append-only log to wp-content/uploads/sanctify-falcon.log plus a rolling
 * mirror in an option so the admin screen can show recent events quickly.
 */
if (!defined('ABSPATH')) {
    exit;
}

class Sanctify_Falcon_Logger {

    const OPTION = 'sanctify_falcon_events';
    const MAX_EVENTS = 200;

    /**
     * Record an event.
     *
     * @param string $message
     * @param string $level info|warn|action|critical
     */
    public static function log($message, $level = 'info') {
        $line = '[' . gmdate('Y-m-d H:i:s') . ' UTC] [' . strtoupper($level) . '] ' . $message;

        // File log (best-effort).
        if (defined('SANCTIFY_FALCON_LOG')) {
            @file_put_contents(SANCTIFY_FALCON_LOG, $line . "\n", FILE_APPEND | LOCK_EX);
        }

        // Option mirror (for the admin screen).
        $events = get_option(self::OPTION, array());
        if (!is_array($events)) {
            $events = array();
        }
        $events[] = array('t' => time(), 'level' => $level, 'msg' => $message);
        if (count($events) > self::MAX_EVENTS) {
            $events = array_slice($events, -self::MAX_EVENTS);
        }
        update_option(self::OPTION, $events, false);
    }

    /**
     * @return array Recent events, newest last.
     */
    public static function recent() {
        $events = get_option(self::OPTION, array());
        return is_array($events) ? $events : array();
    }
}
