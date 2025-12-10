"""
Exceptions for Loyalty.lt SDK.
"""


class LoyaltySDKError(Exception):
    """Base exception for SDK errors."""
    
    def __init__(self, message: str, code: str = 'UNKNOWN_ERROR', http_status: int = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status
    
    def __str__(self):
        return f"[{self.code}] {self.message}"
    
    def to_dict(self):
        return {
            'message': self.message,
            'code': self.code,
            'http_status': self.http_status,
        }


class LoyaltyAPIError(LoyaltySDKError):
    """Exception for API-level errors."""
    pass


class LoyaltyAuthError(LoyaltySDKError):
    """Exception for authentication errors."""
    pass
