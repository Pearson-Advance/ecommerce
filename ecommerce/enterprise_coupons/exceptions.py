"""
Custom exceptions for enterprise coupons application.
"""


class CouponError(Exception):
    """Base exception for coupon-related errors."""
    message = 'Invalid coupon.'


class CouponNotFoundError(CouponError):
    """Raised when a coupon code does not exist."""
    message = 'Coupon code not found.'


class CatalogueNotFoundError(CouponError):
    """Raised when no catalogue is found for a coupon."""
    message = 'No catalogue available for this coupon.'
