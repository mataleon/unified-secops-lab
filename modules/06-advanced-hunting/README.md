# Module 06 — Advanced hunting

**SC-200 objectives:** Detect threats with Defender XDR (tables, KQL, advanced hunting, threat analytics, hunting graphs, Sentinel graph) · Detect threats with the Sentinel platform (hunting queries, KQL jobs, summary rules, notebooks + Sentinel MCP server)
**Time:** 3 evenings

## Lab 6.1 — Hunting query pack
Run every query in [hunting-queries/](hunting-queries/) in Advanced hunting. For each one record: hypothesis, result count, verdict (benign / suspicious), and whether it should become a detection. Save the useful ones as Sentinel **hunting queries** with MITRE tags.

## Lab 6.2 — Hunts and bookmarks
Sentinel → Hunting → **Hunts** → new hunt "Persistence via scheduled tasks". Add queries, bookmark 2 results, link the bookmark to the Module 04 incident.

## Lab 6.3 — Threat analytics
Pick one current threat analytics report. Document: the actor/technique, **Exposure & mitigations** for your devices, and run one of its hunting queries.

## Lab 6.4 — Hunting graph and blast radius
Advanced hunting → **Hunting graph** → run a built-in scenario (e.g. paths to a critical asset). Open the Module 04 incident and screenshot the **blast radius** view if available.

## Lab 6.5 — KQL jobs (data lake)
Follow [data-lake/kql-jobs.md](data-lake/kql-jobs.md): one **one-time** job that promotes 90 days of failed sign-ins, one **scheduled** job that builds a daily sign-in baseline.

## Lab 6.6 — Summary rule
Follow [data-lake/summary-rules.md](data-lake/summary-rules.md): hourly firewall summary from `CommonSecurityLog` (data lake tier) into an analytics `_CL` table, plus an analytics rule on the summary.

## Lab 6.7 — Notebook + Sentinel MCP server
1. Install VS Code + the **Microsoft Sentinel** extension; sign in.
2. Open [notebooks/signin-baseline.ipynb](notebooks/signin-baseline.ipynb) and run it on a small Spark pool.
3. Copy [.vscode/mcp.json](.vscode/mcp.json) into your VS Code workspace, start the server, and in Copilot agent mode ask: *"Find sign-in failures in the last 24 hours and summarize key findings."* Save the prompt and answer in `evidence/mcp-session.md`.

## Done when
- [ ] Hunting pack results table filled in
- [ ] Hunt with bookmarks linked to an incident
- [ ] Threat analytics summary
- [ ] Hunting graph / blast radius screenshots
- [ ] Two KQL jobs and one summary rule running (Jobs page screenshot)
- [ ] Notebook run + MCP session saved
