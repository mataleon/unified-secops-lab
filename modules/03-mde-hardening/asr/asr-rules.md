# ASR rules used in this lab

Rule GUIDs are from Microsoft's ASR rules reference. Re-check them against the current Microsoft Learn page ("Attack surface reduction rules reference") before deploying.

| Rule | GUID | Lab mode | Final mode |
|---|---|---|---|
| Block credential stealing from LSASS | 9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2 | Audit | **Block** (standard protection) |
| Block abuse of exploited vulnerable signed drivers | 56a863a9-875e-4185-98a7-b882c64b5ce5 | Audit | **Block** (standard protection) |
| Block persistence through WMI event subscription | e6db77e5-3df2-4cf1-b95a-636979351e5b | Audit | **Block** (standard protection) |
| Block all Office applications from creating child processes | d4f940ab-401b-4efc-aadc-ad5f3c50688a | Audit | Block after review |
| Block Office applications from creating executable content | 3b576869-a4ec-4529-8536-b80a7769e899 | Audit | Block after review |
| Block executable content from email client and webmail | be9ba2d9-53ea-4cdc-84e5-9b1eeee46550 | Audit | Block after review |
| Block execution of potentially obfuscated scripts | 5beb7efe-fd9a-4556-801d-275e5ffc04cc | Audit | Audit (noisy) |
| Block process creations from PSExec and WMI commands | d1e49aac-8f56-4280-b9ba-993a6d77406c | Audit | Audit (breaks some admin tools) |
| Use advanced protection against ransomware | c1db55ab-c21a-4637-bb3f-a12568109d35 | Audit | Block after review |
