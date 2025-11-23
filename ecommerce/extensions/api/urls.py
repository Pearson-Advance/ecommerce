

from django.urls import include, re_path as url

urlpatterns = [
    url(r'^v2/', include(('ecommerce.extensions.api.v2.urls', 'v2'))),
]
