from oscar.core.loading import get_model

from ecommerce.enterprise_coupons.backends.base import EnterpriseCouponBackend
from ecommerce.enterprise_coupons.exceptions import CatalogueNotFoundError, CouponNotFoundError

Voucher = get_model('voucher', 'Voucher')


class VoucherModelBackend(EnterpriseCouponBackend):
    """Backend that reads coupons from the database."""
    def get_catalog_uuid(self, coupon_code: str):
        """Extract catalog UUID from database voucher."""
        try:
            voucher = Voucher.objects.get(code=coupon_code)
        except Voucher.DoesNotExist as e:
            raise CouponNotFoundError() from e

        catalog_uuid = (
            voucher.offers
            .filter(condition__enterprise_customer_catalog_uuid__isnull=False)
            .values_list('condition__enterprise_customer_catalog_uuid', flat=True)
            .distinct()
            .first()
        )
        if not catalog_uuid:
            raise CatalogueNotFoundError()
        return catalog_uuid
