# Keep the wardrobe app and its tunnel up.
#
# Run by the "Wardrobe keep-alive" scheduled task at logon and every 5 minutes.
#
# WHY A WATCHDOG AND NOT TASK SCHEDULER'S OWN RESTART. The task was first set up
# with -RestartCount 999, which sounds like exactly this and is not: that fires
# when the TASK fails, and a process killed out from under it does not count as
# a failure. Tested by killing the app — it stayed dead for 75 seconds and the
# task reported 4294967295. This checks the thing that actually matters, which
# is whether the port is answering.
#
# Idempotent by design: if both are already up it does nothing and exits, so
# running it every five minutes is free.

$ErrorActionPreference = 'Stop'
$proj = Split-Path -Parent $PSScriptRoot

function Test-AppUp {
    $null -ne (Get-NetTCPConnection -LocalPort 5005 -State Listen -ErrorAction SilentlyContinue)
}

# --- the Flask app -------------------------------------------------------
if (Test-AppUp) {
    Write-Output "app: already listening on 5005"
} else {
    # pythonw so it runs without a console window; python.exe is the fallback
    # for a venv that has no pythonw.
    $py = Join-Path $proj '.venv\Scripts\pythonw.exe'
    if (-not (Test-Path $py)) { $py = Join-Path $proj '.venv\Scripts\python.exe' }
    Start-Process -FilePath $py -ArgumentList 'run.py' -WorkingDirectory $proj -WindowStyle Hidden
    Write-Output "app: started"
}

# --- the cloudflared tunnel ---------------------------------------------
# Checked by process rather than by port: the tunnel makes an OUTBOUND
# connection to Cloudflare and listens on nothing locally, so there is no port
# to probe.
if (Get-Process cloudflared -ErrorAction SilentlyContinue) {
    Write-Output "tunnel: already running"
} else {
    $cf = 'C:\Program Files (x86)\cloudflared\cloudflared.exe'
    if (Test-Path $cf) {
        Start-Process -FilePath $cf -ArgumentList 'tunnel','run','wardrobe' -WindowStyle Hidden
        Write-Output "tunnel: started"
    } else {
        Write-Output "tunnel: cloudflared not found at $cf"
    }
}
