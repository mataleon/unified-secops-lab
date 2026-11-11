#!/usr/bin/env bash
# Sends lab-only CEF and Syslog test messages to the local rsyslog listener.
# Run on the Linux forwarder (ubu-fwd-01). All values are synthetic.
set -euo pipefail
TARGET="${1:-127.0.0.1}"

for i in $(seq 1 5); do
  logger -p local4.warn -n "$TARGET" -P 514 -T --rfc3164 -t CEF \
    "CEF:0|VCBHN-Lab|LabFirewall|1.0|100|Traffic denied|5|src=10.10.1.$i dst=203.0.113.10 spt=5$i$i$i dpt=4444 proto=TCP act=deny"
done

# Plain syslog on a different facility (auth) so it lands in the Syslog table, not CommonSecurityLog
logger -p auth.warning -n "$TARGET" -P 514 -T --rfc3164 -t sshd \
  "Failed password for invalid user labtest from 198.51.100.7 port 51515 ssh2"

echo "Sent 5 CEF + 1 syslog test messages to $TARGET:514 (TCP)."
