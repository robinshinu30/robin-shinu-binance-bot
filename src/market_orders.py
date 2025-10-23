"""Place market orders on Binance Futures Testnet using python-binance.

This module provides a comprehensive helper to place market orders on Binance USDT-M Futures
using the python-binance library. It supports both .env file and environment variable
configuration, with full Testnet support and extensive error handling.

Usage (example):
    from src.market_orders import place_market_order

    # Test order validation (no execution)
    place_market_order('BTCUSDT', 'BUY', quantity=0.001, testnet=True, test=True)
    
    # Actual order (be careful!)
    place_market_order('BTCUSDT', 'BUY', quantity=0.001, testnet=True, test=False)

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
    from binance.enums import SIDE_BUY, SIDE_SELL
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


def _validate_order_params(symbol: str, side: str, quantity: float) -> tuple[str, str, float]:
    """Validate order parameters."""
    symbol = symbol.upper().strip()
    side = side.upper().strip()
    
    if not symbol:
        raise OrderError("Symbol cannot be empty")
    
    if side not in ('BUY', 'SELL'):
        raise OrderError(f"Side must be 'BUY' or 'SELL', got: {side}")
    
    if quantity <= 0:
        raise OrderError(f"Quantity must be positive, got: {quantity}")
    
    # Basic symbol validation
    if not symbol.endswith('USDT') or len(symbol) < 5:
        logger.warning(f"Symbol {symbol} may not be valid for USDT-M Futures")
    
    return symbol, side, quantity


def place_market_order(
    symbol: str,
    side: str,
    quantity: float,
    api_key: Optional[str] = None,
    api_secret: Optional[str] = None,
    testnet: bool = True,
    reduce_only: bool = False,
    test: bool = False,
) -> Dict[str, Any]:
    """Place a market order on Binance USDT-M Futures with comprehensive error handling.

    Args:
        symbol: Trading pair symbol, e.g. 'BTCUSDT'.
        side: 'BUY' or 'SELL'.
        quantity: Quantity in contract units (check contract specifics on Binance).
        api_key/api_secret: Optional API credentials (fallback to env vars/.env file).
        testnet: If True, configure the client to use Futures testnet base URL.
        reduce_only: If True, mark order as reduce-only (closes existing positions).
        test: If True, use test endpoint to validate without executing.

    Returns:
        Dict containing order response or test validation result.

    Raises:
        ConfigurationError: Authentication or client setup issues.
        OrderError: Order validation or placement issues.
        BinanceBotError: Other bot-related errors.
    """
    try:
        # Validate inputs
        symbol, side, quantity = _validate_order_params(symbol, side, quantity)
        
        # Get configured client
        client = _get_client(api_key, api_secret, testnet)
        
        # Prepare order parameters
        order_params = {
            'symbol': symbol,
            'side': SIDE_BUY if side == 'BUY' else SIDE_SELL,
            'type': 'MARKET',
            'quantity': quantity,
        }
        
        if reduce_only:
            order_params['reduceOnly'] = True
            logger.info("Order marked as reduce-only (position closing)")

        # Execute order or test
        if test:
            logger.info(f'🧪 Testing market order: {symbol} {side} {quantity}')
            try:
                result = client.futures_create_test_order(**order_params)
                logger.info('✅ Test order validation successful')
                return {
                    'test': True, 
                    'valid': True,
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'testnet': testnet,
                    'result': result
                }
            except BinanceAPIException as e:
                logger.error(f'❌ Test order validation failed: {e}')
                raise OrderError(f"Order validation failed: {e}")
        else:
            logger.info(f'🚀 Placing market order: {symbol} {side} {quantity}')
            logger.warning("⚠️  This will place a REAL order!")
            
            try:
                result = client.futures_create_order(**order_params)
                logger.info(f'✅ Order placed successfully: Order ID {result.get("orderId")}')
                return result
            except BinanceOrderException as e:
                logger.error(f'❌ Order placement failed: {e}')
                raise OrderError(f"Failed to place order: {e}")
            except BinanceAPIException as e:
                logger.error(f'❌ API error: {e}')
                raise OrderError(f"Binance API error: {e}")

    except (ConfigurationError, OrderError):
        raise  # Re-raise our custom exceptions
    except Exception as e:
        logger.exception(f'❌ Unexpected error in place_market_order: {e}')
        raise BinanceBotError(f"Unexpected error: {e}")


def main():
    """CLI interface for placing market orders."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Place market orders on Binance Futures Testnet',
        epilog='Example: py -m src.market_orders BTCUSDT BUY 0.001 --test'
    )
    parser.add_argument('symbol', help='Trading pair symbol (e.g., BTCUSDT)')
    parser.add_argument('side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=float, help='Order quantity in contracts')
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
        print("⚠️  WARNING: This will place a REAL order!")
        input("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        result = place_market_order(
            symbol=args.symbol,
            side=args.side,
            quantity=args.quantity,
            testnet=testnet,
            reduce_only=args.reduce_only,
            test=test_mode
        )
        
        print("✅ Success!")
        if test_mode:
            print("🧪 Test order validated successfully")
        else:
            print(f"🚀 Order placed: {result}")
            
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
