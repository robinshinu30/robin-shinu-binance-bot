# Robin Shinu Binance Futures Trading Bot# Robin Shinu Binance Futures Trading Bot



A Python trading bot for Binance USDT-M Futures Testnet with automated setup, comprehensive safety features, and support for both market and limit orders.A Python trading bot for Binance USDT-M Futures Testnet with automated setup, comprehensive safety features, and support for both market and limit orders.



## 🚀 Quick Start## Project Structure

```

### 1. Setup (Automated)Robin_Shinu_binance_bot/

```bash├── src/

git clone https://github.com/yourusername/robin-shinu-binance-bot.git│   ├── market_orders.py    # Main trading module

cd robin-shinu-binance-bot│   └── __init__.py         # Package marker

.\setup.ps1├── setup.ps1               # Automated setup script

```├── run_test_order.py       # Test runner script

├── requirements.txt        # Python dependencies

### 2. Get API Keys├── README.md              # This file

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com/)├── report.pdf             # Trading report (placeholder)

2. Create account and generate API keys├── bot.log               # Runtime logs

3. Copy `.env.example` to `.env`└── .env.example          # Environment template

4. Add your keys to `.env`:```

```

BINANCE_API_KEY=your_testnet_api_key_here## Features

BINANCE_API_SECRET=your_testnet_api_secret_here- **Market Orders**: Place USDT-M Futures orders on Binance Testnet

```- **Safety First**: Test mode by default, comprehensive validation

- **Easy Setup**: Automated PowerShell setup script

### 3. Test the Bot- **Configuration**: .env file support for API credentials

```bash- **Error Handling**: Custom exceptions with helpful messages

# Market order (default)- **Logging**: Detailed logs saved to bot.log

py run_test_order.py BTCUSDT BUY 0.001

## Setup Instructions

# Limit order

py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000**Quick Setup (Recommended)**

``````bash

git clone https://github.com/yourusername/robin-shinu-binance-bot.git

## 📁 Project Structurecd robin-shinu-binance-bot

```.\setup.ps1

Robin_Shinu_binance_bot/```

├── src/

│   ├── market_orders.py    # Market order functionality**Manual Setup (Alternative)**

│   ├── limit_orders.py     # Limit order functionality  

│   └── __init__.py         # Package marker### 1) Verify Python Installation

├── setup.ps1               # Automated setup script

├── run_test_order.py       # Main CLI interfaceYour system has Python available via the `py` launcher:

├── requirements.txt        # Python dependencies```powershell

├── README.md              # This filepy --version  # Should show Python 3.x.x

├── report.pdf             # Project report```

├── bot.log               # Trading logs

└── .env.example          # Environment templateIf you get an error, install Python from https://www.python.org/downloads/windows/ with "Add Python to PATH" enabled.

```

### 2) Create Virtual Environment and Install Dependencies

## 🎯 Features

```powershell

### ✅ **Order Types**# Create virtual environment

- **Market Orders**: Execute immediately at current market pricepy -m venv .venv

- **Limit Orders**: Execute when price reaches your specified level

# Allow script execution (temporary, safe)

### ✅ **Safety Features**Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

- **Test Mode Default**: All orders validated but not executed unless explicitly requested

- **Testnet Only**: Configured for safe testing environment# Activate virtual environment

- **Multiple Confirmations**: Safety prompts before live order execution.\.venv\Scripts\Activate.ps1

- **Parameter Validation**: Comprehensive input checking

# Upgrade pip and install dependencies

### ✅ **Technical Features**py -m pip install --upgrade pip

- **Automated Setup**: One-command environment configurationpy -m pip install -r .\requirements.txt

- **Error Handling**: Custom exceptions with helpful error messages```

- **Comprehensive Logging**: All activity logged to `bot.log`

- **Environment Management**: Virtual environment with dependency isolation**Note:** Use `py -m pip` instead of just `pip` to avoid PATH issues.



## 📖 How to Use### 3) Get Testnet API Keys



### Market Orders1. Visit https://testnet.binancefuture.com/

```bash2. Create an account and generate API keys

# Test market order (safe - no execution)3. **Important:** Never use mainnet API keys for testing!

py run_test_order.py BTCUSDT BUY 0.001

### 4) .env Configuration

# Live market order (requires confirmation)

py run_test_order.py BTCUSDT BUY 0.001 --liveCopy the example file and add your Testnet API keys:

```powershell

# Verbose output# Copy template file

py run_test_order.py BTCUSDT BUY 0.001 --verboseCopy-Item .env.example .env

```

# Edit .env file with your actual Testnet API keys

### Limit Ordersnotepad .env

```bash```

# Test limit order (safe - no execution)

py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000Add your credentials to `.env`:

```bash

# Live limit order (requires confirmation)BINANCE_API_KEY=your_testnet_api_key

py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000 --liveBINANCE_API_SECRET=your_testnet_api_secret

```

# Sell limit order

py run_test_order.py ETHUSDT SELL 0.01 --type limit --price 3500**Important**: Get Testnet keys from https://testnet.binancefuture.com/ (never use mainnet keys!)

```

## Usage

### Direct Module Usage

```bash**Test Order (Safe - Validation Only)**

# Market orders module```powershell

py -m src.market_orders BTCUSDT BUY 0.001 --testpy run_test_order.py BTCUSDT BUY 0.001

```

# Limit orders module

py -m src.limit_orders BTCUSDT BUY 0.001 65000 --test**Test Order with Dry Run Flag**

``````powershell

py run_test_order.py BTCUSDT BUY 0.001 --test

### Command Options```

| Option | Description | Example |

|--------|-------------|---------|**Limit Order (NEW!)**

| `symbol` | Trading pair | `BTCUSDT`, `ETHUSDT` |```powershell

| `side` | Order direction | `BUY`, `SELL` |py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000

| `quantity` | Order size | `0.001`, `10.5` |```

| `--type` | Order type | `market` (default), `limit` |

| `--price` | Limit price | `60000`, `3500.50` |**Live Order (Requires Confirmation)**

| `--live` | Execute real order | Requires confirmation |```powershell

| `--verbose` | Detailed output | Shows full response |py run_test_order.py BTCUSDT BUY 0.001 --live

```

## ⚙️ Manual Setup (Alternative)

## Logs

### 1. Install Python

Download from [python.org](https://www.python.org/downloads/windows/) and ensure "Add Python to PATH" is checked.All actions and errors are recorded in `bot.log`. The log includes:

- Order attempts and validations

### 2. Create Virtual Environment- API responses and errors  

```bash- Configuration checks

py -m venv .venv- Timestamped entries with detailed context

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

.\.venv\Scripts\Activate.ps1## Safety

```

By default, test mode is enabled. Live trading requires explicit confirmation and multiple safety prompts. The bot includes:

### 3. Install Dependencies

```bash- **Test Mode Default**: All orders are validated but not executed unless explicitly requested

py -m pip install --upgrade pip- **Testnet Only**: Configured for Binance Futures Testnet (never mainnet)

py -m pip install -r requirements.txt- **Configuration Validation**: Checks API keys and prevents placeholder values

```- **Error Handling**: Comprehensive exception handling with helpful error messages

- **Confirmation Prompts**: Multiple warnings before any live order execution

### 4. Configure Environment

```bash## Technical Features

Copy-Item .env.example .env

notepad .env  # Add your API keys- **Automated Setup**: One-command environment configuration

```- **Environment Management**: Virtual environment with dependency isolation

- **Error Handling**: Custom exceptions with detailed error messages

## 🔍 Understanding the Output- **Logging**: Comprehensive activity logging to `bot.log`

- **Configuration**: .env file support with template and validation

### Test Mode (Default)- **Safety Validations**: Multiple layers of safety checks and confirmations

```

🔧 Configuration Check:## Next Features 🚀

   ✅ .env file found

   ✅ BINANCE_API_KEY: Set### ✅ **Limit Orders (IMPLEMENTED!)**

   ✅ BINANCE_API_SECRET: Set

The bot now supports both market and limit orders:

🚀 Testing market order:

   Symbol: BTCUSDT**Market Orders (Default)**:

   Side: BUY```bash

   Quantity: 0.001py run_test_order.py BTCUSDT BUY 0.001

   Mode: TEST (validation only)```



✅ Success!**Limit Orders (NEW!)**:

   Order parameters validated successfully```bash

```py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000

```

### Live Mode (--live flag)

```**Key Features**:

⚠️  WARNING: --live flag detected!- Full validation for limit order parameters (price, quantity, symbol)

   This will place a REAL order on the Testnet!- Comprehensive error handling specific to limit orders

   Type 'yes' to continue: yes- Test mode by default with safety confirmations for live orders

- Detailed logging with price information

🚀 Placing market order:- CLI support via both `run_test_order.py` and `py -m src.limit_orders`

   Symbol: BTCUSDT

   Side: BUY**Direct Module Usage**:

   Quantity: 0.001```bash

   Mode: LIVE (real order)# Test limit order validation

py -m src.limit_orders ETHUSDT SELL 0.01 3500 --test

✅ Success!

   Order ID: 123456789# Live limit order (with confirmations)

```py -m src.limit_orders BTCUSDT BUY 0.001 65000 --live

```

## 📊 Logs and Monitoring

### 🔮 **Future Enhancements**

All bot activity is automatically logged to `bot.log`:

```- **Stop-Loss Orders**: Automatic position protection

2025-10-23 12:15:38 - INFO - Configured client for Binance Futures Testnet- **Take-Profit Orders**: Automatic profit taking

2025-10-23 12:15:38 - INFO - 🧪 Testing market order: BTCUSDT BUY 0.001- **Order Management**: Cancel, modify, and track existing orders

2025-10-23 12:15:41 - INFO - ✅ Test order validation successful- **Position Monitoring**: Real-time position tracking and P&L

```- **Risk Management**: Position sizing and leverage controls

- **Strategy Framework**: Support for automated trading strategies

View recent logs:
```bash
Get-Content bot.log -Tail 10
```

## ⚠️ Important Safety Notes

### 🔐 **API Keys**
- **Never use mainnet API keys** - Only Testnet keys from [testnet.binancefuture.com](https://testnet.binancefuture.com/)
- **Keep .env file secure** - Never commit real API keys to version control
- **Use the provided .env.example** as template

### 🛡️ **Trading Safety**
- **Test mode is default** - Orders are validated but not executed
- **Use small quantities** - Start with minimal amounts for testing
- **Understand leverage** - Futures contracts use leverage which amplifies risk
- **Monitor positions** - Always track your open positions

### 🧪 **Testing Environment**
- **Testnet only** - This bot is configured for Testnet environment
- **No real money** - Testnet uses fake funds for safe testing
- **Live orders require confirmation** - Multiple safety prompts prevent accidents

## 🚨 Troubleshooting

### Common Issues

**"pip is not recognized"**
```bash
# Use py launcher instead
py -m pip install -r requirements.txt
```

**"API key not found"**
```bash
# Check .env file exists and has correct format
Get-Content .env
# Should show your API keys (not placeholders)
```

**"Order validation failed"**
- Check symbol format (must be USDT pairs like BTCUSDT)
- Verify quantity is positive
- For limit orders, ensure price is positive
- Check Testnet API keys are valid

**"Execution policy error"**
```bash
# Allow script execution temporarily
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### Getting Help
1. Check `bot.log` for detailed error messages
2. Run with `--verbose` flag for more information
3. Verify Testnet API keys are working on [testnet.binancefuture.com](https://testnet.binancefuture.com/)

## 📈 Examples

### Basic Market Order
```bash
# Safe test of buying 0.001 BTC
py run_test_order.py BTCUSDT BUY 0.001
```

### Limit Order Strategy
```bash
# Place buy order below current price
py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 50000

# Place sell order above current price  
py run_test_order.py BTCUSDT SELL 0.001 --type limit --price 70000
```

### Different Assets
```bash
# Ethereum limit order
py run_test_order.py ETHUSDT BUY 0.01 --type limit --price 3000

# Cardano market order
py run_test_order.py ADAUSDT SELL 100
```

## 🔄 Workflow

1. **Setup**: Run `setup.ps1` for automated configuration
2. **Configure**: Add Testnet API keys to `.env` file  
3. **Test**: Run orders in test mode (default)
4. **Monitor**: Check `bot.log` for all activity
5. **Execute**: Use `--live` flag when ready for real orders

## 📋 Requirements

- **Python 3.8+** (tested with Python 3.14)
- **Windows PowerShell** (for setup script)
- **Binance Futures Testnet Account** 
- **Internet Connection** for API access

## 🏁 Ready to Trade!

Your bot is now configured and ready for safe Testnet trading. Remember:
- ✅ Always test first with default test mode
- ✅ Start with small quantities
- ✅ Monitor logs for all activity  
- ✅ Keep API keys secure

Happy trading! 🚀