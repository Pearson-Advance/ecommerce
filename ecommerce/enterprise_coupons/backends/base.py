from abc import ABC, abstractmethod

from django.conf import settings
from django.utils.module_loading import import_string


class EnterpriseCouponBackend(ABC):
    """Base class for enterprise coupon backends."""

    @abstractmethod
    def get_catalog_uuid(self, coupon_code):
        """Get the catalog UUID for a coupon code."""


def get_coupon_backend():
    """Load and return configured coupon backend."""
    return import_string(settings.ENTERPRISE_COUPON_BACKEND)()


def get_enterprise_catalog_uuid_from_coupon(coupon_code):
    """Get catalog UUID using configured backend."""
    return get_coupon_backend().get_catalog_uuid(coupon_code)
