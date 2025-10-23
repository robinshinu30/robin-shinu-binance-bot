"""Place limit orders on Binance Futures Testnet using python-binance.

This module provides comprehensive functionality to place limit orders on Binance USDT-M Futures
using the python-binance library. It supports both .env file and environment variable
configuration, with full Testnet support and extensive error handling.

Usage (example):
    from src.limit_orders import place_limit_order

    # Test limit order validation (no execution)
    place_limit_order('BTCUSDT', 'BUY', quantity=0.001, price=60000, testnet=True, test=True)
    
    # Actual limit order (be careful!)
    place_limit_order('BTCUSDT', 'BUY', quantity=0.001, price=60000, testnet=True, test=False)

Configuration:
  Create a .env file or set environment variables:
  - BINANCE_API_KEY: your Testnet API key
  - BINANCE_API_SECRET: your Testnet API secret

Safety:
  - Always use Testnet keys from https://testnet.binancefuture.com/
  - Use test=True first to validate order parameters
  - Never use mainnet credentials for testing
"""
from typing import Optional, Dict, Any
import os
import logging
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # python-dotenv not installed, use system env vars only

try:
    from binance.client import Client
    from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
    from binance.exceptions import BinanceAPIException, BinanceOrderException
except ImportError as e:
    print(f"Error: python-binance not installed. Run: py -m pip install python-binance")
    print(f"Import error: {e}")
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BinanceBotError(Exception):
    """Base exception for Binance bot errors."""
    pass


class ConfigurationError(BinanceBotError):
    """Configuration or authentication error."""
    pass


class OrderError(BinanceBotError):
    """Order placement or validation error."""
    pass


def _validate_credentials(api_key: Optional[str], api_secret: Optional[str]) -> tuple[str, str]:
    """Validate and return API credentials."""
    if api_key is None:
        api_key = os.environ.get('BINANCE_API_KEY')
    if api_secret is None:
        api_secret = os.environ.get('BINANCE_API_SECRET')

    if not api_key:
        raise ConfigurationError(
            'BINANCE_API_KEY not found. Set it in .env file or environment variable.'
        )
    if not api_secret:
        raise ConfigurationError(
            'BINANCE_API_SECRET not found. Set it in .env file or environment variable.'
        )
    
    if api_key.strip() in ('your_testnet_api_key_here', 'your_api_key'):
        raise ConfigurationError(
            'Please replace placeholder API key with your actual Testnet key from https://testnet.binancefuture.com/'
        )
    
    return api_key.strip(), api_secret.strip()


def _get_client(api_key: Optional[str], api_secret: Optional[str], testnet: bool) -> Client:
    """Create a python-binance Client configured for Futures testnet when requested."""
    try:
        api_key, api_secret = _validate_credentials(api_key, api_secret)
        
        client = Client(api_key, api_secret)

        if testnet:
            # Configure for Futures testnet
            client.FUTURES_URL = 'https://testnet.binancefuture.com'
            logger.info("Configured client for Binance Futures Testnet")
        else:
            logger.warning("Using MAINNET - ensure this is intentional!")

        return client
    
    except Exception as e:
        raise ConfigurationError(f"Failed to create Binance client: {e}")


def _validate_limit_order_params(symbol: str, side: str, quantity: float, price: float) -> tuple[str, str, float, float]:
    """Validate limit order parameters."""
    symbol = symbol.upper().strip()
    side = side.upper().strip()
    
    if not symbol:
        raise OrderError("Symbol cannot be empty")
    
    if side not in ('BUY', 'SELL'):
        raise OrderError(f"Side must be 'BUY' or 'SELL', got: {side}")
    
    if quantity <= 0:
        raise OrderError(f"Quantity must be positive, got: {quantity}")
    
    if price <= 0:
        raise OrderError(f"Price must be positive, got: {price}")
    
    # Basic symbol validation
    if not symbol.endswith('USDT') or len(symbol) < 5:
        logger.warning(f"Symbol {symbol} may not be valid for USDT-M Futures")
    
    return symbol, side, quantity, price


def place_limit_order(
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    testnet: bool = True,
    reduce_only: bool = False,
    test: bool = False,
    time_in_force: str = 'GTC'
) -> Dict[str, Any]:
    """Place a limit order on Binance USDT-M Futures with comprehensive error handling.

    Args:
        symbol: Trading pair symbol, e.g. 'BTCUSDT'.
        side: 'BUY' or 'SELL'.
        quantity: Quantity in contract units (check contract specifics on Binance).
        price: Limit price for the order.
        api_key/api_secret: Optional API credentials (fallback to env vars/.env file).
        testnet: If True, configure the client to use Futures testnet base URL.
        reduce_only: If True, mark order as reduce-only (closes existing positions).
        test: If True, use test endpoint to validate without executing.
        time_in_force: Order time in force ('GTC', 'IOC', 'FOK'). Default: 'GTC'.

    Returns:
        Dict containing order response or test validation result.

    Raises:
        ConfigurationError: Authentication or client setup issues.
        OrderError: Order validation or placement issues.
        BinanceBotError: Other bot-related errors.
    """
    try:
        # Validate inputs
        symbol, side, quantity, price = _validate_limit_order_params(symbol, side, quantity, price)
        
        # Get configured client
        client = _get_client(api_key, api_secret, testnet)
        
        # Prepare order parameters
        order_params = {
            'symbol': symbol,
            'side': SIDE_BUY if side == 'BUY' else SIDE_SELL,
            'type': ORDER_TYPE_LIMIT,
            'quantity': quantity,
            'price': price,
            'timeInForce': TIME_IN_FORCE_GTC if time_in_force == 'GTC' else time_in_force,
        }
        
        if reduce_only:
            order_params['reduceOnly'] = True
            logger.info("Order marked as reduce-only (position closing)")

        # Execute order or test
        if test:
            logger.info(f'🧪 Testing limit order: {symbol} {side} {quantity} @ ${price}')
            try:
                result = client.futures_create_test_order(**order_params)
                logger.info('✅ Test limit order validation successful')
                return {
                    'test': True, 
                    'valid': True,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'price': price,
                    'type': 'LIMIT',
                    'testnet': testnet,
                    'result': result
                }
            except BinanceAPIException as e:
                logger.error(f'❌ Test limit order validation failed: {e}')
                raise OrderError(f"Limit order validation failed: {e}")
        else:
            logger.info(f'🚀 Placing limit order: {symbol} {side} {quantity} @ ${price}')
            logger.warning("⚠️  This will place a REAL limit order!")
            
            try:
                result = client.futures_create_order(**order_params)
                logger.info(f'✅ Limit order placed successfully: Order ID {result.get("orderId")}')
                return result
            except BinanceOrderException as e:
                logger.error(f'❌ Limit order placement failed: {e}')
                raise OrderError(f"Failed to place limit order: {e}")
            except BinanceAPIException as e:
                logger.error(f'❌ API error: {e}')
                raise OrderError(f"Binance API error: {e}")

    except (ConfigurationError, OrderError):
        raise  # Re-raise our custom exceptions
    except Exception as e:
        logger.exception(f'❌ Unexpected error in place_limit_order: {e}')
        raise BinanceBotError(f"Unexpected error: {e}")


def main():
    """CLI interface for placing limit orders."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Place limit orders on Binance Futures Testnet',
        epilog='Example: py -m src.limit_orders BTCUSDT BUY 0.001 60000 --test'
    )
    parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=float, help='Order quantity in contracts')
    parser.add_argument('price', type=float, help='Limit price')
    parser.add_argument('--test', action='store_true', default=True, 
                       help='Use test endpoint (default: True, no execution)')
    parser.add_argument('--live', action='store_true', 
                       help='Place REAL order (dangerous! Use with caution)')
    parser.add_argument('--mainnet', action='store_true', 
                       help='Use mainnet instead of testnet (VERY dangerous!)')
    parser.add_argument('--reduce-only', action='store_true', 
                       help='Mark order as reduce-only (position closing)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Safety checks
    testnet = not args.mainnet
    test_mode = not args.live
    
    if args.mainnet:
        print("⚠️  WARNING: Using MAINNET - this could place real orders with real money!")
        input("Press Enter to continue or Ctrl+C to cancel...")
    
    if args.live:
        print("⚠️  WARNING: This will place a REAL limit order!")
        input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = place_limit_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            price=args.price,
            testnet=testnet,
            reduce_only=args.reduce_only,
            test=test_mode
        )
        
        print("✅ Success!")
        if test_mode:
            print(f"🧪 Test limit order validated successfully: {args.symbol} {args.side} {args.quantity} @ ${args.price}")
        else:
            print(f"🚀 Limit order placed: {result}")
            
    except (ConfigurationError, OrderError, BinanceBotError) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()