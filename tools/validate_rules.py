"""Validate Sentinel analytics rule YAML files (detection-as-code check).

Checks: required fields per rule kind, GUID ids (unique), MITRE tactic names and technique IDs,
entity mapping limits, and that every rule has a non-empty query.
Usage: python tools/validate_rules.py [rules_dir ...]
"""
import re
import sys
import uuid
from pathlib import Path

import yaml

TACTICS = {
    "Reconnaissance", "ResourceDevelopment", "InitialAccess", "Execution", "Persistence",
    "PrivilegeEscalation", "DefenseEvasion", "CredentialAccess", "Discovery", "LateralMovement",
    "Collection", "CommandAndControl", "Exfiltration", "Impact",
}
COMMON = {"id", "name", "description", "severity", "tactics", "relevantTechniques", "query", "version", "kind"}
SCHEDULED = COMMON | {"queryFrequency", "queryPeriod", "triggerOperator", "triggerThreshold"}
SEVERITIES = {"Informational", "Low", "Medium", "High"}
TECHNIQUE = re.compile(r"^T\d{4}(\.\d{3})?$")


def check(path: Path, seen_ids: set) -> list[str]:
    errors = []
    try:
        rule = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        return [f"invalid YAML: {exc}"]
    if not isinstance(rule, dict):
        return ["file is not a YAML mapping"]

    kind = rule.get("kind")
    if kind not in {"Scheduled", "NRT"}:
        errors.append(f"kind must be Scheduled or NRT, got {kind!r}")
    required = SCHEDULED if kind == "Scheduled" else COMMON
    for field in sorted(required - rule.keys()):
        errors.append(f"missing field: {field}")
    if kind == "NRT":
        for field in ("queryFrequency", "queryPeriod"):
            if field in rule:
                errors.append(f"NRT rules must not set {field}")

    try:
        rid = str(uuid.UUID(str(rule.get("id"))))
        if rid in seen_ids:
            errors.append(f"duplicate id {rid}")
        seen_ids.add(rid)
    except ValueError:
        errors.append("id is not a GUID")

    if rule.get("severity") not in SEVERITIES:
        errors.append(f"severity must be one of {sorted(SEVERITIES)}")
    for tactic in rule.get("tactics") or []:
        if tactic not in TACTICS:
            errors.append(f"unknown tactic: {tactic}")
    for tech in rule.get("relevantTechniques") or []:
        if not TECHNIQUE.match(str(tech)):
            errors.append(f"bad technique id: {tech}")
    if not str(rule.get("query", "")).strip():
        errors.append("query is empty")
    mappings = rule.get("entityMappings") or []
    if len(mappings) > 10:
        errors.append("more than 10 entity mappings")
    for m in mappings:
        if len(m.get("fieldMappings", [])) > 3:
            errors.append(f"entity {m.get('entityType')} has more than 3 identifiers")
    if len(rule.get("customDetails") or {}) > 20:
        errors.append("more than 20 custom details")
    return errors


def main(dirs: list[str]) -> int:
    seen: set = set()
    files = [p for d in dirs for p in sorted(Path(d).rglob("*.yaml"))]
    failed = 0
    for path in files:
        errs = check(path, seen)
        status = "FAIL" if errs else "ok  "
        print(f"{status} {path}")
        for e in errs:
            print(f"     - {e}")
        failed += bool(errs)
    print(f"\n{len(files)} rules checked, {failed} failed")
    return 1 if failed or not files else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["modules"]))
