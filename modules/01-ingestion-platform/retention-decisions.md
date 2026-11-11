# Retention and tier decisions

| Table | Tier | Analytics retention | Total retention | Reason |
|---|---|---|---|---|
| SecurityEvent | Analytics | 180 days | 2 years | Real-time detections + investigations |
| SigninLogs | Analytics | 90 days | 2 years | Identity detections (NRT/scheduled) |
| CommonSecurityLog | Data lake | — | 1 year | High volume, low value for real-time; queried via KQL jobs/summary rules |
| DeviceProcessEvents (XDR) | XDR default + lake | 30 days (free) | 1 year | Cheap long-term hunting |
| | | | | |
