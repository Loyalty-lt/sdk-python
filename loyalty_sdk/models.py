"""
Data models for Loyalty.lt SDK.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model."""
    id: int
    phone: str
    name: Optional[str] = None
    email: Optional[str] = None
    is_verified: bool = False
    avatar: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    locale: str = "en"
    timezone: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class LoyaltyCard(BaseModel):
    """Loyalty card model."""
    id: int
    user_id: int
    card_type: str  # digital, physical
    card_number: str
    brand_name: str
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    logo_url: Optional[str] = None
    qr_code: Optional[str] = None
    barcode: Optional[str] = None
    is_active: bool = True
    is_third_party: bool = False
    points_balance: int = 0
    custom_fields: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PointsTransaction(BaseModel):
    """Points transaction model."""
    id: int
    loyalty_card_id: int
    points: int
    type: str  # earned, redeemed, expired, adjusted, transfer
    description: str
    reference_id: Optional[str] = None
    reference_type: Optional[str] = None
    balance_after: int
    expires_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    # Relationships
    loyalty_card: Optional[LoyaltyCard] = None


class Offer(BaseModel):
    """Offer model."""
    id: int
    title: str
    description: str
    image: Optional[str] = None
    type: str  # discount, points_multiplier, free_item, cashback
    discount_type: Optional[str] = None  # percentage, fixed_amount
    discount_percentage: Optional[float] = None
    discount_amount: Optional[float] = None
    points_multiplier: Optional[float] = None
    points_cost: Optional[int] = None
    minimum_purchase: Optional[float] = None
    maximum_discount: Optional[float] = None
    is_active: bool = True
    is_featured: bool = False
    categories: List[str] = []
    partner_name: Optional[str] = None
    partner_logo: Optional[str] = None
    usage_limit: Optional[int] = None
    usage_count: int = 0
    user_limit: Optional[int] = None
    terms_conditions: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class Coupon(BaseModel):
    """Coupon model."""
    id: int
    user_id: int
    offer_id: int
    code: str
    status: str  # active, redeemed, expired, cancelled
    qr_code: Optional[str] = None
    barcode: Optional[str] = None
    redeemed_at: Optional[datetime] = None
    redemption_reference: Optional[str] = None
    expires_at: Optional[datetime] = None
    meta_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    offer: Optional[Offer] = None


class Game(BaseModel):
    """Game model."""
    id: int
    name: str
    description: str
    type: str  # slot_machine, wheel_of_fortune, scratch_card, memory, quiz, puzzle
    image: Optional[str] = None
    is_active: bool = True
    is_featured: bool = False
    categories: List[str] = []
    points_cost: Optional[int] = None
    daily_limit: Optional[int] = None
    total_limit: Optional[int] = None
    min_score_for_reward: Optional[int] = None
    rewards: List[Dict[str, Any]] = []
    game_config: Optional[Dict[str, Any]] = None
    instructions: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class GameSession(BaseModel):
    """Game session model."""
    id: int
    user_id: int
    game_id: int
    session_key: str
    status: str  # active, completed, expired, cancelled
    score: Optional[int] = None
    level: Optional[int] = None
    progress_data: Optional[Dict[str, Any]] = None
    reward_claimed: Optional[Dict[str, Any]] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Relationships
    game: Optional[Game] = None


class QrLoginSession(BaseModel):
    """QR login session model."""
    session_id: str
    qr_code: str
    status: str  # pending, scanned, confirmed, rejected, expired
    device_info: Optional[str] = None
    user_id: Optional[int] = None
    tokens: Optional[Dict[str, str]] = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel):
    """Paginated response model."""
    data: List[Any]
    meta: Dict[str, Any]


class ApiResponse(BaseModel):
    """API response model."""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    code: Optional[str] = None
    errors: Optional[Dict[str, List[str]]] = None 
 
 