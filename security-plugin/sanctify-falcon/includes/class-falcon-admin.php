<?php
/**
 * Sanctify Falcon — Admin UI
 * Adds a "Sanctify Falcon" menu with a status dashboard, a Scan Now button,
 * and the recent event log. Capability-gated and nonce-protected.
 */
if (!defined('ABSPATH')) {
    exit;
}

class Sanctify_Falcon_Admin {

    public function hooks() {
        add_action('admin_menu', array($this, 'menu'));
        add_action('admin_post_sanctify_falcon_scan', array($this, 'handle_scan'));
    }

    public function menu() {
        add_menu_page(
            'Sanctify Falcon',
            'Sanctify Falcon',
            'manage_options',
            'sanctify-falcon',
            array($this, 'render'),
            'dashicons-shield-alt',
            81
        );
    }

    public function handle_scan() {
        if (!current_user_can('manage_options')) {
            wp_die('Insufficient permissions.');
        }
        check_admin_referer('sanctify_falcon_scan');
        Sanctify_Falcon_Scanner::scan();
        wp_safe_redirect(admin_url('admin.php?page=sanctify-falcon&scanned=1'));
        exit;
    }

    public function render() {
        if (!current_user_can('manage_options')) {
            return;
        }
        $report = get_option('sanctify_falcon_last_scan', array());
        $events = array_reverse(Sanctify_Falcon_Logger::recent());
        $next   = wp_next_scheduled('sanctify_falcon_hourly');
        ?>
        <div class="wrap">
            <h1>🦅 Sanctify Falcon <span style="font-size:13px;color:#666;">v<?php echo esc_html(SANCTIFY_FALCON_VERSION); ?></span></h1>
            <p>Active defense against self-healing WordPress malware (the "Smooth Backup Ink" / SCV family and similar).</p>

            <div style="display:flex;gap:20px;flex-wrap:wrap;margin:16px 0;">
                <div style="flex:1;min-width:280px;background:#fff;border:1px solid #ccd0d4;padding:16px;border-radius:6px;">
                    <h2 style="margin-top:0;">Protection status</h2>
                    <ul style="line-height:1.9;">
                        <li>✅ File-dropper auto-removal</li>
                        <li>✅ <code>.user.ini</code> / <code>.htaccess</code> auto_prepend guard</li>
                        <li>✅ Malicious &amp; rogue-hex cron cleaner</li>
                        <li>✅ Backdoor admin detection (auto-demote)</li>
                        <li>✅ Uploads PHP quarantine</li>
                        <li>⏱ Hourly sweep: <?php echo $next ? esc_html(gmdate('Y-m-d H:i', $next)) . ' UTC' : '<span style="color:#b32d2e;">not scheduled</span>'; ?></li>
                    </ul>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                        <?php wp_nonce_field('sanctify_falcon_scan'); ?>
                        <input type="hidden" name="action" value="sanctify_falcon_scan" />
                        <button type="submit" class="button button-primary">Scan now</button>
                    </form>
                </div>

                <div style="flex:1;min-width:280px;background:#fff;border:1px solid #ccd0d4;padding:16px;border-radius:6px;">
                    <h2 style="margin-top:0;">Last scan</h2>
                    <?php if (empty($report)) : ?>
                        <p>No scan run yet. Click <strong>Scan now</strong>.</p>
                    <?php else : ?>
                        <p><strong>When:</strong> <?php echo esc_html(gmdate('Y-m-d H:i', (int) $report['scanned_at'])); ?> UTC</p>
                        <?php if (!empty($report['clean'])) : ?>
                            <p style="color:#008a20;font-weight:600;">✅ Clean — no threats detected.</p>
                        <?php else : ?>
                            <p style="color:#b32d2e;font-weight:600;">⚠ Threats detected:</p>
                            <ul style="line-height:1.7;">
                                <?php foreach ($report['findings'] as $f) : ?>
                                    <li style="color:#b32d2e;">• <?php echo esc_html($f); ?></li>
                                <?php endforeach; ?>
                            </ul>
                            <p>These are auto-handled on the next request/sweep. Backdoor admins are demoted — review and delete them under Users.</p>
                        <?php endif; ?>
                    <?php endif; ?>
                </div>
            </div>

            <div style="background:#fff;border:1px solid #ccd0d4;padding:16px;border-radius:6px;">
                <h2 style="margin-top:0;">Recent activity (latest <?php echo count($events); ?>)</h2>
                <?php if (empty($events)) : ?>
                    <p>No events logged yet. That's good — nothing malicious has been seen.</p>
                <?php else : ?>
                    <table class="widefat striped">
                        <thead><tr><th style="width:170px;">Time (UTC)</th><th style="width:90px;">Level</th><th>Event</th></tr></thead>
                        <tbody>
                        <?php foreach ($events as $e) :
                            $color = ($e['level'] === 'critical') ? '#b32d2e' : (($e['level'] === 'action') ? '#8a6d00' : '#333'); ?>
                            <tr>
                                <td><?php echo esc_html(gmdate('Y-m-d H:i:s', (int) $e['t'])); ?></td>
                                <td style="color:<?php echo esc_attr($color); ?>;font-weight:600;"><?php echo esc_html(strtoupper($e['level'])); ?></td>
                                <td><?php echo esc_html($e['msg']); ?></td>
                            </tr>
                        <?php endforeach; ?>
                        </tbody>
                    </table>
                    <p style="color:#666;font-size:12px;">Full log: <code>wp-content/uploads/sanctify-falcon.log</code></p>
                <?php endif; ?>
            </div>
        </div>
        <?php
    }
}
