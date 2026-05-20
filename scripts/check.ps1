# Intent Kit — CI wrapper for intent check (PowerShell)
# Usage: .\scripts\check.ps1 [-Verbose] [-Fix]

param(
    [switch]$Verbose,
    [switch]$Fix
)

$ErrorActionPreference = "Stop"

$args_list = @("check")
if ($Verbose) { $args_list += "--verbose" }
if ($Fix) { $args_list += "--fix" }

if (Get-Command intent -ErrorAction SilentlyContinue) {
    & intent @args_list
} elseif (Get-Command uv -ErrorAction SilentlyContinue) {
    & uv run intent @args_list
} else {
    Write-Error "Error: neither 'intent' nor 'uv' found on PATH"
    exit 1
}

exit $LASTEXITCODE
