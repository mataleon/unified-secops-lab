<#
.SYNOPSIS  Read-only triage collector for the live response library (lab use).
.DESCRIPTION Writes basic host triage to C:\ProgramData\VCBHN-Triage\triage.txt for retrieval with getfile.
#>
$out = 'C:\ProgramData\VCBHN-Triage'
New-Item -ItemType Directory -Path $out -Force | Out-Null
$file = Join-Path $out 'triage.txt'

"=== VCBHN live response triage $(Get-Date -Format o) on $env:COMPUTERNAME ===" | Out-File $file
"`n--- Logged-on sessions ---" | Out-File $file -Append
quser 2>$null | Out-File $file -Append
"`n--- Non-Microsoft scheduled tasks ---" | Out-File $file -Append
Get-ScheduledTask | Where-Object { $_.TaskPath -notlike '\Microsoft\*' } |
  Select-Object TaskName, TaskPath, State, @{n='Action';e={($_.Actions | ForEach-Object Execute) -join ';'}} |
  Format-Table -AutoSize | Out-String -Width 300 | Out-File $file -Append
"`n--- Run keys ---" | Out-File $file -Append
'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run','HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' |
  ForEach-Object { Get-ItemProperty $_ -ErrorAction SilentlyContinue } | Out-String | Out-File $file -Append
"`n--- Established TCP connections ---" | Out-File $file -Append
Get-NetTCPConnection -State Established |
  Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess,
    @{n='Process';e={(Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue).ProcessName}} |
  Format-Table -AutoSize | Out-String -Width 300 | Out-File $file -Append
"`n--- Recent files in TEMP ---" | Out-File $file -Append
Get-ChildItem $env:TEMP -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending |
  Select-Object -First 20 FullName, Length, LastWriteTime | Format-Table -AutoSize | Out-String -Width 300 | Out-File $file -Append

Write-Output "Triage written to $file"
