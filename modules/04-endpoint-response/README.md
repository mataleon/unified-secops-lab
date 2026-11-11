# Module 04 — Endpoint response & case management

**SC-200 objectives:** Respond to alerts and incidents in Defender for Endpoint (device timeline, live response, investigation packages, evidence & entities, attack disruption) · Investigate complex attacks · Manage incidents with case management
**Time:** 2 evenings

## Scenario
`attacker.sim` runs a benign "attack chain" on `win11-ep-01`: encoded PowerShell → discovery commands → scheduled task persistence → EICAR drop. You investigate and respond like a Tier 2 analyst.

Emulation (run in an elevated PowerShell on the lab VM only):
```powershell
$cmd = 'whoami; hostname; net user; nltest /dclist:'
powershell.exe -NoProfile -EncodedCommand ([Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($cmd)))
schtasks /create /tn "VCBHN-Lab-Updater" /tr "cmd.exe /c echo lab" /sc daily /st 23:00 /f
'X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' | Out-File "$env:TEMP\eicar-lab.txt" -Encoding ascii
```

## Lab 4.1 — Investigate
1. Open the incident: **attack story**, incident graph, alerts, evidence.
2. Device page → **Timeline**: filter to the attack window, **flag** each step, note the MITRE techniques shown.
3. Fill in [investigation-report.md](investigation-report.md).

## Lab 4.2 — Respond
1. **Isolate device → Selective** (Outlook/Teams keep working). Release afterwards.
2. **Collect investigation package**; open the zip and list what you found in each folder in the report.
3. **Live response**: upload [live-response/Get-LabTriage.ps1](live-response/Get-LabTriage.ps1) to the library, then:
   ```
   connect
   processes
   scheduledtasks
   run Get-LabTriage.ps1
   getfile C:\ProgramData\VCBHN-Triage\triage.txt
   remediate scheduledtask "VCBHN-Lab-Updater"
   ```
4. File page for the EICAR file: **Stop and quarantine**, add a **block indicator**.

## Lab 4.3 — Case management
1. Open the incident as an **incident case**: assign to yourself, add tasks (Contain, Eradicate, Recover, Lessons learned) with due dates, add a comment and attach the triage file.
2. Create a **generic case** "Q4 hunt – scheduled task persistence" and link it.
3. Query `SecurityCaseEvent` to show the audit trail.

## Lab 4.4 — Attack disruption review (read-only in the lab)
Attack disruption needs real high-confidence multi-stage attacks, so it may not trigger in a small lab. Document instead:
- Settings → Microsoft Defender XDR → **Automated response** exclusions you configured (Module 03)
- How you would **release** a contained device/user
- The hunting query `DisruptionAndResponseEvents | where Timestamp > ago(30d)` and what it would show

## Done when
- [ ] Investigation report complete with timeline and MITRE mapping
- [ ] Isolation, investigation package, live response and file actions done (screenshots)
- [ ] Incident case with tasks + generic case
- [ ] Attack disruption section documented
