# Lessons learned

A running log. Recruiters read this file: it shows how I troubleshoot.

| Date | Module | What broke | Root cause | Fix | What I learned |
|---|---|---|---|---|---|
| YYYY-MM-DD | 01 | *Example:* CEF events showed up twice | Same facility (local4) in both the Syslog and CEF DCRs | Removed local4 from the Syslog DCR | Use separate facilities for CEF and Syslog on one forwarder |
