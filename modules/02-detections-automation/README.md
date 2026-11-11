# Module 02 — Detections & automation

**SC-200 objectives:** Configure detections · Configure automation for Defender XDR and Microsoft Sentinel
**Time:** 3–4 evenings · **Prereq:** Module 01 data flowing

## Lab 2.1 — Deploy the analytics rules in [rules/](rules/)

Rules are stored as YAML (Sentinel content format) and checked by CI. Create each one in Sentinel → Analytics → **Create scheduled rule** / **NRT rule**, copying the query, schedule, entity mapping and custom details.

For every rule:
1. Emulate the activity (see each rule's description).
2. Confirm an incident fires.
3. Fill in a write-up from [templates/detection-writeup.md](../../templates/detection-writeup.md) in `writeups/`.

Settings to practice on at least one rule each: **event grouping per result**, **suppression**, **alert grouping by entity**, **alert details override**, **custom details**.

## Lab 2.2 — Defender XDR custom detections

Run each query in [custom-detections/](custom-detections/) in Advanced hunting → **Create detection rule** → frequency **every hour** → action as noted in the file. Emulate with an encoded PowerShell `Write-Output` command on `win11-ep-01`.

## Lab 2.3 — Anomalies and UEBA
1. Settings → **Entity behavior analytics** → enable with SigninLogs, AuditLogs, AzureActivity, SecurityEvent.
2. Analytics → **Anomalies**: duplicate one anomaly rule, change its threshold, set the copy to **Flighting**.
3. After a few days, compare: `Anomalies | summarize count() by AnomalyTemplateName, RuleStatus`.

## Lab 2.4 — MITRE ATT&CK coverage
Sentinel → **MITRE ATT&CK** page → screenshot Active vs Simulated coverage before and after deploying the rules.

## Lab 2.5 — Automation rules and playbook
Follow [automation/automation-rules.md](automation/automation-rules.md) and [playbooks/README.md](playbooks/README.md).

## Done when
- [ ] 8 analytics rules deployed (6 scheduled, 2 NRT), each with a write-up
- [ ] 2 XDR custom detections deployed and triggered once
- [ ] Anomaly rule duplicated into Flighting
- [ ] MITRE coverage screenshots (before/after)
- [ ] Automation rules + playbook working end to end
