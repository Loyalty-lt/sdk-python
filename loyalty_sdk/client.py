"""
Official Loyalty.lt SDK for Python - Partner API client.
"""

import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlencode
import requests

from .exceptions import LoyaltySDKError, LoyaltyAPIError


class LoyaltySDK:
    """
    Main SDK client for Loyalty.lt Partner API.
    
    Provides complete access to partner functionality including QR Login,
    QR Card Scan, transactions, offers, and more.
    """
    
    VERSION = "2.0.0"
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRIES = 3
    
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        environment: str = "production",
        locale: str = "lt",
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        debug: bool = False,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the Loyalty SDK.
        
        Args:
            api_key: Partner API Key (required)
            api_secret: Partner API Secret (required)
            environment: 'production' or 'staging' (default: 'production')
            locale: Language locale - 'lt' or 'en' (default: 'lt')
            timeout: Request timeout in seconds (default: 30)
            retries: Number of retry attempts (default: 3)
            debug: Enable debug logging (default: False)
            base_url: Override base URL (optional)
        """
        if not api_key:
            raise LoyaltySDKError("API Key is required", "INVALID_CONFIG")
        if not api_secret:
            raise LoyaltySDKError("API Secret is required", "INVALID_CONFIG")
        
        self.api_key = api_key
        self.api_secret = api_secret
        self.locale = locale
        self.timeout = timeout
        self.retries = retries
        self.debug = debug
        
        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            self.base_url = (
                "https://staging-api.loyalty.lt" if environment == "staging"
                else "https://api.loyalty.lt"
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': f'LoyaltySDK-Python/{self.VERSION}',
            'X-API-Key': self.api_key,
            'X-API-Secret': self.api_secret,
        })
    
    @property
    def api_url(self) -> str:
        """Get full API URL."""
        return f"{self.base_url}/{self.locale}/shop"
    
    # ===================
    # QR LOGIN (Partner API)
    # ===================
    
    def generate_qr_login(
        self, 
        device_name: Optional[str] = None, 
        shop_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate QR Login session for shop.
        
        Args:
            device_name: Name of device/terminal
            shop_id: Optional shop ID
            
        Returns:
            Dict with session_id, qr_code, expires_at
        """
        return self._request('POST', '/auth/qr-login/generate', {
            'device_name': device_name or 'Python SDK',
            'shop_id': shop_id,
        })
    
    def poll_qr_login(self, session_id: str) -> Dict[str, Any]:
        """
        Poll QR Login status.
        
        Args:
            session_id: QR login session ID
            
        Returns:
            Dict with status, user, token (when authenticated)
        """
        return self._request('POST', f'/auth/qr-login/poll/{session_id}')
    
    def send_app_link(
        self,
        phone: str,
        shop_id: int,
        customer_name: Optional[str] = None,
        language: str = 'lt'
    ) -> Dict[str, Any]:
        """
        Send app download link via SMS.
        
        Args:
            phone: Customer phone number
            shop_id: Shop ID (required)
            customer_name: Optional customer name
            language: SMS language ('lt' or 'en')
        """
        return self._request('POST', '/auth/send-app-link', {
            'phone': phone,
            'shop_id': shop_id,
            'customer_name': customer_name,
            'language': language,
        })
    
    # ===================
    # QR CARD SCAN (Partner API)
    # ===================
    
    def generate_qr_card_session(
        self,
        device_name: Optional[str] = None,
        shop_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate QR Card Scan session for POS.
        
        Args:
            device_name: Name of POS terminal
            shop_id: Optional shop ID
            
        Returns:
            Dict with session_id, qr_code, expires_at
        """
        return self._request('POST', '/qr-card/generate', {
            'device_name': device_name or 'POS Terminal',
            'shop_id': shop_id,
        })
    
    def poll_qr_card_status(self, session_id: str) -> Dict[str, Any]:
        """
        Poll QR Card Scan status.
        
        Args:
            session_id: QR card scan session ID
            
        Returns:
            Dict with status, card_data (when completed)
        """
        return self._request('GET', f'/qr-card/status/{session_id}')
    
    # ===================
    # ABLY REAL-TIME (Partner API)
    # ===================
    
    def get_ably_token(self, session_id: str) -> Dict[str, Any]:
        """
        Get Ably token for real-time updates.
        
        Args:
            session_id: QR login or QR card scan session ID
            
        Returns:
            Dict with token, channel
        """
        return self._request('POST', '/ably/token', {
            'session_id': session_id,
        })
    
    # ===================
    # SHOPS (Partner API)
    # ===================
    
    def get_shops(self, **filters) -> Dict[str, Any]:
        """
        Get partner shops.
        
        Args:
            **filters: Optional filters (is_active, is_virtual, etc.)
            
        Returns:
            Dict with data (list of shops) and meta (pagination)
        """
        return self._request('GET', '/shops', params=filters)
    
    # ===================
    # LOYALTY CARDS (Partner API)
    # ===================
    
    def get_loyalty_cards(self, **filters) -> Dict[str, Any]:
        """
        Get loyalty cards.
        
        Args:
            **filters: Optional filters (card_number, user_id, etc.)
            
        Returns:
            Dict with data (list of cards) and meta (pagination)
        """
        return self._request('GET', '/loyalty-cards', params=filters)
    
    def get_loyalty_card(self, card_id: int) -> Dict[str, Any]:
        """
        Get single loyalty card.
        
        Args:
            card_id: Loyalty card ID
            
        Returns:
            Card data dict
        """
        return self._request('GET', f'/loyalty-cards/{card_id}')
    
    def get_loyalty_card_info(self, **params) -> Dict[str, Any]:
        """
        Get loyalty card info by various identifiers.
        
        Args:
            **params: card_id, card_number, or user_id
            
        Returns:
            Card info dict
        """
        return self._request('GET', '/loyalty-cards/info', params=params)
    
    def get_points_balance(self, **params) -> Dict[str, Any]:
        """
        Get points balance for card.
        
        Args:
            **params: card_id or card_number
            
        Returns:
            Balance dict
        """
        return self._request('GET', '/loyalty-cards/balance', params=params)
    
    # ===================
    # TRANSACTIONS (Partner API)
    # ===================
    
    def create_transaction(
        self,
        card_id: int,
        amount: float,
        points: int,
        transaction_type: str = 'earn',
        description: Optional[str] = None,
        reference: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create transaction (award points).
        
        Args:
            card_id: Loyalty card ID
            amount: Transaction amount
            points: Points to award
            transaction_type: 'earn' or 'redeem'
            description: Optional description
            reference: Optional reference (order ID, etc.)
            
        Returns:
            Transaction data dict
        """
        data = {
            'card_id': card_id,
            'amount': amount,
            'points': points,
            'type': transaction_type,
            'description': description,
            'reference': reference,
            **kwargs
        }
        return self._request('POST', '/transactions/create', data)
    
    def award_points(self, **data) -> Dict[str, Any]:
        """
        Award points (alias for create_transaction).
        """
        return self._request('POST', '/transactions/award-points', data)
    
    def deduct_points(
        self,
        card_id: int,
        points: int,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deduct points.
        
        Args:
            card_id: Loyalty card ID
            points: Points to deduct
            description: Optional description
            
        Returns:
            Transaction data dict
        """
        return self._request('POST', '/transactions/deduct-points', {
            'card_id': card_id,
            'points': points,
            'description': description or 'Points deduction',
        })
    
    def get_transactions(self, **filters) -> Dict[str, Any]:
        """
        Get partner transactions.
        
        Args:
            **filters: Optional filters (card_id, type, etc.)
            
        Returns:
            Dict with data and meta
        """
        return self._request('GET', '/transactions', params=filters)
    
    # ===================
    # OFFERS (Partner API)
    # ===================
    
    def get_offers(self, **filters) -> Dict[str, Any]:
        """
        Get offers.
        
        Args:
            **filters: Optional filters (is_active, category, etc.)
            
        Returns:
            Dict with data and meta
        """
        return self._request('GET', '/offers', params=filters)
    
    def get_offer(self, offer_id: int) -> Dict[str, Any]:
        """
        Get single offer.
        """
        return self._request('GET', f'/offers/{offer_id}')
    
    def create_offer(self, **data) -> Dict[str, Any]:
        """
        Create offer.
        """
        return self._request('POST', '/offers', data)
    
    def update_offer(self, offer_id: int, **data) -> Dict[str, Any]:
        """
        Update offer.
        """
        return self._request('PUT', f'/offers/{offer_id}', data)
    
    def delete_offer(self, offer_id: int) -> None:
        """
        Delete offer.
        """
        self._request('DELETE', f'/offers/{offer_id}')
    
    def get_categories(self) -> List[str]:
        """
        Get offer categories.
        """
        return self._request('GET', '/categories')
    
    # ===================
    # XML IMPORT (Partner API)
    # ===================
    
    def import_from_url(self, url: str, **options) -> Dict[str, Any]:
        """
        Import offers from XML URL.
        
        Args:
            url: XML file URL
            **options: Import options (auto_publish, etc.)
        """
        return self._request('POST', '/xml-import/from-url', {
            'url': url,
            **options
        })
    
    def validate_xml(self, url: str) -> Dict[str, Any]:
        """
        Validate XML file.
        """
        return self._request('POST', '/xml-import/validate', {'url': url})
    
    def get_import_stats(self) -> Dict[str, Any]:
        """
        Get import statistics.
        """
        return self._request('GET', '/xml-import/stats')
    
    # ===================
    # SYSTEM (Partner API)
    # ===================
    
    def validate_credentials(self) -> Dict[str, Any]:
        """
        Validate API credentials.
        """
        return self._request('POST', '/validate-credentials')
    
    def health_check(self) -> Dict[str, Any]:
        """
        Health check.
        """
        return self._request('GET', '/system/health')
    
    # ===================
    # HTTP CLIENT
    # ===================
    
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Any:
        """
        Make HTTP request with retry logic.
        """
        url = f"{self.api_url}{endpoint}"
        
        # Filter out None values
        if data:
            data = {k: v for k, v in data.items() if v is not None}
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        
        if self.debug:
            print(f"[LoyaltySDK] {method} {url}")
            if data:
                print(f"[LoyaltySDK] Data: {data}")
            if params:
                print(f"[LoyaltySDK] Params: {params}")
        
        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if data else None,
                    params=params,
                    timeout=self.timeout
                )
                
                if self.debug:
                    print(f"[LoyaltySDK] Response: {response.status_code}")
                
                if response.status_code < 400:
                    result = response.json()
                    
                    if not result.get('success', True):
                        raise LoyaltyAPIError(
                            result.get('message', 'API request failed'),
                            result.get('code', 'API_ERROR'),
                            response.status_code
                        )
                    
                    # Return paginated or simple data
                    if 'data' in result and 'meta' in result:
                        return {
                            'data': result['data'],
                            'meta': result['meta']
                        }
                    
                    return result.get('data', result)
                
                # Handle errors
                try:
                    error_data = response.json()
                    raise LoyaltyAPIError(
                        error_data.get('message', f'HTTP {response.status_code}'),
                        error_data.get('code', 'HTTP_ERROR'),
                        response.status_code
                    )
                except ValueError:
                    raise LoyaltyAPIError(
                        f'HTTP {response.status_code}',
                        'HTTP_ERROR',
                        response.status_code
                    )
                    
            except requests.RequestException as e:
                if attempt == self.retries - 1:
                    raise LoyaltySDKError(f'Request failed: {str(e)}', 'NETWORK_ERROR')
                
                # Exponential backoff
                time.sleep(2 ** attempt)
        
        raise LoyaltySDKError('Maximum retry attempts exceeded', 'MAX_RETRIES_EXCEEDED')
