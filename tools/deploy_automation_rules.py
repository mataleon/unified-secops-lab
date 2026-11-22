#!/usr/bin/env python3
"""Deploy the Sentinel automation rules AR01-AR03 described in
modules/02-detections-automation/automation/automation-rules.md.

AR04 (run playbook) is left out until the notify playbook exists and Sentinel has the
Microsoft Sentinel Automation Contributor role on its resource group.

Usage:
    python3 tools/deploy_automation_rules.py --subscription <id> --resource-group rg-secops-lab \
        --workspace law-secops-lab --responder-upn soc.responder@<tenant>.onmicrosoft.com
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
import tempfile
import os

API = "2024-03-01"
BRUTE_FORCE_RULE_ID = "9c3acaf7-906a-41b0-b72d-add04e5b0620"


def az(*args):
    out = subprocess.run(["az", *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return out.stdout.strip()


def rules(ws_id, responder_oid, responder_upn):
    expires = (dt.datetime.utcnow() + dt.timedelta(days=30)).replace(microsecond=0).isoformat() + "Z"
    brute_force_rule = f"{ws_id}/providers/Microsoft.SecurityInsights/alertRules/{BRUTE_FORCE_RULE_ID}"
    return {
        "ar01-suppress-lab-runas": {
            "displayName": "AR01-Suppress-Lab-Local-Runas-Tests",
            "order": 1,
            "triggeringLogic": {
                "isEnabled": True,
                "expirationTimeUtc": expires,
                "triggersOn": "Incidents",
                "triggersWhen": "Created",
                "conditions": [
                    {"conditionType": "Property", "conditionProperties": {
                        "propertyName": "IncidentRelatedAnalyticRuleIds", "operator": "Contains",
                        "propertyValues": [brute_force_rule]}},
                    {"conditionType": "Property", "conditionProperties": {
                        "propertyName": "IPAddress", "operator": "Equals", "propertyValues": ["::1"]}},
                ],
            },
            "actions": [
                {"order": 1, "actionType": "ModifyProperties", "actionConfiguration": {
                    "status": "Closed", "classification": "BenignPositive",
                    "classificationReason": "SuspiciousButExpected",
                    "classificationComment": "AR01: local runas failures from lab testing (source ::1). Rule expires after 30 days."}},
            ],
        },
        "ar02-assign-identity": {
            "displayName": "AR02-Assign-Identity-Incidents",
            "order": 2,
            "triggeringLogic": {
                "isEnabled": True,
                "triggersOn": "Incidents",
                "triggersWhen": "Created",
                "conditions": [
                    {"conditionType": "Property", "conditionProperties": {
                        "propertyName": "IncidentTitle", "operator": "Contains", "propertyValues": ["Entra", "Consent"]}},
                ],
            },
            "actions": [
                {"order": 1, "actionType": "ModifyProperties", "actionConfiguration": {
                    "owner": {"objectId": responder_oid, "userPrincipalName": responder_upn},
                    "labels": [{"labelName": "identity"}]}},
            ],
        },
        "ar03-triage-tasks-high": {
            "displayName": "AR03-Add-Triage-Tasks-High",
            "order": 3,
            "triggeringLogic": {
                "isEnabled": True,
                "triggersOn": "Incidents",
                "triggersWhen": "Created",
                "conditions": [
                    {"conditionType": "Property", "conditionProperties": {
                        "propertyName": "IncidentSeverity", "operator": "Equals", "propertyValues": ["High"]}},
                ],
            },
            "actions": [
                {"order": i + 1, "actionType": "AddIncidentTask", "actionConfiguration": {"title": t, "description": d}}
                for i, (t, d) in enumerate([
                    ("Check sign-in logs", "Review SigninLogs for the account(s) for the last 7 days: IPs, apps, MFA results."),
                    ("Check device timeline", "Open each host entity's device timeline in Defender for Endpoint around the alert time."),
                    ("Scope with Go hunt", "Use Go hunt on the main entity to find related activity across all tables."),
                ])
            ],
        },
    }


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--subscription", required=True)
    p.add_argument("--resource-group", required=True)
    p.add_argument("--workspace", required=True)
    p.add_argument("--responder-upn", required=True)
    a = p.parse_args()

    ws_id = (f"/subscriptions/{a.subscription}/resourceGroups/{a.resource_group}"
             f"/providers/Microsoft.OperationalInsights/workspaces/{a.workspace}")
    oid = az("ad", "user", "show", "--id", a.responder_upn, "--query", "id", "-o", "tsv")
    base = f"https://management.azure.com{ws_id}/providers/Microsoft.SecurityInsights/automationRules"
    failures = 0
    for rid, props in rules(ws_id, oid, a.responder_upn).items():
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump({"properties": props}, tmp)
        try:
            az("rest", "--method", "put", "--url", f"{base}/{rid}?api-version={API}", "--body", f"@{tmp.name}")
            print(f"OK    {props['order']}  {props['displayName']}")
        except RuntimeError as err:
            failures += 1
            msg = next((l for l in str(err).splitlines() if "message" in l.lower()), str(err))
            print(f"FAIL  {props['order']}  {props['displayName']}: {msg[:200]}")
        finally:
            os.unlink(tmp.name)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
