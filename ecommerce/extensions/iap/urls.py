from django.urls import include, re_path as url

urlpatterns = [
    url(r'', include('ecommerce.extensions.iap.api.urls')),
]
