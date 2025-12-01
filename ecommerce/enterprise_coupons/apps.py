"""
Configuration for the Enterprise Coupons application.
"""
from django.apps import AppConfig


class EnterpriseCouponsConfig(AppConfig):
    """
    Django application configuration for Enterprise Coupons.

    This application manages coupon functionality for enterprise customers,
    enabling organizations to create and distribute bulk coupons for their members.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enterprise_coupons'
