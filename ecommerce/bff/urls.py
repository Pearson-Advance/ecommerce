

from django.urls import include, re_path as url

urlpatterns = [
    url(r'^payment/', include(('ecommerce.bff.payment.urls', 'payment'))),
    url(r'subscriptions/', include(('ecommerce.bff.subscriptions.urls', 'subscriptions')))

]
