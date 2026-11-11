# BEC investigation — victim.user

## Summary
(3–4 sentences: what happened, impact, status)

## Timeline
| Time (UTC) | Source | Event |
|---|---|---|
| | EmailEvents | Phishing email delivered |
| | UrlClickEvents | User clicked link |
| | SigninLogs | Sign-in from unfamiliar IP |
| | Purview Audit | New-InboxRule with ForwardTo |
| | MailItemsAccessed | Messages read |
| | MicrosoftGraphActivityLogs | API calls during attacker session |

## Scope
- Mailboxes that received the phish:
- Messages accessed:
- Data forwarded externally:

## Remediation
| Step | Done | Evidence |
|---|---|---|
| Soft-delete phish (Explorer) | | |
| Disable account / revoke sessions | | |
| Reset password, review MFA methods | | |
| Remove inbox rule / forwarding | | |
| Block sender/URL (Tenant Allow/Block List) | | |

## Prevent next time
- 
