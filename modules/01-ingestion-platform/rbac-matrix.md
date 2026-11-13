# RBAC test matrix

**Setup (done 2026-11-13):** three test users, each granted one Microsoft Sentinel role on `rg-secops-lab`. Microsoft recommends assigning Sentinel roles at the resource group level. Because the tenant has Entra ID P2, the Azure role wizard created the assignments as **PIM-eligible (time-bound)** rather than active. Each user has to **activate** the role in Privileged Identity Management before it works.

| Test user | Role | Assignment |
|---|---|---|
| `soc.reader` | Microsoft Sentinel Reader | PIM eligible |
| `soc.responder` | Microsoft Sentinel Responder | PIM eligible |
| `soc.engineer` | Microsoft Sentinel Contributor | PIM eligible |

## Expected permissions (Microsoft docs) vs. tested

✓ = allowed, ✗ = blocked. "Expected" comes from [Roles and permissions in the Microsoft Sentinel platform](https://learn.microsoft.com/azure/sentinel/roles). Fill in "Tested" after signing in as each user and activating the role.

| Action | Sentinel Reader | Sentinel Responder | Sentinel Contributor | + Playbook Operator |
|---|---|---|---|---|
| View incidents | ✓ | ✓ | ✓ | ✗ |
| Assign / close incident | ✗ | ✓ | ✓ | ✗ |
| Create / edit analytics rule | ✗ | ✗ | ✓ | ✗ |
| Create workbook | ✗ * | ✗ * | ✓ * | ✗ |
| Install Content hub solutions | ✗ | ✗ | ✓ | ✗ |
| Run playbook on incident | ✗ | ✗ | ✗ | ✓ |
| Edit playbook | ✗ | ✗ | ✗ | ✗ (needs Logic App Contributor) |

\* Creating or deleting workbooks also needs the **Workbook Contributor** role.

### Tested results

| Action | soc.reader | soc.responder | soc.engineer |
|---|---|---|---|
| Close incident | | | |
| Edit analytics rule | | | |
| Run playbook | | | |

## Findings

- **No role can run playbooks, not even Contributor.** That needs **Microsoft Sentinel Playbook Operator** (run) or **Logic App Contributor** (run and edit). Sentinel itself also needs **Microsoft Sentinel Automation Contributor** on the playbook's resource group before automation rules can call a playbook.
- **The P2 tenant defaulted to PIM-eligible assignments.** A role check with `az role assignment list` shows nothing until the user activates the role. Least privilege now also covers *time*, not just scope.
- **Role assignments are cumulative.** A Reader who is also a Contributor gets Contributor rights, so audit for stacked roles.

**Takeaway:** a SOC analyst needs **Responder** to work incidents and **Playbook Operator** to run response actions. **Contributor** is for detection engineers who change rules and content. All three should be PIM-eligible, not permanent.
