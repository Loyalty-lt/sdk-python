"""
Loyalty.lt SDK for Python - Official Shop API client.

Usage:
    from loyalty_sdk import LoyaltySDK
    
    sdk = LoyaltySDK(
        api_key='lty_your_api_key',
        api_secret='your_api_secret'
    )
    
    shops = sdk.get_shops()
"""

from .client import LoyaltySDK
from .exceptions import LoyaltySDKError, LoyaltyAPIError, LoyaltyAuthError

__version__ = "1.0.0"
__all__ = [
    'LoyaltySDK',
    'LoyaltySDKError',
    'LoyaltyAPIError',
    'LoyaltyAuthError',
]
