# Dang ky Windows Scheduled Task chay 07:00 hang ngay.
#   powershell -ExecutionPolicy Bypass -File deploy\install_task.ps1
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$bat  = Join-Path $root "deployun_daily.bat"
$name = "YouTubeTrendHunter"

$action  = New-ScheduledTaskAction -Execute $bat -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Daily -At 7:00am
# StartWhenAvailable = chay bu neu may tat dung luc 7h
# MultipleInstances IgnoreNew = khong chay chong (tang bao ve thu hai ngoai RunLock)
$set = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
        -MultipleInstances IgnoreNew -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName $name -Action $action -Trigger $trigger -Settings $set -Force | Out-Null
Write-Host "Da dang ky '$name' - chay 07:00 hang ngay."
Write-Host "Chay thu ngay: Start-ScheduledTask -TaskName $name"
Write-Host "Go bo:         Unregister-ScheduledTask -TaskName $name -Confirm:0"
