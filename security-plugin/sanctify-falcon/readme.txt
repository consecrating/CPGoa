=== Sanctify Falcon ===
Contributors: sanctify
Tags: security, malware, cleanup, hardening, incident-response
Requires at least: 5.0
Requires PHP: 7.0
Stable tag: 1.0.0
License: GPL2

Active malware defense for WordPress. Detects and auto-removes self-healing
infections and hardens common re-entry paths.

== Description ==

Sanctify Falcon was built in direct response to the "Smooth Backup Ink" (SCV)
infection that used PHP `auto_prepend_file` persistence, a fake mu-plugin, rogue
WP-Cron hooks, a backdoor administrator, and a zipped re-infection seed to
regenerate itself after every cleanup.

Falcon runs on every request (front, admin, and cron) and:

1. **File defense** — auto-removes known dropper/loader/payload files if they
   reappear (`64f6b5eb.php`, `.64f6b5eb.php`, `ed0c7e2b.php`, malicious `db.php`,
   `865fa429.zip`, `mu-plugins/smooth-backup-ink.php`, hidden `.sc_*` dirs, and the
   fake `plugins/smooth-backup-ink` directory).
2. **Prepend guard** — sanitizes malicious `auto_prepend_file` re-injected into
   `.user.ini` (root + wp-content) or `wp-content/.htaccess`.
3. **Cron cleaner** — unschedules known malicious hooks (`sc_cron_fetch`,
   `my_monitoring_cron`) and rogue random-hex hooks that don't belong to a known
   plugin, while leaving all legitimate schedules untouched.
4. **Backdoor admin detection** — demotes auto-generated `backup_<hex>`
   administrator accounts to no role and flags them for manual deletion.
5. **Uploads quarantine** — moves unexpected PHP files found in `wp-content/uploads`
   into a protected quarantine folder.

Every action is written to `wp-content/uploads/sanctify-falcon.log` and shown in
the admin dashboard (Sanctify Falcon menu), which also offers an on-demand scan.

== Notes ==

* Falcon is defensive and conservative: it never deletes user accounts (it demotes
  and flags), and it only removes files/hooks that match strict malware signatures.
* It complements — does not replace — good hygiene: keep WordPress, plugins, and
  themes updated, rotate credentials after any incident, and remove nulled software.

== Changelog ==

= 1.0.0 =
* Initial release: file defense, prepend guard, cron cleaner, backdoor-admin
  detection, uploads quarantine, admin dashboard, hourly sweep.
