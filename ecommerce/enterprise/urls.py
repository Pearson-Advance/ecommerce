

from django.urls import include, re_path as url

from ecommerce.enterprise import views

OFFER_URLS = [
    url(r'^$', views.EnterpriseOfferListView.as_view(), name='list'),
    url(r'^new/$', views.EnterpriseOfferCreateView.as_view(), name='new'),
    url(r'^(?P<pk>[\d]+)/edit/$', views.EnterpriseOfferUpdateView.as_view(), name='edit'),
]

urlpatterns = [
    url(r'^offers/', include((OFFER_URLS, 'offers'))),
    url(r'^coupons/(.*)$', views.EnterpriseCouponAppView.as_view(), name='coupons'),
]
