# Module 05 — Microsoft 365 investigation: business email compromise (BEC)

**SC-200 objectives:** Investigate and remediate threats with Defender for Office 365 · compromised identities (Entra ID) · Purview Audit · Content search (eDiscovery) · Microsoft Graph activity logs · Defender for Cloud Apps
**Time:** 2–3 evenings

## Scenario
`victim.user` receives a phishing email, "signs in" from an unfamiliar IP (use a VPN or a cloud VM browser), creates an inbox rule forwarding mail containing "invoice" to an external address, and reads several messages. You scope and remediate.

## Prep
- Turn on **Audit** (Purview) if it isn't on; it's on by default for new tenants.
- Entra diagnostic settings → send `SignInLogs`, `AuditLogs`, `NonInteractiveUserSignInLogs`, `MicrosoftGraphActivityLogs` to the Sentinel workspace.
- Office 365 connector in Sentinel (Exchange) → `OfficeActivity`.

## Lab 5.1 — Email
1. Send a lab "phish" from an external mailbox to `victim.user`.
2. **Threat Explorer**: find it by sender/subject → check delivery location, URLs, authentication results → **Soft delete** from all mailboxes. Submit it to Microsoft as phish.
3. Hunt: [queries/bec-hunting.kql](queries/bec-hunting.kql) (EmailEvents, UrlClickEvents).

## Lab 5.2 — Identity
1. Find the risky sign-in (Entra ID Protection → Risky sign-ins) and correlate in `SigninLogs`.
2. Remediate in order: **disable account → revoke sessions → reset password → review MFA methods**.

## Lab 5.3 — Mailbox activity
1. **Purview Audit** search: `New-InboxRule`, `Set-InboxRule`, `MailItemsAccessed` for `victim.user` (MailItemsAccessed requires Audit Premium / E5).
2. Or run [scripts/Search-BecAudit.ps1](scripts/Search-BecAudit.ps1).
3. Remove the inbox rule; check mailbox forwarding (`Get-Mailbox | fl ForwardingSmtpAddress`).

## Lab 5.4 — Content search
Purview → eDiscovery → **Content search** with `subject:"invoice" AND received>=2026-11-01`. Export the report. Note: this uses **Keyword Query Language**, not Kusto.

## Lab 5.5 — Graph activity logs
Run the Graph section of [queries/bec-hunting.kql](queries/bec-hunting.kql) to see which Graph API calls the user's sessions made, joined to sign-ins by token ID.

## Lab 5.6 — Write-up
Complete [bec-report.md](bec-report.md): timeline, scope (how many mailboxes/messages), actions, and the preventive controls you'd add (Conditional Access, phishing-resistant MFA, outbound forwarding policy).

## Done when
- [ ] Phish removed with Explorer, audit evidence of the inbox rule, Content search report, Graph log correlation, identity remediated, report written
