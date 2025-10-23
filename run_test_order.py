"""Test runner for Binance Futures Testnet market orders.

Usage:
    py run_test_order.py BTCUSDT BUY 0.001

This script uses the test endpoint by default (no actual order execution). 
Configure API keys in .env file or environment variables before running.

Features:
- Safe test-only execution by default
- Comprehensive error handling  
- Configuration validation
- Supports .env file loading
"""
import argparse
import os
import sys
from pathlib import Path

try:
    from src.market_orders import place_market_order, ConfigurationError, OrderError, BinanceBotError
    from src.limit_orders import place_limit_order
except ImportError as e:
    print(f"❌ Failed to import trading modules: {e}")
    print("Make sure you're running from the project root and dependencies are installed.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Test market and limit orders on Binance Futures Testnet',
        epilog='Examples:\n  py run_test_order.py BTCUSDT BUY 0.001\n  py run_test_order.py BTCUSDT BUY 0.001 --type limit --price 60000',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side') 
    parser.add_argument('quantity', type=float, help='Order quantity in contracts')
    parser.add_argument('--type', choices=['market', 'limit'], default='market',
                       help='Order type: market (default) or limit')
    parser.add_argument('--price', type=float, 
                       help='Limit price (required for limit orders)')
    parser.add_argument('--live', action='store_true', 
                       help='Place REAL order instead of test (dangerous!)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable detailed logging')
    
    args = parser.parse_args()
    
    # Validate limit order requirements
    if args.type == 'limit' and args.price is None:
        print("❌ Error: --price is required for limit orders")
        parser.print_help()
        sys.exit(1)
    
    # Display configuration status
    print("🔧 Configuration Check:")
    env_file = Path('.env')
    if env_file.exists():
        print(f"   ✅ .env file found: {env_file.absolute()}")
    else:
        print(f"   ⚠️  .env file not found, using system environment variables")
    
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')
    
    print(f"   {'✅' if api_key else '❌'} BINANCE_API_KEY: {'Set' if api_key else 'Missing'}")
    print(f"   {'✅' if api_secret else '❌'} BINANCE_API_SECRET: {'Set' if api_secret else 'Missing'}")
    print()
    
    # Safety warning for live orders
    if args.live:
        print("⚠️  WARNING: --live flag detected!")
        print("   This will place a REAL order on the Testnet!")
        response = input("   Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("   Cancelled by user")
            return
        print()
    
    # Execute order
    test_mode = not args.live
    order_type = args.type.upper()
    
    try:
        if args.type == 'limit':
            print(f"🚀 {'Testing' if test_mode else 'Placing'} limit order:")
            print(f"   Symbol: {args.symbol}")
            print(f"   Side: {args.side}")  
            print(f"   Quantity: {args.quantity}")
            print(f"   Price: ${args.price}")
            print(f"   Type: LIMIT")
            print(f"   Mode: {'TEST (validation only)' if test_mode else 'LIVE (real order)'}")
            print()
            
            result = place_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
                testnet=True,  # Always use testnet for this example
                test=test_mode
            )
        else:
            print(f"🚀 {'Testing' if test_mode else 'Placing'} market order:")
            print(f"   Symbol: {args.symbol}")
            print(f"   Side: {args.side}")  
            print(f"   Quantity: {args.quantity}")
            print(f"   Type: MARKET")
            print(f"   Mode: {'TEST (validation only)' if test_mode else 'LIVE (real order)'}")
            print()
            
            result = place_market_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                testnet=True,  # Always use testnet for this example
                test=test_mode
            )
        
        print("✅ Success!")
        if args.verbose:
            print(f"   Full result: {result}")
        elif test_mode:
            if args.type == 'limit':
                print(f"   Limit order parameters validated successfully: {args.symbol} {args.side} {args.quantity} @ ${args.price}")
            else:
                print("   Market order parameters validated successfully")
        else:
            order_id = result.get('orderId', 'Unknown')
            print(f"   Order ID: {order_id}")
            
    except ConfigurationError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Quick fix:")
        print("   1. Get Testnet API keys from: https://testnet.binancefuture.com/")
        print("   2. Add them to .env file or run: .\\setup.ps1")
        sys.exit(1)
        
    except OrderError as e:
        print(f"❌ Order Error: {e}")
        sys.exit(1)
        
    except BinanceBotError as e:
        print(f"❌ Bot Error: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()