# Build the plugin on Windows: base + optional company layer -> dist\<name>[-<company>].plugin
# Usage (PowerShell 5.1 or 7):  powershell -ExecutionPolicy Bypass -File scripts\build.ps1 [company-slug]
param([string]$Company = "")
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem

$Root  = Split-Path -Parent $PSScriptRoot
$Out   = Join-Path $Root "dist"
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Build = Join-Path ([System.IO.Path]::GetTempPath()) ("tao-build-" + [guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $Build | Out-Null

try {
  # Base: everything except dev-only folders/files
  $skip = @(".git", "companies", "scripts", "tests", ".tmp", ".kouen-worktrees", ".claude", "dist", "CLAUDE.md", ".gitignore", ".gitattributes", ".DS_Store")
  Get-ChildItem -Force -Path $Root | Where-Object { $skip -notcontains $_.Name } |
    ForEach-Object { Copy-Item -Recurse -Force -Path $_.FullName -Destination $Build }

  $Name = "thai-accounting-office"
  if ($Company -ne "") {
    $Src = Join-Path (Join-Path $Root "companies") $Company
    if (-not (Test-Path $Src)) { throw "no such company layer: $Src" }
    if (Select-String -Path (Join-Path $Src "*") -Pattern "<COMPANY_NAME>" -SimpleMatch -Quiet -ErrorAction SilentlyContinue) {
      Write-Warning "$Company still has <COMPANY_NAME> placeholders"
    }
    $Profile = Join-Path $Build "skills\company-profile"
    New-Item -ItemType Directory -Force -Path $Profile | Out-Null
    Copy-Item -Recurse -Force (Join-Path $Src "company-profile\*") $Profile
    $Over = Join-Path $Src "overrides"
    if (Test-Path $Over) {
      Get-ChildItem -Force -Path $Over | ForEach-Object { Copy-Item -Recurse -Force -Path $_.FullName -Destination $Build }
    }
    # plugin.json: prefix the description with the company (UTF-8 without BOM, Thai-safe)
    $Manifest = Join-Path $Build ".claude-plugin\plugin.json"
    $json = [System.IO.File]::ReadAllText($Manifest, [System.Text.Encoding]::UTF8) | ConvertFrom-Json
    $json.description = "[$Company] " + $json.description
    [System.IO.File]::WriteAllText($Manifest, ($json | ConvertTo-Json -Depth 10), (New-Object System.Text.UTF8Encoding($false)))
    $Name = "$Name-$Company"
  }

  Get-ChildItem -Recurse -Force -Path $Build -Include ".DS_Store",".gitkeep" | Remove-Item -Force
  $Zip = Join-Path $Out "$Name.zip"; $File = Join-Path $Out "$Name.plugin"
  Remove-Item -Force -ErrorAction SilentlyContinue $Zip, $File
  # ZipFile (not Compress-Archive): entry names use '/' so the package opens on every OS
  [System.IO.Compression.ZipFile]::CreateFromDirectory($Build, $Zip)
  Move-Item -Force $Zip $File
  Write-Host "built $File"
} finally {
  Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $Build
}
