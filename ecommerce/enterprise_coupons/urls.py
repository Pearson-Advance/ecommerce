"""
URL configuration for enterprise_coupons app.
"""

from django.urls import path

from ecommerce.enterprise_coupons import views

urlpatterns = [
    path(
        '<str:coupon_code>/',
        views.CouponRedirectView.as_view(),
        name='coupon_redirect',
    ),
]
