<#
  Starts the two processes the phone demo needs, in their own windows:
    1. the app, under waitress (see wardrobe/app.py main())
    2. the Cloudflare tunnel that publishes it at wardrobe.maxboucoiran.com

  Close either window to take the demo down. The laptop has to stay awake:
  both processes run here, and the public URL is only a pipe to this machine.
#>

$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repo ".venv\Scripts\python.exe"
$cloudflared = "C:\Program Files (x86)\cloudflared\cloudflared.exe"

if (-not (Test-Path $python))      { throw "No venv at $python" }
if (-not (Test-Path $cloudflared)) { throw "cloudflared not found at $cloudflared" }

Start-Process -FilePath $python -ArgumentList (Join-Path $repo "run.py") -WorkingDirectory $repo
Start-Process -FilePath $cloudflared -ArgumentList "tunnel","run","wardrobe"

Write-Output ""
Write-Output "  Starting. Give it about ten seconds, then open:"
Write-Output ""
Write-Output "      https://wardrobe.maxboucoiran.com"
Write-Output ""
Write-Output "  Two windows opened - the app and the tunnel. Close them to stop."
Write-Output ""
