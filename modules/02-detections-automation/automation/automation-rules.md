# Automation rules

Create in Defender portal → Microsoft Sentinel → Configuration → Automation (or Azure portal → Sentinel → Automation).

| Order | Name | Trigger | Conditions | Actions | Purpose |
|---|---|---|---|---|---|
| 1 | AR01-Suppress-Lab-Scanner | Incident created | Entity IP equals `<forwarder IP>` AND analytics rule contains "brute force" | Change status → **Closed (Benign positive)**, add comment | Close known-benign noise (expires after 30 days) |
| 2 | AR02-Assign-Identity-Incidents | Incident created | Analytics rule name contains "Entra" | Assign owner → soc.responder · Add tag `identity` | Routing |
| 3 | AR03-Add-Triage-Tasks | Incident created | Severity = High | Add tasks: "Check sign-in logs", "Check device timeline", "Scope with Go hunt" | Consistent triage |
| 4 | AR04-Run-Notify-Playbook | Incident created | Severity = High | Run playbook `pb-vcbhn-notify-teams` | Notify the on-call channel |

## Done when
- [ ] All 4 rules created; screenshots of each in `../evidence/`
- [ ] A test incident shows the owner, tag and tasks applied automatically
- [ ] AR01 has an **expiration date** set

## Notes / exam traps I verified
- An automation rule can't list a playbook until **Microsoft Sentinel** has the **Microsoft Sentinel Automation Contributor** role on the playbook's resource group (Settings → Playbook permissions).
- "When alert is created" triggers can only run playbooks.
