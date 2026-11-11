# Cost guide

Prices change. Check the Azure pricing calculator before you start. Estimates below are for a small lab.

| Item | Cost | How to minimize |
|---|---|---|
| Microsoft Sentinel ingestion | Free up to 10 GB/day for the first 31 days, then pay-as-you-go per GB (region dependent) | Do Modules 01–02 inside the trial; set a **daily cap** of 1 GB on the workspace |
| Windows VMs | ~$1–2/day each if left on | Auto-shutdown; deallocate when idle |
| Linux forwarder | Free-tier VM sizes are available on new accounts | Use B2ats v2 / B1s |
| Logic Apps (Consumption) | Cents | — |
| Data lake queries / KQL jobs | Billed per data processed | Keep lookback windows short in the lab |
| **Security Copilot** | Billed in Security Compute Units; can be expensive | Don't provision in the lab; document from Microsoft Learn |

## Guardrails

```bash
# Daily cap on the workspace (GB)
az monitor log-analytics workspace update -g rg-secops-lab -n law-vcbhn-sentinel --quota 1
```

- Cost Management → **Budgets** → $25/month with email alert at 50/80/100%.
- When finished: `az group delete -n rg-secops-lab` (keep the code and screenshots in this repo).
