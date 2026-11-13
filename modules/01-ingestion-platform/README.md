# Module 01 — Data ingestion & platform

**SC-200 objectives:** Configure the Microsoft Sentinel SIEM and platform · Ingest data into the Microsoft Sentinel SIEM and platform
**Time:** 2–3 evenings · **Prereq:** [Lab 0](../../docs/lab-setup.md)

## Lab 1.1 — RBAC: least privilege in practice

1. Assign on the workspace resource group: `soc.reader` → **Microsoft Sentinel Reader**, `soc.responder` → **Microsoft Sentinel Responder**, `soc.engineer` → **Microsoft Sentinel Contributor**.
2. Sign in as each user. Try to (a) close an incident, (b) edit an analytics rule, (c) run a playbook.
3. Record the results in [rbac-matrix.md](rbac-matrix.md).

**Done when:** the matrix is filled in with what each role could and couldn't do.

## Lab 1.2 — Windows Security events via AMA (+ custom XPath DCR)

1. Content hub → install **Windows Security Events**.
2. Connector **Windows Security Events via AMA** → Create DCR → select `win-srv-01` → **Common** event set.
3. Deploy the second DCR in [dcr/windows-security-custom-xpath.json](dcr/windows-security-custom-xpath.json) (logons, failed logons, log cleared, new services, Kerberos TGS):
   ```bash
   az deployment group create -g rg-secops-lab \
     --template-file dcr/windows-security-custom-xpath.json \
     --parameters workspaceResourceId=<workspace resource ID>
   ```
   Then associate it with `win-srv-01` (DCR → Resources → Add).
4. Generate events: a few failed RDP/`runas` logons; `wevtutil cl Security` once (creates 1102).
5. Run [queries/validate-ingestion.kql](queries/validate-ingestion.kql).

**Done when:** `SecurityEvent` shows 4624, 4625 and 1102 from `win-srv-01`.

## Lab 1.3 — CEF and Syslog via AMA (Linux forwarder)

1. On `ubu-fwd-01`: run the forwarder installer from the **CEF via AMA** connector page (configures rsyslog on 514 TCP/UDP).
2. Create a **CEF via AMA** DCR (facility `local4`, LOG_INFO+) and a **Syslog via AMA** DCR for `auth`/`authpriv` only. Keep facilities separate to avoid duplicates.
3. Send test data with [cef/send-test-cef.sh](cef/send-test-cef.sh).
4. Validate with `CommonSecurityLog` and `Syslog` queries in [queries/validate-ingestion.kql](queries/validate-ingestion.kql).

**Done when:** test CEF events appear **only** in `CommonSecurityLog`.

## Lab 1.4 — Azure Activity via Azure Policy

1. Content hub → **Azure Activity** → connector → **Launch Azure Policy Assignment wizard**.
2. Scope: your subscription · Workspace: `law-vcbhn-sentinel` · ✅ **Create a remediation task**.
3. Create/delete a test resource group, then query `AzureActivity`.

**Done when:** your test operations appear in `AzureActivity`. Screenshot the remediation task.

## Lab 1.5 — Threat intelligence

1. Add 3 manual indicators (Defender portal → Threat intelligence → Intel management): one IP you control (e.g. your forwarder's public IP), one domain, one file hash.
2. Optional: connect a public **TAXII** feed or the **MDTI** connector.
3. Query `ThreatIntelIndicators`. (The legacy `ThreatIntelligenceIndicator` table is retired.)

**Done when:** indicators are queryable and used by the TI rule in Module 02.

## Lab 1.6 — Custom table with the Logs ingestion API

1. Workspace → Tables → **Create → New custom log (DCR-based)** → name `VCBHNApp` (becomes `VCBHNApp_CL`); upload [custom-table/sample.json](custom-table/sample.json) as the schema sample; transformation: `source | extend TimeGenerated = todatetime(EventTime)`.
2. Register an Entra app, create a certificate or secret, grant it **Monitoring Metrics Publisher** on the DCR.
3. Run [custom-table/send_logs.py](custom-table/send_logs.py).

**Done when:** `VCBHNApp_CL | take 10` returns your events.

## Lab 1.7 — Retention tiers, data lake and SOC optimization

1. Defender portal → Microsoft Sentinel → Configuration → **Tables**:
   - `SecurityEvent`: analytics 180 days, total 2 years.
   - `CommonSecurityLog`: switch to **Data lake tier** (high-volume firewall data).
2. Record decisions and reasons in [retention-decisions.md](retention-decisions.md).
3. Open **SOC optimization**; screenshot and summarize each recommendation.
4. Install the **Data collection health** and **Workspace usage report** workbooks.

**Done when:** the decisions table is complete with a reason for each table.

## Results (run on 2026-11-11 to 2026-11-13)

Built in my own lab tenant: workspace `law-secops-lab` (West US 2), VM `vm-win-01` (Windows Server 2022, AMA, Defender for Servers P2). Screenshots are cropped Cloud Shell output with no tenant, subscription or IP data.

| Lab | Result | Evidence |
|---|---|---|
| 1.1 RBAC | Reader / Responder / Contributor assigned to 3 test users as **PIM-eligible**; matrix in [rbac-matrix.md](rbac-matrix.md) | — |
| 1.2 Windows Security events (AMA + custom XPath DCR) | 4624, 4625 and 1102 collected from `vm-win-01` | [screenshot](evidence/lab12-securityevent-4624-4625-1102.png) |
| 1.4 Azure Activity via Azure Policy | Remediation succeeded; test resource group create/delete landed in `AzureActivity` | [screenshot](evidence/lab14-18-azureactivity-signin-audit.png) |
| 1.8 Microsoft Entra ID | Diagnostic setting with 7 categories; `SigninLogs` shows a success and a 50126 (bad password) failure; `AuditLogs` flowing | [setting](evidence/lab18-entra-id-diagnostic-setting.png) · [data](evidence/lab14-18-azureactivity-signin-audit.png) |

### What went wrong and what I learned

- **Azure Activity policy at the wrong scope.** I first assigned it to the resource group. The policy targets the *subscription* resource, which sits outside any resource group, so the remediation found nothing to fix. Reassigning it at subscription scope fixed it right away.
- **Overlapping DCRs.** The connector's *Common* DCR and my custom XPath DCR both collect 4624/4625, so those events arrive twice. In production I'd keep one DCR per event set.
- **Noise, not cost (yet).** Event 4673 (privileged service call) was about 915 events in 3 hours, more than everything else combined. Total `SecurityEvent` volume was still only about 0.004 GB over 3 days, so it was a signal-to-noise problem rather than a bill. It gets filtered in Lab 1.7.
- **Defender XDR connector.** With the workspace onboarded to the unified Defender portal, the connector's "incidents and alerts" option is disabled by design. Incidents sync natively.
- **Brand-new subscription has 0 vCPU quota for most VM families.** B-series had no capacity in West US 2, so the VM landed on D2ads_v7. Check `az vm list-usage` before choosing a size.

## Evidence

Put sanitized screenshots in [evidence/](evidence/). See the [evidence checklist](../../templates/module-evidence-checklist.md).
