<?php
/**
 * Sanctify Falcon — Active Defense
 *
 * Runs on every request (and hourly via cron). Targets the "Smooth Backup Ink"
 * (SCV) self-healing malware family and generic re-infection patterns:
 *   1. Auto-remove known dropper/loader/payload files if they reappear.
 *   2. Neutralize malicious auto_prepend_file re-injected into .user.ini.
 *   3. Strip malicious auto_prepend blocks re-injected into wp-content/.htaccess.
 *   4. Unschedule malicious cron hooks (known + rogue random-hex).
 *   5. Demote/flag rogue "backup_*" administrator accounts.
 *   6. Quarantine unexpected PHP files dropped into uploads/.
 *
 * All destructive actions are logged. Guards are wrapped so a failure in one
 * never breaks the site.
 */
if (!defined('ABSPATH')) {
    exit;
}

class Sanctify_Falcon_Defense {

    /** @var string wp-content absolute path */
    private $wc;

    public function __construct() {
        $this->wc = defined('WP_CONTENT_DIR') ? WP_CONTENT_DIR : dirname(dirname(dirname(__DIR__)));
    }

    public function run_guards() {
        // Throttle the heavier filesystem guards to once per few minutes on
        // front-end hits to avoid overhead; always run on cron/admin.
        $last = (int) get_option('sanctify_falcon_last_run', 0);
        $now  = time();
        $is_cron_or_admin = (defined('DOING_CRON') && DOING_CRON) || is_admin();
        if (!$is_cron_or_admin && ($now - $last) < 180) {
            return;
        }
        update_option('sanctify_falcon_last_run', $now, false);

        $this->safe('guard_known_files');
        $this->safe('guard_user_ini');
        $this->safe('guard_wp_content_htaccess');
        $this->safe('guard_cron');
        $this->safe('guard_rogue_admins');
        $this->safe('guard_uploads_php');
    }

    private function safe($method) {
        try {
            $this->$method();
        } catch (\Throwable $e) {
            Sanctify_Falcon_Logger::log('Guard error in ' . $method . ': ' . $e->getMessage(), 'warn');
        }
    }

    // 1) Known malware files/dirs (IOCs from the cpofficial.in incident).
    private function guard_known_files() {
        $files = array(
            '/64f6b5eb.php', '/.64f6b5eb.php', '/ed0c7e2b.php', '/db.php',
            '/865fa429.zip', '/cache/bce0f3b9.php',
            '/mu-plugins/smooth-backup-ink.php',
        );
        foreach ($files as $rel) {
            $p = $this->wc . $rel;
            if (@file_exists($p) && $this->looks_malicious_file($p, $rel)) {
                if (@unlink($p)) {
                    Sanctify_Falcon_Logger::log('Removed reappeared malware file: ' . $rel, 'action');
                }
            }
        }
        // Hidden .sc_* state dirs.
        foreach ((array) @glob($this->wc . '/.sc_*', GLOB_ONLYDIR) as $d) {
            $this->rrmdir($d);
            Sanctify_Falcon_Logger::log('Removed hidden malware dir: ' . basename($d), 'action');
        }
        // Fake plugin dir.
        $fake = $this->wc . '/plugins/smooth-backup-ink';
        if (@is_dir($fake)) {
            $this->rrmdir($fake);
            Sanctify_Falcon_Logger::log('Removed fake plugin dir: plugins/smooth-backup-ink', 'action');
        }
    }

    private function looks_malicious_file($path, $rel) {
        // db.php could theoretically be a legit dropin; only remove if it carries
        // the SC malware markers. Other IOC names are removed unconditionally.
        if ($rel === '/db.php') {
            $head = @file_get_contents($path, false, null, 0, 200);
            return is_string($head) && (stripos($head, 'SC_DB') !== false || stripos($head, 'SCV:') !== false);
        }
        return true;
    }

    // 2) .user.ini auto_prepend neutralization (root + wp-content).
    private function guard_user_ini() {
        $targets = array($this->wc . '/.user.ini', dirname($this->wc) . '/.user.ini');
        foreach ($targets as $ini) {
            if (!@is_file($ini)) {
                continue;
            }
            $c = @file_get_contents($ini);
            if (is_string($c) && stripos($c, 'auto_prepend_file') !== false) {
                // Only act if it references a suspicious path (hex file / wp-content payload),
                // never a legitimate one the host may set.
                if (preg_match('/auto_prepend_file\s*=\s*["\']?[^"\'\n]*(64f6b5eb|ed0c7e2b|\/[0-9a-f]{8}\.php|wp-content)/i', $c)) {
                    @file_put_contents($ini, "; sanitized by Sanctify Falcon\n");
                    Sanctify_Falcon_Logger::log('Neutralized malicious auto_prepend in ' . $ini, 'critical');
                }
            }
        }
    }

    // 3) wp-content/.htaccess malicious auto_prepend block.
    private function guard_wp_content_htaccess() {
        $ht = $this->wc . '/.htaccess';
        if (!@is_file($ht)) {
            return;
        }
        $c = @file_get_contents($ht);
        if (!is_string($c) || stripos($c, 'auto_prepend_file') === false) {
            return;
        }
        if (preg_match('/(64f6b5eb|ed0c7e2b|\/[0-9a-f]{8}\.php)/i', $c)) {
            $hardened = "# Sanitized by Sanctify Falcon — block direct PHP execution in wp-content\n"
                . "<FilesMatch \"\\.(?i:php|phtml|phar|php[0-9])$\">\n"
                . "<IfModule mod_authz_core.c>\nRequire all denied\n</IfModule>\n"
                . "<IfModule !mod_authz_core.c>\nOrder allow,deny\nDeny from all\n</IfModule>\n"
                . "</FilesMatch>\n";
            @file_put_contents($ht, $hardened);
            Sanctify_Falcon_Logger::log('Sanitized malicious auto_prepend in wp-content/.htaccess', 'critical');
        }
    }

    // 4) Malicious cron hooks.
    private function guard_cron() {
        if (!function_exists('_get_cron_array')) {
            require_once ABSPATH . 'wp-includes/cron.php';
        }
        $cron = _get_cron_array();
        if (!is_array($cron)) {
            return;
        }
        $known_bad = array('sc_cron_fetch', 'my_monitoring_cron');
        // Hooks that belong to legit plugins/core — never touch these.
        $allow = '/(^wp_|^woocommerce|^wc_|elementor|rocket|action_scheduler|googlesitekit|jetpack|updraft|mc4wp|wpseo|smush|seo_boost|^cpo|sb_instagram|fbrfg|eps_|wpb_|litespeed|recovery_mode|delete_expired|do_pings|publish_future|wp-headers)/i';

        $seen = array();
        foreach ($cron as $ts => $ev) {
            foreach ((array) $ev as $hook => $data) {
                $seen[$hook] = true;
            }
        }
        foreach (array_keys($seen) as $hook) {
            $bad = in_array($hook, $known_bad, true);
            if (!$bad && preg_match('/^[a-z0-9]{16,}$/', $hook) && !preg_match($allow, $hook)) {
                $bad = true; // rogue random-hex hook
            }
            if ($bad) {
                wp_clear_scheduled_hook($hook);
                Sanctify_Falcon_Logger::log('Cleared malicious cron hook: ' . $hook, 'critical');
            }
        }
    }

    // 5) Rogue "backup_*" admins (auto-generated backdoor accounts).
    private function guard_rogue_admins() {
        if (!function_exists('get_users')) {
            return;
        }
        $admins = get_users(array('role' => 'administrator', 'fields' => array('ID', 'user_login', 'user_email')));
        foreach ($admins as $u) {
            $login = (string) $u->user_login;
            $email = (string) $u->user_email;
            $suspect = preg_match('/^backup_[0-9a-f]{6,}$/i', $login)
                    || preg_match('/^backup_[0-9a-f]{6,}@/i', $email);
            if ($suspect) {
                // Do not auto-delete a user (risky); demote to no-role + flag loudly.
                $user = new WP_User($u->ID);
                $user->set_role('');
                update_user_meta($u->ID, 'sanctify_falcon_flagged', time());
                Sanctify_Falcon_Logger::log('DEMOTED suspected backdoor admin: ' . $login . ' (id ' . $u->ID . ') — review & delete', 'critical');
            }
        }
    }

    // 6) Unexpected PHP dropped into uploads/.
    private function guard_uploads_php() {
        $uploads = $this->wc . '/uploads';
        if (!@is_dir($uploads)) {
            return;
        }
        // Only scan the top two levels to stay cheap; malware usually drops shallow.
        $found = array();
        $this->collect_php($uploads, 0, 2, $found);
        foreach ($found as $php) {
            $name = basename($php);
            $rel  = str_replace($uploads, '', $php);

            // Allowlist: empty index.php guards + known-legit plugin config files
            // that legitimately live under uploads/.
            if ($name === 'index.php' && @filesize($php) < 60) {
                continue;
            }
            $allow_paths = array(
                '/wph/',            // WP Hide & Security Enhancer environment config
                '/wp-file-manager', // WP File Manager working files
                '/backup',          // backup plugin working dirs
            );
            $allowed = false;
            foreach ($allow_paths as $ap) {
                if (stripos($rel, $ap) !== false) { $allowed = true; break; }
            }
            if ($allowed) {
                continue;
            }

            // Only quarantine if the file actually contains code that looks like a
            // web shell / dropper — not benign config that merely ends in .php.
            if (!$this->php_looks_dangerous($php)) {
                continue;
            }

            $qdir = $uploads . '/.sanctify-quarantine';
            if (!@is_dir($qdir)) {
                @mkdir($qdir, 0755, true);
                @file_put_contents($qdir . '/.htaccess', "Require all denied\n");
                @file_put_contents($qdir . '/index.php', "<?php // silence\n");
            }
            $dest = $qdir . '/' . basename($php) . '.' . substr(md5($php), 0, 8) . '.quar';
            if (@rename($php, $dest)) {
                Sanctify_Falcon_Logger::log('Quarantined PHP in uploads: ' . str_replace($this->wc, '', $php), 'critical');
            }
        }
    }

    /**
     * Heuristic: does this PHP file contain web-shell / dropper style code?
     * Config files that merely assign a variable are NOT dangerous.
     */
    private function php_looks_dangerous($php) {
        $c = @file_get_contents($php, false, null, 0, 65536);
        if (!is_string($c) || $c === '') {
            return false;
        }
        $patterns = array(
            'eval(', 'assert(', 'base64_decode(', 'gzinflate(', 'gzuncompress(',
            'str_rot13(', 'create_function(', 'shell_exec(', 'passthru(',
            'proc_open(', 'popen(', 'system(', '`',
            'preg_replace', 'php://input', 'move_uploaded_file(',
            'file_put_contents(', 'fwrite(', 'FilesystemIterator',
            'SCV:', 'SC_DB', 'smooth-backup', 'auto_prepend',
            '$_POST[', '$_GET[', '$_REQUEST[', '$_COOKIE[',
        );
        foreach ($patterns as $p) {
            if (stripos($c, $p) !== false) {
                // exec( appears inside safe words; require a call-like context.
                return true;
            }
        }
        // exec( with word boundary (avoid matching "execute"/"executed").
        if (preg_match('/\bexec\s*\(/i', $c)) {
            return true;
        }
        return false;
    }

    private function collect_php($dir, $depth, $max, &$out) {
        if ($depth > $max) {
            return;
        }
        $items = @scandir($dir);
        if (!is_array($items)) {
            return;
        }
        foreach ($items as $it) {
            if ($it === '.' || $it === '..' || $it === '.sanctify-quarantine') {
                continue;
            }
            $p = $dir . '/' . $it;
            if (@is_dir($p)) {
                $this->collect_php($p, $depth + 1, $max, $out);
            } elseif (preg_match('/\.(php|phtml|phar|php[0-9])$/i', $it)) {
                $out[] = $p;
            }
        }
    }

    private function rrmdir($dir) {
        if (!@is_dir($dir)) {
            return;
        }
        $items = @scandir($dir);
        if (is_array($items)) {
            foreach ($items as $it) {
                if ($it === '.' || $it === '..') {
                    continue;
                }
                $p = $dir . '/' . $it;
                @is_dir($p) ? $this->rrmdir($p) : @unlink($p);
            }
        }
        @rmdir($dir);
    }
}
