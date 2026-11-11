<#
.SYNOPSIS  Pulls BEC-relevant Purview audit records for one user (lab tenant).
.EXAMPLE   .\Search-BecAudit.ps1 -UserId victim.user@vcbhnlab.onmicrosoft.com -Days 7
.NOTES     Requires ExchangeOnlineManagement module and the Audit Logs (or View-Only Audit Logs) role.
#>
param(
  [Parameter(Mandatory)] [string]$UserId,
  [int]$Days = 7,
  [string]$OutFile = ".\bec-audit-$((Get-Date).ToString('yyyyMMdd')).csv"
)

Connect-ExchangeOnline -ShowBanner:$false

$operations = 'New-InboxRule','Set-InboxRule','UpdateInboxRules','Set-Mailbox','MailItemsAccessed','Send','UserLoggedIn'
$results = Search-UnifiedAuditLog -StartDate (Get-Date).AddDays(-$Days) -EndDate (Get-Date) `
  -UserIds $UserId -Operations $operations -ResultSize 5000 -SessionCommand ReturnLargeSet

$results | ForEach-Object {
  $d = $_.AuditData | ConvertFrom-Json
  [pscustomobject]@{
    CreationDate = $_.CreationDate
    Operation    = $_.Operations
    ClientIP     = $d.ClientIP
    Workload     = $d.Workload
    Parameters   = ($d.Parameters | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join '; '
  }
} | Sort-Object CreationDate | Export-Csv $OutFile -NoTypeInformation

Write-Output "Exported $($results.Count) records to $OutFile"
