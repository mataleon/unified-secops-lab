# Lab 0 — Build the lab

**Goal:** a working Microsoft unified SecOps environment for all six modules.
**Time:** 2–3 hours · **Cost:** $0 during trials (see [cost-guide.md](cost-guide.md))

## 1. Accounts

| What | Why | Notes |
|---|---|---|
| Microsoft 365 E5 trial (30 days) | Defender XDR, MDE, MDO, MDI, MDCA, Purview, Entra ID P2 | Create a new lab tenant, e.g. `vcbhnlab.onmicrosoft.com`. Never use a work tenant |
| Azure subscription (free account or pay-as-you-go) | Log Analytics, Sentinel, VMs, Logic Apps | Link it to the **same** lab tenant |

## 2. Azure resources (one resource group)

```bash
az group create -n rg-secops-lab -l westus2
az monitor log-analytics workspace create -g rg-secops-lab -n law-vcbhn-sentinel -l westus2
```

1. Enable **Microsoft Sentinel** on `law-vcbhn-sentinel` (Azure portal → Microsoft Sentinel → Create). The 31-day free trial starts now.
2. Defender portal (security.microsoft.com) → **System → Settings → Microsoft Sentinel → Connect a workspace** → choose it as the primary workspace.
3. Onboard to the **Sentinel data lake** (Defender portal banner / Settings → Microsoft Sentinel → Data lake). Note the managed identity `msg-resources-<guid>` it creates.

## 3. Virtual machines

| VM | Size | Purpose |
|---|---|---|
| `win-srv-01` Windows Server 2022 | B2s | Security events via AMA, WEF collector (optional) |
| `ubu-fwd-01` Ubuntu 22.04 | B2ats v2 (free tier eligible) | CEF/Syslog forwarder |
| `win11-ep-01` Windows 11 | B2s | Onboarded to Defender for Endpoint |

Set **auto-shutdown** on every VM (VM → Operations → Auto-shutdown → 11:00 PM).

## 4. Onboard the Windows 11 VM to Defender for Endpoint

Defender portal → **Settings → Endpoints → Onboarding** → Windows 10/11 → **Local script** → run as admin on `win11-ep-01`. Verify:

```powershell
Get-MpComputerStatus | Select AMRunningMode, RealTimeProtectionEnabled
```

Then run a detection test from the onboarding page and confirm an alert appears within ~30 minutes.

## 5. Lab users

Create test users in Entra ID: `soc.reader`, `soc.responder`, `soc.engineer`, `victim.user`, `attacker.sim`. Give `victim.user` an E5 license (mailbox for Module 05).

## Done when

- [ ] Sentinel workspace visible in the Defender portal
- [ ] Data lake onboarding complete
- [ ] `win11-ep-01` shows **Onboarded** in Device inventory
- [ ] Budget alert and VM auto-shutdown configured
