# Automated Setup Script for Binance Futures Testnet Bot
Write-Host "Setting up Binance Futures Testnet Bot..." -ForegroundColor Green

# Check Python availability
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version 2>$null
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install from python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Cyan
} else {
    py -m venv .venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Set execution policy temporarily
Write-Host "Setting execution policy..." -ForegroundColor Yellow
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
try {
    .\.venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip and install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
py -m pip install --upgrade pip --quiet
py -m pip install -r .\requirements.txt --quiet
Write-Host "Dependencies installed" -ForegroundColor Green

# Syntax check
Write-Host "Running syntax validation..." -ForegroundColor Yellow
try {
    py -m py_compile .\src\market_orders.py .\run_test_order.py
    Write-Host "Syntax validation passed" -ForegroundColor Green
} catch {
    Write-Host "Syntax validation failed" -ForegroundColor Red
    exit 1
}

# Setup .env file
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file found" -ForegroundColor Green
} else {
    Write-Host ".env file not found" -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Write-Host "Copying .env.example to .env..." -ForegroundColor Cyan
        Copy-Item ".env.example" ".env"
        Write-Host ".env file created from template" -ForegroundColor Green
    } else {
        Write-Host ".env.example not found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your Testnet API keys from testnet.binancefuture.com" -ForegroundColor White
Write-Host "2. Test the bot: py .\run_test_order.py BTCUSDT BUY 0.001" -ForegroundColor White