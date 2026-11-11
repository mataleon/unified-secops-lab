<#
.SYNOPSIS  Puts the lab ASR rules into Audit mode on a single lab VM (run as administrator).
.NOTES     For production use Intune or MDE security settings management instead of local PowerShell.
           Change -Mode to Enabled (Block) or Warn after reviewing audit events.
#>
param([ValidateSet('AuditMode','Enabled','Warn','Disabled')] [string]$Mode = 'AuditMode')

$rules = @(
  '9e6c4e1f-7d60-472f-ba1a-a39ef669e4b2', # LSASS credential stealing
  '56a863a9-875e-4185-98a7-b882c64b5ce5', # Vulnerable signed drivers
  'e6db77e5-3df2-4cf1-b95a-636979351e5b', # WMI event subscription persistence
  'd4f940ab-401b-4efc-aadc-ad5f3c50688a', # Office child processes
  '3b576869-a4ec-4529-8536-b80a7769e899', # Office executable content
  'be9ba2d9-53ea-4cdc-84e5-9b1eeee46550', # Executable content from email
  '5beb7efe-fd9a-4556-801d-275e5ffc04cc', # Obfuscated scripts
  'd1e49aac-8f56-4280-b9ba-993a6d77406c', # PSExec and WMI process creation
  'c1db55ab-c21a-4637-bb3f-a12568109d35'  # Advanced ransomware protection
)

foreach ($id in $rules) {
  Add-MpPreference -AttackSurfaceReductionRules_Ids $id -AttackSurfaceReductionRules_Actions $Mode
}

# Show the result
$p = Get-MpPreference
for ($i = 0; $i -lt $p.AttackSurfaceReductionRules_Ids.Count; $i++) {
  [pscustomobject]@{ RuleId = $p.AttackSurfaceReductionRules_Ids[$i]; Action = $p.AttackSurfaceReductionRules_Actions[$i] }
}
