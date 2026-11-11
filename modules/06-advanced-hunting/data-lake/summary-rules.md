# Summary rule — hourly firewall summary

**Where:** Microsoft Sentinel → Configuration → **Summary rules** → Create · **Role:** Microsoft Sentinel Contributor

| Setting | Value |
|---|---|
| Name | SR-VCBHN-Firewall-Hourly |
| Destination | New custom table `FirewallHourlySummary` (→ `FirewallHourlySummary_CL`, analytics tier) |
| Frequency | Every 1 hour |
| Delay | 15 minutes |
| SummaryLogs diagnostic setting | Enabled (to see run history and failures) |

```kusto
CommonSecurityLog
| summarize Connections = count(),
            DeniedConnections = countif(DeviceAction in~ ("deny", "drop", "block")),
            DistinctPorts = dcount(DestinationPort),
            Ports = make_set(DestinationPort, 50)
    by SourceIP, DestinationIP, DeviceVendor, bin(TimeGenerated, 1h)
```

## Analytics rule on the summary (scheduled, hourly)

```kusto
FirewallHourlySummary_CL
| where TimeGenerated > ago(1h)
| where DistinctPorts > 50 or DeniedConnections > 200
| project TimeGenerated, SourceIP, DestinationIP, DistinctPorts, DeniedConnections
```

**Why this design:** raw firewall logs stay in the cheap data lake tier, while detections run on a small analytics-tier summary.
