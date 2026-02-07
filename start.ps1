$ErrorActionPreference = "Stop"

Write-Host "Starting Sales Analytics Platform..." -ForegroundColor Green

# 1. Run Python Backend
Write-Host "`n[1/3] Running Python Analysis..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot/sales-analytics"
try {
    python main.py
} catch {
    Write-Host "Python script failed!" -ForegroundColor Red
    exit 1
}

# 2. Copy Analytics Data
Write-Host "`n[2/3] Copying Analytics Data..." -ForegroundColor Cyan
$source = "output/analytics.json"
$dest = "../frontend/public/analytics.json"

if (Test-Path $source) {
    Copy-Item $source $dest -Force
    Write-Host "Data synced to frontend." -ForegroundColor Green
} else {
    Write-Host "Warning: analytics.json not found in output/" -ForegroundColor Yellow
}

# 3. Start Next.js Frontend
Write-Host "`n[3/3] Starting Next.js Frontend..." -ForegroundColor Cyan
Set-Location "$PSScriptRoot/frontend"
pnpm dev
