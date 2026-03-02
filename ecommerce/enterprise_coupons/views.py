"""
Views for enterprise coupons application.
"""

import logging

from django.conf import settings
from django.shortcuts import redirect
from django.views import View

from ecommerce.enterprise_coupons.backends.base import get_enterprise_catalog_uuid_from_coupon
from ecommerce.enterprise_coupons.exceptions import CatalogueNotFoundError, CouponError, CouponNotFoundError
from ecommerce.enterprise_coupons.utils import get_build_mfe_base_url

logger = logging.getLogger(__name__)


class CouponRedirectView(View):
    """
    View to redirect users to the MFE catalog page based on a coupon code.

    This view extracts the catalog UUID from the provided coupon code and redirects
    the user to the appropriate MFE catalog page with the catalog UUID as a parameter.

    Returns:
        - 302: Redirect to MFE catalog page on success
        - 302: Redirect to error page (ENTERPRISE_COUPONS_ERROR_MFE_URL or LMS root) on any error

    Error Handling:
        All errors (coupon not found, catalogue not found, configuration errors, etc.)
        are logged internally with detailed information for debugging, but users are
        simply redirected to an error page to avoid exposing implementation details.

    Configuration:
        - ENTERPRISE_COUPONS_ERROR_MFE_URL: Optional setting to specify where to redirect on errors
        - Falls back to LMS root URL if ENTERPRISE_COUPONS_ERROR_MFE_URL is not configured
    """
    def get(self, request, coupon_code):
        try:
            catalog_uuid = get_enterprise_catalog_uuid_from_coupon(coupon_code)
            mfe_url = get_build_mfe_base_url(catalog_uuid, coupon_code)
            return redirect(mfe_url)
        except CouponNotFoundError as e:
            logger.error('Coupon not found: %s - Error: %s', coupon_code, str(e))
        except CatalogueNotFoundError as e:
            logger.error('Catalogue not found for coupon: %s - Error: %s', coupon_code, str(e))
        except CouponError as e:
            logger.error('Coupon error for code %s: %s', coupon_code, str(e))
        except ValueError as e:
            logger.error('Configuration error: %s', str(e))
        except Exception as e:
            logger.exception('Unexpected error processing coupon %s: %s', coupon_code, str(e))

        error_url = getattr(settings, 'ENTERPRISE_COUPONS_ERROR_MFE_URL', request.site.siteconfiguration.lms_url_root)
        return redirect(error_url)
