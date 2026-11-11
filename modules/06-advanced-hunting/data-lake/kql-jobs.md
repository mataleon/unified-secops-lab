# KQL jobs (Sentinel data lake)

**Where:** Defender portal → Microsoft Sentinel → Data lake exploration → **KQL queries** (test) → **Create job**, or **Jobs → Create a new KQL job**.
**Permissions:** Entra **Security Operator** or **Security Administrator**. To create *new* analytics-tier tables, the data lake managed identity `msg-resources-<guid>` needs **Log Analytics Contributor** on the workspace.

## Job 1 — One-time: promote 90 days of failed sign-ins for an investigation

- Destination: new table `FailedSignins90d` (saved as `FailedSignins90d_KQL_CL`)

```kusto
SigninLogs
| where TimeGenerated between (ago(90d) .. now())
| where ResultType in ("50126", "50053")
| project OriginalTime = TimeGenerated, UserPrincipalName, IPAddress, ResultType,
          AppDisplayName, Country = tostring(LocationDetails.countryOrRegion)
```

## Job 2 — Scheduled daily: per-user sign-in baseline

- Schedule: daily · Destination: `SigninBaselineDaily_KQL_CL`
- Uses a 15-minute delay because lake data can arrive up to ~15 minutes late.

```kusto
let delay = 15m;
let endTime = now() - delay;
let startTime = endTime - 1d;
SigninLogs
| where TimeGenerated between (startTime .. endTime)
| summarize SignIns = count(), DistinctIPs = dcount(IPAddress),
            Countries = make_set(tostring(LocationDetails.countryOrRegion), 20),
            Apps = dcount(AppDisplayName)
    by UserPrincipalName, Day = startofday(TimeGenerated)
```

## Limits I confirmed (record what you observe)
| Limit | Value |
|---|---|
| Concurrent job runs per tenant | 5 |
| Enabled jobs per tenant | 100 |
| Job timeout | 1 hour |
| Output tables per job | 1 |

## Evidence
Jobs page screenshot (status, last/next run), job history, and a query on each destination table.
