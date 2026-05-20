# Intent Kit — CI wrapper for intent init (PowerShell)
# Usage: .\scripts\init.ps1 <project-name> [-Ai agent] [-Force]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$ProjectName,
    [string]$Ai = "claude",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$args_list = @("init", $ProjectName, "--ai", $Ai)
if ($Force) { $args_list += "--force" }

if (Get-Command intent -ErrorAction SilentlyContinue) {
    & intent @args_list
} elseif (Get-Command uv -ErrorAction SilentlyContinue) {
    & uv run intent @args_list
} else {
    Write-Error "Error: neither 'intent' nor 'uv' found on PATH"
    exit 1
}

exit $LASTEXITCODE
