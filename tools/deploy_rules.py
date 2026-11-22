#!/usr/bin/env python3
"""Deploy the YAML analytics rules in modules/02-detections-automation/rules to Microsoft Sentinel.

Detection-as-code: the YAML files are the source of truth. Each rule's `id` is used as the
Sentinel rule ID, so re-running the script updates rules in place instead of duplicating them.

Usage (Azure Cloud Shell or any shell signed in with `az login`):
    python3 tools/deploy_rules.py --subscription <id> --resource-group rg-secops-lab \
        --workspace law-secops-lab [--only name1,name2] [--dry-run]
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

API = "2024-03-01"
# NRT rules are rejected by the GA API versions ("Unsupported api-version ... for kind: NRT"),
# so they go through the preview API.
API_BY_KIND = {"NRT": "2024-10-01-preview"}
DURATIONS = {"m": "M", "h": "H"}


def iso_duration(value):
    """Convert '15m' / '1h' / '14d' into ISO 8601 ('PT15M' / 'PT1H' / 'P14D')."""
    number, unit = value[:-1], value[-1]
    if unit == "d":
        return f"P{number}D"
    return f"PT{number}{DURATIONS[unit]}"


def to_api_body(rule):
    techniques = rule.get("relevantTechniques", [])
    props = {
        "displayName": rule["name"],
        "description": rule["description"],
        "severity": rule["severity"],
        "enabled": True,
        "query": rule["query"],
        "suppressionDuration": "PT5H",
        "suppressionEnabled": False,
        "tactics": rule["tactics"],
        "techniques": sorted({t.split(".")[0] for t in techniques}),
        "subTechniques": [t for t in techniques if "." in t],
        "entityMappings": [
            {"entityType": e["entityType"], "fieldMappings": e["fieldMappings"]}
            for e in rule.get("entityMappings", [])
        ],
        "incidentConfiguration": {
            "createIncident": True,
            "groupingConfiguration": {
                "enabled": False,
                "reopenClosedIncident": False,
                "lookbackDuration": "PT5H",
                "matchingMethod": "AllEntities",
            },
        },
    }
    if rule.get("customDetails"):
        props["customDetails"] = rule["customDetails"]
    if rule["kind"] == "Scheduled":
        props.update(
            {
                "queryFrequency": iso_duration(rule["queryFrequency"]),
                "queryPeriod": iso_duration(rule["queryPeriod"]),
                "triggerOperator": "GreaterThan",
                "triggerThreshold": rule.get("triggerThreshold", 0),
                "eventGroupingSettings": rule.get(
                    "eventGroupingSettings", {"aggregationKind": "SingleAlert"}
                ),
            }
        )
    return {"kind": rule["kind"], "properties": props}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--subscription", required=True)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--only", help="Comma-separated rule file names (without .yaml)")
    parser.add_argument("--dry-run", action="store_true", help="Print the API bodies, deploy nothing")
    args = parser.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(root, "modules/02-detections-automation/rules/*.yaml")))
    if args.only:
        wanted = set(args.only.split(","))
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in wanted]

    base = (
        f"https://management.azure.com/subscriptions/{args.subscription}/resourceGroups/{args.resource_group}"
        f"/providers/Microsoft.OperationalInsights/workspaces/{args.workspace}"
        f"/providers/Microsoft.SecurityInsights/alertRules"
    )
    failures = 0
    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path) as fh:
            rule = yaml.safe_load(fh)
        body = to_api_body(rule)
        if args.dry_run:
            print(json.dumps({name: body}, indent=2))
            continue
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
            json.dump(body, tmp)
        result = subprocess.run(
            ["az", "rest", "--method", "put", "--url", f"{base}/{rule['id']}?api-version={API_BY_KIND.get(rule['kind'], API)}",
             "--body", f"@{tmp.name}", "--query", "properties.displayName", "-o", "tsv"],
            capture_output=True, text=True,
        )
        os.unlink(tmp.name)
        if result.returncode == 0:
            print(f"OK    {rule['kind']:<9} {name}")
        else:
            failures += 1
            reason = next((l for l in result.stderr.splitlines() if "Message" in l or "ERROR" in l), result.stderr.strip())
            print(f"FAIL  {rule['kind']:<9} {name}: {reason[:160]}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
