# Module 03 — Defender for Endpoint hardening & Defender XDR settings

**SC-200 objectives:** Configure email/alert notifications · MDE advanced features · rules settings · custom data collection · security policies incl. ASR · AIR · attack disruption · device groups, permissions and automation levels
**Time:** 2–3 evenings · **Prereq:** `win11-ep-01` onboarded

## Lab 3.1 — Advanced features
Settings → Endpoints → General → **Advanced features**. Turn on: Automated investigation, Live response, Live response for servers, EDR in block mode, Allow or block file, **Custom network indicators**, Tamper protection, Web content filtering, Device discovery, Microsoft Defender for Cloud Apps, Download quarantined files.
Record each one and *why* in [advanced-features.md](advanced-features.md).

## Lab 3.2 — ASR rules: audit → review → block
1. Apply the rules in [asr/asr-rules.md](asr/asr-rules.md) in **Audit** mode with [asr/set-asr-audit.ps1](asr/set-asr-audit.ps1) (lab VM) or an Intune/security settings management ASR policy.
2. Generate test activity (e.g. Office macro spawning `cmd.exe` in a test doc).
3. Review with [queries/asr-and-indicators.kql](queries/asr-and-indicators.kql) and the **ASR rules report**.
4. Switch the three "standard protection" rules to **Block**.

## Lab 3.3 — Indicators
1. Import [indicators/lab-indicators.csv](indicators/lab-indicators.csv) (Settings → Endpoints → Indicators → Import). Download Microsoft's current CSV template first and match its headers.
2. Test the **IP block** from `win11-ep-01` (`Test-NetConnection <ip> -Port 443`). It only works when network protection is in **block mode** and **custom network indicators** is on. Prove both.

## Lab 3.4 — Device groups and automation levels
Create two device groups:

| Rank | Group | Rule | Automation level |
|---|---|---|---|
| 1 | VCBHN-Finance | Tag = `Finance` | Semi – require approval for any remediation |
| 2 | VCBHN-Workstations | OS = Windows 11 | Full – remediate threats automatically |
| last | Ungrouped devices | — | Full |

Tag `win11-ep-01` with `Finance`, trigger an EICAR test file, and show the action waiting in **Action center → Pending**. Remove the tag and repeat: it should remediate automatically.

## Lab 3.5 — Custom data collection
1. Settings → Endpoints → Rules → **Asset rule management** → dynamic tag `CDC-Pilot` for `win11-ep-01`.
2. Rules → **Custom Data Collection** → select the Sentinel workspace → new rule: table `DeviceCustomNetworkEvents`, outbound connections, condition `RemotePort equals 3389`, scope = tag `CDC-Pilot`.
3. Wait up to 1 hour, generate RDP attempts, then run the validation query in [queries/asr-and-indicators.kql](queries/asr-and-indicators.kql).

## Lab 3.6 — Defender XDR notifications and alert tuning
1. Settings → Microsoft Defender XDR → **Email notifications**: one rule each for Incidents (High), Actions, Threat analytics.
2. **Alert tuning**: hide alerts for a known lab admin script by command line; document the conditions.
3. **Automated response** (attack disruption): add your break-glass account as an excluded identity and document why.

## Done when
- [ ] Advanced features documented
- [ ] ASR audit events found, 3 rules moved to Block
- [ ] IP/URL/file indicators proven to block
- [ ] Two device groups showing different remediation behavior
- [ ] Custom data collection events in `DeviceCustom*` tables
- [ ] Notifications, alert tuning and attack disruption exclusion configured
