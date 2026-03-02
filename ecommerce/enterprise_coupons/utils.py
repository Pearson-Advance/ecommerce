"""
Helper methods for enterprise app.
"""
from urllib.parse import urlencode, urljoin

from django.conf import settings


def get_build_mfe_base_url(catalog_uuid, coupon_code):
    """
    Build the base URL for the ecommerce microfrontend receipt page with catalog and coupon parameters.

    Args:
        catalog_uuid (UUID): The catalog UUID to include in the microfrontend URL.
        coupon_code (str): The coupon code to include in the microfrontend URL.

    Returns:
        str: The complete URL for the ecommerce microfrontend receipt page with the catalog
             and coupon_code parameters appended.

    Raises:
        ValueError: If ENTERPRISE_COUPONS_MFE_URL is not configured in settings.
    """
    mfe_path = getattr(settings, 'ENTERPRISE_COUPONS_MFE_URL', None)
    if not mfe_path:
        raise ValueError('ENTERPRISE_COUPONS_MFE_URL is not configured in settings.')

    return f"{mfe_path}?{urlencode({'catalog': catalog_uuid, 'coupon_code': coupon_code})}"
