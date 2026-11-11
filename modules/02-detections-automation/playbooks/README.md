# Playbook: pb-vcbhn-notify-teams

**Goal:** when a High-severity incident is created, post a Teams message with the incident title, severity, entities and a link, then add a comment to the incident.

## Build steps
1. Content hub → install **Microsoft Sentinel – Teams**/**SOAR Essentials** solution → Automation → Playbook templates → *Post message to Teams* (incident trigger) → Create.
2. Logic App → **Identity → System assigned: On**.
3. Grant the managed identity **Microsoft Sentinel Responder** on `rg-secops-lab`.
4. Designer: authorize the Teams connection; after the post step add **Add comment to incident (V3)** with "Notified SOC channel".
5. Attach via automation rule AR04.
6. Trigger a test incident and confirm the Logic App **Run history** shows success.

## Commit the artifact
Export the deployed playbook so the repo contains real code:

```bash
az group export -g rg-secops-lab --resource-ids $(az logic workflow show -g rg-secops-lab -n pb-vcbhn-notify-teams --query id -o tsv) > pb-vcbhn-notify-teams.json
```

Remove connection secrets and subscription IDs before committing.

## Stretch goal
Add an **entity-triggered** playbook that enriches an IP with a TI lookup and posts the result as an incident comment.
