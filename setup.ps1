# Quick Start Script for Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SE Architecture & Pricing Assistant" -ForegroundColor Cyan
Write-Host "Quick Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "1. Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(1[0-9]|[2-9][0-9])") {
    Write-Host "   ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ✗ Python 3.10+ required. Found: $pythonVersion" -ForegroundColor Red
    Write-Host "   Please install Python 3.10 or higher from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check Azure CLI
Write-Host "`n2. Checking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az version 2>&1 | ConvertFrom-Json
    Write-Host "   ✓ Azure CLI installed" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Azure CLI not found" -ForegroundColor Red
    Write-Host "   Please install from: https://learn.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Yellow
    exit 1
}

# Check Azure login
Write-Host "`n3. Checking Azure login..." -ForegroundColor Yellow
try {
    $account = az account show 2>&1 | ConvertFrom-Json
    Write-Host "   ✓ Logged in as: $($account.user.name)" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Not logged in to Azure" -ForegroundColor Red
    Write-Host "   Running 'az login'..." -ForegroundColor Yellow
    az login
}

# Create virtual environment
Write-Host "`n4. Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "   ℹ Virtual environment already exists" -ForegroundColor Blue
} else {
    python -m venv .venv
    Write-Host "   ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n5. Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "   ✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host "`n6. Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   ✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host "`n7. Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
Write-Host "   ℹ Note: --pre flag is REQUIRED for Agent Framework preview" -ForegroundColor Blue
pip install --pre -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "   ✗ Error installing dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
Write-Host "`n8. Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "   ℹ Creating .env from template..." -ForegroundColor Blue
    Copy-Item ".env.example" ".env"
    Write-Host "   ⚠ Please edit .env with your Azure AI Foundry settings!" -ForegroundColor Yellow
    Write-Host "`n   Required settings:" -ForegroundColor Yellow
    Write-Host "   - FOUNDRY_ENDPOINT=https://your-project.cognitiveservices.azure.com/" -ForegroundColor Gray
    Write-Host "   - MODEL_DEPLOYMENT_NAME=gpt-4.1" -ForegroundColor Gray
    Write-Host "   - AZURE_SUBSCRIPTION_ID=your-subscription-id`n" -ForegroundColor Gray
    
    $edit = Read-Host "   Open .env for editing now? (y/n)"
    if ($edit -eq "y") {
        notepad .env
    }
}

# Final instructions
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure .env is configured with your Azure AI Foundry settings" -ForegroundColor White
Write-Host "2. Run the demo:" -ForegroundColor White
Write-Host "   python main.py`n" -ForegroundColor Cyan

Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "- README.md" -ForegroundColor White
Write-Host "- DEMO_GUIDE.md`n" -ForegroundColor White

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
