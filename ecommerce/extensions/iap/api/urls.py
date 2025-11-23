from django.urls import include, re_path as url

urlpatterns = [
    url(r'^v1/', include('ecommerce.extensions.iap.api.v1.urls')),
]
