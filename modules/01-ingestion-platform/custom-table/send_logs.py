"""Send synthetic VCBHN patient-portal events to a DCR-based custom table (VCBHNApp_CL).

Requires:  pip install azure-identity azure-monitor-ingestion
Env vars:  DCE_ENDPOINT   e.g. https://dce-vcbhn-xxxx.westus2-1.ingest.monitor.azure.com
           DCR_IMMUTABLE_ID  e.g. dcr-0123456789abcdef0123456789abcdef
           STREAM_NAME    e.g. Custom-VCBHNApp_CL
           AZURE_TENANT_ID / AZURE_CLIENT_ID / AZURE_CLIENT_SECRET (app with Monitoring Metrics Publisher on the DCR)
All data is synthetic lab data.
"""
import os
import random
from datetime import datetime, timedelta, timezone

from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient

ACTIONS = ["Login", "ViewRecord", "RecordExport", "PasswordChange"]
USERS = ["victim.user", "nurse.lab", "billing.lab", "attacker.sim"]


def make_events(n: int = 25) -> list[dict]:
    now = datetime.now(timezone.utc)
    events = []
    for _ in range(n):
        action = random.choice(ACTIONS)
        events.append({
            "EventTime": (now - timedelta(minutes=random.randint(0, 60))).isoformat(),
            "AppName": "VCBHN-PatientPortal",
            "UserPrincipalName": f"{random.choice(USERS)}@vcbhnlab.onmicrosoft.com",
            "Action": action,
            "RecordCount": random.randint(200, 2000) if action == "RecordExport" else 1,
            "SourceIP": f"198.51.100.{random.randint(1, 254)}",
            "Result": random.choice(["Success", "Success", "Failure"]),
        })
    return events


def main() -> None:
    client = LogsIngestionClient(endpoint=os.environ["DCE_ENDPOINT"], credential=DefaultAzureCredential())
    events = make_events()
    client.upload(rule_id=os.environ["DCR_IMMUTABLE_ID"], stream_name=os.environ["STREAM_NAME"], logs=events)
    print(f"Uploaded {len(events)} events")


if __name__ == "__main__":
    main()
