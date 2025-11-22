

from django.urls import re_path as url

from ecommerce.management import views

urlpatterns = [
    url(r'^$', views.ManagementView.as_view(), name='index'),
]
