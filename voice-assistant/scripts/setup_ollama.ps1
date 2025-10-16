# Ollama Setup Script for Windows
# Run this in PowerShell as Administrator

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Ollama WSL Configuration" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Configure Ollama to listen on all interfaces
Write-Host "Configuring Ollama for network access..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'User')
Write-Host "✓ OLLAMA_HOST set to 0.0.0.0:11434" -ForegroundColor Green
Write-Host ""

# Add firewall rule
Write-Host "Adding Windows Firewall rule..." -ForegroundColor Yellow
try {
    $existingRule = Get-NetFirewallRule -DisplayName "Ollama WSL" -ErrorAction SilentlyContinue
    if ($existingRule) {
        Write-Host "✓ Firewall rule already exists" -ForegroundColor Green
    } else {
        New-NetFirewallRule -DisplayName "Ollama WSL" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434 | Out-Null
        Write-Host "✓ Firewall rule created" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Failed to create firewall rule: $_" -ForegroundColor Red
    Write-Host "  Please run this script as Administrator" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Stop Ollama if running
Write-Host "Restarting Ollama..." -ForegroundColor Yellow
Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Write-Host "✓ Ollama stopped" -ForegroundColor Green
Write-Host ""

Write-Host "Please start Ollama from the Start Menu" -ForegroundColor Yellow
Write-Host ""

# Pull required models
Write-Host "Pulling required models..." -ForegroundColor Yellow
Write-Host "This will download ~10GB of models" -ForegroundColor Cyan
Write-Host ""

$models = @("llama3.2:1b", "llama3.2:3b", "qwen2.5:7b")

foreach ($model in $models) {
    Write-Host "Pulling $model..." -ForegroundColor Yellow
    & ollama pull $model
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $model downloaded" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to download $model" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ Ollama Configuration Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Test from WSL
Write-Host "Test the connection from WSL with:" -ForegroundColor Yellow
Write-Host "  curl http://172.22.32.1:11434/api/tags" -ForegroundColor Cyan
Write-Host ""
