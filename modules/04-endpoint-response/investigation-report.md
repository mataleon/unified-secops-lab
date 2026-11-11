# Investigation report — VCBHN-INC-001

| Field | Value |
|---|---|
| Incident ID | |
| Severity / classification | |
| Affected assets | win11-ep-01, attacker.sim |
| Detection sources | |
| Analyst | Leon Kiyonga |

## Timeline
| Time (UTC) | Event | Evidence (table / page) | MITRE |
|---|---|---|---|
| | Encoded PowerShell executed | DeviceProcessEvents | T1059.001 |
| | Discovery commands (whoami, net user, nltest) | Timeline | T1033, T1087, T1482 |
| | Scheduled task created | DeviceEvents ScheduledTaskCreated | T1053.005 |
| | Test malware file written | DeviceFileEvents / AV detection | — |

## Investigation package findings
| Folder | What I checked | Finding |
|---|---|---|
| Autoruns | | |
| Scheduled tasks | | |
| Processes | | |
| Network connections | | |
| Prefetch | | |

## Response actions
| Action | Time | Result |
|---|---|---|

## Root cause and recommendations
- 
