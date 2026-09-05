#!/usr/bin/env python3
"""Generate the Sanctify incident report PDF for cpofficial.in."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, ListFlowable, ListItem, PageBreak, HRFlowable)
from reportlab.pdfgen import canvas
from datetime import datetime

OUT = "/projects/sandbox/CPGoa/security-plugin/Sanctify-Incident-Report-cpofficial.pdf"

# Brand palette
NAVY   = colors.HexColor("#0B2540")
BLUE   = colors.HexColor("#1E5AA8")
ACCENT = colors.HexColor("#C8A24B")   # gold
RED    = colors.HexColor("#B32D2E")
GREEN  = colors.HexColor("#1E7A3D")
GREY   = colors.HexColor("#5A6675")
LIGHT  = colors.HexColor("#F2F5F9")
LINE   = colors.HexColor("#D5DCE5")

styles = getSampleStyleSheet()

def S(name, **kw):
    parent = kw.pop("parent", styles["Normal"])
    return ParagraphStyle(name, parent=parent, **kw)

body   = S("body", fontName="Helvetica", fontSize=9.5, leading=14, textColor=colors.HexColor("#1c1c1c"), alignment=TA_JUSTIFY, spaceAfter=6)
h1     = S("h1", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=8)
h2     = S("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=10, spaceAfter=4)
small  = S("small", fontName="Helvetica", fontSize=8, leading=11, textColor=GREY)
bullet = S("bullet", parent=body, alignment=TA_LEFT, spaceAfter=3)
cell   = S("cell", fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#1c1c1c"))
cellb  = S("cellb", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=NAVY)
cellw  = S("cellw", fontName="Helvetica-Bold", fontSize=8.5, leading=12, textColor=colors.white)
code   = S("code", fontName="Courier", fontSize=8, leading=11, textColor=colors.HexColor("#333333"), backColor=LIGHT)

REPORT_DATE = "5 September 2026"

# ---------- page furniture ----------
def header_footer(cv, doc):
    cv.saveState()
    w, h = A4
    # header band
    cv.setFillColor(NAVY); cv.rect(0, h-18*mm, w, 18*mm, fill=1, stroke=0)
    cv.setFillColor(ACCENT); cv.rect(0, h-18*mm, w, 1.4*mm, fill=1, stroke=0)
    cv.setFillColor(colors.white); cv.setFont("Helvetica-Bold", 11)
    cv.drawString(18*mm, h-12*mm, "SANCTIFY")
    cv.setFont("Helvetica", 8); cv.setFillColor(ACCENT)
    cv.drawString(38*mm, h-12*mm, "Security Incident Report")
    cv.setFillColor(colors.white); cv.setFont("Helvetica", 8)
    cv.drawRightString(w-18*mm, h-12*mm, "cpofficial.in  \u2022  CONFIDENTIAL")
    # footer
    cv.setStrokeColor(LINE); cv.setLineWidth(0.5); cv.line(18*mm, 14*mm, w-18*mm, 14*mm)
    cv.setFillColor(GREY); cv.setFont("Helvetica", 7.5)
    cv.drawString(18*mm, 9*mm, "Prepared by Sanctify  \u2022  www.sanctify.in")
    cv.drawCentredString(w/2, 9*mm, REPORT_DATE)
    cv.drawRightString(w-18*mm, 9*mm, "Page %d" % doc.page)
    cv.restoreState()

def cover(cv, doc):
    cv.saveState()
    w, h = A4
    cv.setFillColor(NAVY); cv.rect(0, 0, w, h, fill=1, stroke=0)
    cv.setFillColor(BLUE); cv.rect(0, h*0.62, w, h*0.02, fill=1, stroke=0)
    cv.setFillColor(ACCENT); cv.rect(0, h*0.62+ h*0.02, w, 1.5*mm, fill=1, stroke=0)
    cv.setFillColor(colors.white); cv.setFont("Helvetica-Bold", 30)
    cv.drawString(22*mm, h*0.80, "SANCTIFY")
    cv.setFillColor(ACCENT); cv.setFont("Helvetica", 12)
    cv.drawString(23*mm, h*0.80-8*mm, "WORDPRESS SECURITY  \u2022  INCIDENT RESPONSE")
    cv.setFillColor(colors.white); cv.setFont("Helvetica-Bold", 24)
    cv.drawString(22*mm, h*0.50, "Malware Infection &")
    cv.drawString(22*mm, h*0.50-11*mm, "Remediation Report")
    cv.setFillColor(colors.HexColor("#AEC2DD")); cv.setFont("Helvetica", 12)
    cv.drawString(22*mm, h*0.40, "Casino Pride  \u2014  https://www.cpofficial.in")
    # meta box
    cv.setFillColor(colors.HexColor("#12325A")); cv.roundRect(22*mm, h*0.16, w-44*mm, h*0.16, 4, fill=1, stroke=0)
    cv.setFillColor(colors.white); cv.setFont("Helvetica-Bold", 9.5)
    rows = [("Threat", "\u201cSmooth Backup Ink\u201d (SCV) self-healing PHP malware"),
            ("Severity", "Critical"),
            ("Status", "RESOLVED \u2014 site clean, active protection deployed"),
            ("Report date", REPORT_DATE),
            ("Prepared by", "Sanctify  \u2022  www.sanctify.in")]
    y = h*0.16 + h*0.16 - 9*mm
    for k, v in rows:
        cv.setFont("Helvetica-Bold", 9.5); cv.setFillColor(ACCENT); cv.drawString(27*mm, y, k+":")
        cv.setFont("Helvetica", 9.5); cv.setFillColor(colors.white); cv.drawString(58*mm, y, v)
        y -= 6.6*mm
    cv.setFillColor(colors.HexColor("#7E93AE")); cv.setFont("Helvetica", 7.5)
    cv.drawString(22*mm, 12*mm, "CONFIDENTIAL \u2014 intended for the site owner. Contains security-sensitive details.")
    cv.restoreState()

def tbl(data, colw, header_bg=NAVY, header_fg=True):
    t = Table(data, colWidths=colw, repeatRows=1)
    st = [("BACKGROUND",(0,0),(-1,0),header_bg),
          ("VALIGN",(0,0),(-1,-1),"TOP"),
          ("LINEBELOW",(0,0),(-1,0),0.6,header_bg),
          ("GRID",(0,0),(-1,-1),0.4,LINE),
          ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,LIGHT]),
          ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
          ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6)]
    t.setStyle(TableStyle(st))
    return t

def bullets(items, stylefn=None):
    li = [ListItem(Paragraph(x, bullet), leftIndent=6, value="\u2022") for x in items]
    return ListFlowable(li, bulletType="bullet", bulletColor=BLUE, start="\u2022", leftIndent=10)

def P(t, s=body): return Paragraph(t, s)

story = []

# ===== 1. Executive Summary =====
story.append(P("Executive Summary", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P(
    "On 5 September 2026, Sanctify performed a security assessment of the WordPress website "
    "<b>Casino Pride (https://www.cpofficial.in)</b> and identified an active, <b>self-healing malware "
    "infection</b> belonging to the \u201cSmooth Backup Ink\u201d (internal marker <font face='Courier'>SCV</font>) family. "
    "The malware executed on every page request, disguised itself as a legitimate plugin, and could "
    "rebuild itself after any file was deleted \u2014 which is why earlier cleanup attempts had not held."))
story.append(P(
    "Sanctify fully removed the infection, eliminated every persistence and re-entry mechanism "
    "(including a database-level cron backdoor and a rogue administrator account), verified that the "
    "site no longer regenerates the malware, and deployed a purpose-built defensive plugin \u2014 "
    "<b>Sanctify Falcon</b> \u2014 to prevent recurrence. The website is now clean and serving normal content."))

summary = [
    [P("Area", cellw), P("Outcome", cellw)],
    [P("Infection", cell), P("Fully removed and verified", cell)],
    [P("Persistence (cron / users / plugins)", cell), P("Eliminated at the source", cell)],
    [P("Re-infection test", cell), P("Passed \u2014 no regeneration after forcing wp-cron", cell)],
    [P("Ongoing protection", cell), P("Sanctify Falcon plugin installed & active", cell)],
    [P("Website availability", cell), P("Online throughout; content & layout intact", cell)],
]
story.append(Spacer(1, 4))
story.append(tbl(summary, [70*mm, 100*mm]))

# ===== 2. What the malware was =====
story.append(P("1. The Infection", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P("Nature of the threat", h2))
story.append(P(
    "The site was infected with a sophisticated PHP malware that masqueraded as a fake plugin named "
    "<b>\u201cSmooth Backup Ink\u201d</b>. Rather than a single malicious file, it was a <b>multi-layered, "
    "self-repairing system</b> engineered to survive cleanup. Its defining trait was persistence: even "
    "if the visible payload was deleted, hidden components and a scheduled task quietly recreated it."))
story.append(P("How it worked (attack chain)", h2))
story.append(bullets([
    "<b>Execution trigger:</b> hidden <font face='Courier'>.user.ini</font> and <font face='Courier'>.htaccess</font> "
    "directives forced a malicious loader to run before <i>every</i> PHP page load, invisibly.",
    "<b>Loader &amp; dropper:</b> the loader called a hidden, obfuscated \u201cdropper\u201d that checked whether the "
    "payload existed and <b>recreated it</b> from any surviving copy.",
    "<b>Payloads:</b> multiple large encoded files (a fake mu-plugin auto-loaded by WordPress, a fake "
    "database dropin, and hidden state files) carried the actual malicious logic.",
    "<b>Database backdoor:</b> scheduled WordPress cron tasks re-dropped the files on a timer, triggered by "
    "ordinary visitor traffic \u2014 the true reason it kept returning.",
    "<b>Access backdoor:</b> a rogue administrator account allowed the attacker to simply log back in.",
]))
story.append(P("Why previous cleanups failed", h2))
story.append(P(
    "Deleting the malware files alone was never enough: the scheduled database task and the backdoor "
    "admin account remained, so the infection regenerated automatically. A permanent fix required "
    "removing the <b>root cause</b> \u2014 the persistence in the database and the unauthorized access \u2014 not just "
    "the symptoms on disk.", body))

# ===== 3. Findings table =====
story.append(PageBreak())
story.append(P("2. Detailed Findings", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
findings = [
    [P("Component", cellw), P("Description", cellw), P("Severity", cellw)],
    [P("Malicious auto-run triggers", cell), P("<font face='Courier'>.user.ini</font> &amp; <font face='Courier'>.htaccess</font> forcing a loader on every request", cell), P("Critical", S("c",parent=cell,textColor=RED,fontName="Helvetica-Bold"))],
    [P("Loader + hidden dropper", cell), P("Regenerated the payload from backup copies (self-heal)", cell), P("Critical", S("c",parent=cell,textColor=RED,fontName="Helvetica-Bold"))],
    [P("Fake mu-plugin & dropin", cell), P("Large encoded payloads auto-loaded by WordPress", cell), P("Critical", S("c",parent=cell,textColor=RED,fontName="Helvetica-Bold"))],
    [P("Malicious cron tasks", cell), P("Scheduled DB events re-dropping files on a timer", cell), P("Critical", S("c",parent=cell,textColor=RED,fontName="Helvetica-Bold"))],
    [P("Rogue administrator", cell), P("Auto-generated <font face='Courier'>backup_*</font> admin account (attacker access)", cell), P("Critical", S("c",parent=cell,textColor=RED,fontName="Helvetica-Bold"))],
    [P("Planted active plugin", cell), P("Attacker-installed \u201cEasypost\u201d plugin", cell), P("High", S("c",parent=cell,textColor=colors.HexColor('#B5651D'),fontName="Helvetica-Bold"))],
    [P("Re-infection seed", cell), P("Zipped payload staged inside an old theme folder", cell), P("High", S("c",parent=cell,textColor=colors.HexColor('#B5651D'),fontName="Helvetica-Bold"))],
    [P("Fake \u201cloader\u201d plugins", cell), P("Empty attacker-scaffolded plugin directories", cell), P("Medium", S("c",parent=cell,textColor=GREY,fontName="Helvetica-Bold"))],
]
story.append(tbl(findings, [42*mm, 96*mm, 22*mm]))
story.append(Spacer(1, 6))
story.append(P("Confirmed clean", h2))
story.append(P(
    "The active theme and its <font face='Courier'>functions.php</font> (integrity-verified), "
    "<font face='Courier'>wp-config.php</font>, WordPress core, and legitimate plugins/uploads were "
    "examined and found <b>free of injected code</b>. The website\u2019s public HTML and JavaScript served "
    "to visitors contained no malicious scripts or redirects.", body))

# ===== 4. Resolution =====
story.append(P("3. How Sanctify Resolved It", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P(
    "Remediation followed a disciplined order: <b>neutralise the triggers first</b> (to stop the self-heal), "
    "then remove payloads, then eliminate the database and access backdoors, and finally verify and "
    "harden. Every file changed was backed up beforehand, and the site remained online throughout.", body))
steps = [
    [P("#", cellw), P("Action taken", cellw), P("Result", cellw)],
    [P("1", cell), P("Neutralised malicious <font face='Courier'>.user.ini</font> and cleaned injected <font face='Courier'>.htaccess</font> (kept all legitimate rules)", cell), P("Execution trigger disabled", cell)],
    [P("2", cell), P("Deleted loader, dropper, and all payload files; removed hidden malware directory and fake plugin", cell), P("Payloads removed", cell)],
    [P("3", cell), P("Cleared 5 malicious scheduled tasks from the database", cell), P("Self-heal engine stopped", cell)],
    [P("4", cell), P("Removed the rogue administrator account (content reassigned safely)", cell), P("Attacker access revoked", cell)],
    [P("5", cell), P("Removed the planted plugin, the zipped re-infection seed, and empty fake plugins", cell), P("Re-entry seeds removed", cell)],
    [P("6", cell), P("Hardened <font face='Courier'>wp-content</font> to block direct PHP execution", cell), P("Attack class blocked", cell)],
    [P("7", cell), P("Built &amp; deployed the Sanctify Falcon protection plugin", cell), P("Continuous defense active", cell)],
]
story.append(tbl(steps, [8*mm, 118*mm, 44*mm]))
story.append(Spacer(1, 6))
story.append(P("Verification", h2))
story.append(P(
    "To prove the fix is permanent, Sanctify explicitly triggered the WordPress scheduler "
    "(<font face='Courier'>wp-cron.php</font>) \u2014 the exact mechanism the malware used to regenerate \u2014 and "
    "waited. <b>Nothing reappeared.</b> The malicious files, directories, triggers, and cron tasks all "
    "stayed gone, and the website continued to return normal pages (HTTP 200) with correct content.", body))

# ===== 5. Sanctify Falcon =====
story.append(PageBreak())
story.append(P("4. Ongoing Protection \u2014 Sanctify Falcon", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P(
    "Sanctify developed and installed a custom WordPress security plugin, <b>Sanctify Falcon</b> "
    "(www.sanctify.in), built specifically to defend against this malware family and similar "
    "self-healing infections. It runs automatically on every request and on an hourly schedule.", body))
story.append(P("Active defenses", h2))
story.append(bullets([
    "<b>File defense</b> \u2014 automatically removes known dropper/loader/payload files if they ever reappear.",
    "<b>Trigger guard</b> \u2014 sanitises malicious auto-run directives re-injected into <font face='Courier'>.user.ini</font> or <font face='Courier'>.htaccess</font>.",
    "<b>Cron cleaner</b> \u2014 removes malicious and rogue scheduled tasks while protecting all legitimate ones.",
    "<b>Backdoor-admin detection</b> \u2014 detects auto-generated <font face='Courier'>backup_*</font> admin accounts, demotes them, and flags them for review.",
    "<b>Uploads quarantine</b> \u2014 isolates any dangerous PHP dropped into the media folder.",
    "<b>Dashboard &amp; logging</b> \u2014 a \u201cSanctify Falcon\u201d admin screen with an on-demand scan and a full activity log.",
]))
story.append(P(
    "The plugin is intentionally conservative: it never deletes user accounts (it demotes and flags), "
    "and only acts on files/tasks that match strict malware signatures, with an allow-list protecting "
    "legitimate plugin files.", small))

# ===== 6. Recommendations =====
story.append(P("5. Recommendations", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P("The infection is resolved and active protection is in place. To fully close the loop, Sanctify recommends the following owner actions:", body))
story.append(bullets([
    "<b>Rotate all credentials</b> \u2014 WordPress administrators, hosting/FTP, and database password (with fresh security keys). Revoke any temporary access provided for this engagement.",
    "<b>Update or replace higher-risk plugins</b> \u2014 file-manager, slider, and theme-addon plugins are common entry points; ensure they are on the latest versions or removed if unused.",
    "<b>Reinstall WordPress core</b> of the same version to guarantee core file integrity.",
    "<b>Keep Sanctify Falcon active</b> and review its dashboard/log periodically.",
    "<b>Remove any nulled/pirated plugins or themes</b>, the most frequent source of such infections.",
    "<b>Request reputation review</b> with Google Search Console and Malwarebytes so any residual \u201cflagged\u201d status from the infection period is cleared.",
]))

# ===== 7. IOC appendix =====
story.append(P("Appendix \u2014 Indicators of Compromise (IOCs)", h1))
story.append(HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=8))
story.append(P("For future monitoring, the following indicators identify this malware family:", small))
ioc = [
    [P("Type", cellw), P("Indicators", cellw)],
    [P("Files / dirs", cell), P("<font face='Courier'>64f6b5eb.php, .64f6b5eb.php, ed0c7e2b.php, db.php (SC_DB), 865fa429.zip, bce0f3b9.php, .sc_&lt;hex&gt;/, mu-plugins/smooth-backup-ink.php</font>", cell)],
    [P("Cron hooks", cell), P("<font face='Courier'>sc_cron_fetch, my_monitoring_cron</font>, random 16+ character hex hook names", cell)],
    [P("Users", cell), P("<font face='Courier'>backup_&lt;hex&gt;</font> administrator accounts with auto-generated emails", cell)],
    [P("Content markers", cell), P("<font face='Courier'>SCV:4.3.24, SC_DB_BEGIN, Smooth Backup Ink, auto_prepend_file</font>", cell)],
]
story.append(tbl(ioc, [30*mm, 140*mm]))
story.append(Spacer(1, 10))
story.append(P("\u2014 End of report \u2014", S("end", parent=small, alignment=TA_CENTER)))
story.append(P("Prepared by Sanctify \u2022 www.sanctify.in \u2022 " + REPORT_DATE,
               S("cr", parent=small, alignment=TA_CENTER)))

# ---------- build ----------
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=24*mm, bottomMargin=18*mm, title="Sanctify Incident Report - cpofficial.in",
                      author="Sanctify", subject="Malware Infection & Remediation Report")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[Frame(0,0,A4[0],A4[1],id="c")], onPage=cover),
    PageTemplate(id="content", frames=[frame], onPage=header_footer),
])

from reportlab.platypus import NextPageTemplate
flow = [NextPageTemplate("content"), PageBreak()] + story
doc.build(flow)
print("PDF written:", OUT)
