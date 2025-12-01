"""
Helper methods for enterprise app.
"""
from django.conf import settings


def get_build_mfe_base_url(catalog_uuid, base_url):
    """
    Build the base URL for the ecommerce microfrontend receipt page with catalog parameter.

    Args:
        catalog_uuid (UUID): The catalog UUID to include in the microfrontend URL.
        base_url (str): The base URL of the LMS instance.

    Returns:
        str: The complete URL for the ecommerce microfrontend receipt page with the catalog parameter appended.

    Raises:
        ValueError: If ENTERPRISE_COUPONS_MFE_URL is not configured in settings.
    """
    mfe_path = getattr(settings, 'ENTERPRISE_COUPONS_MFE_URL', None)
    if not mfe_path:
        raise ValueError('ENTERPRISE_COUPONS_MFE_URL is not configured in settings.')

    return f'{base_url}{mfe_path}?catalog={catalog_uuid}'
