from django.apps import AppConfig


class DashboardShippingConfig(AppConfig):
    """Wrapper AppConfig for Oscar's dashboard shipping app with unique label."""
    name = 'oscar.apps.dashboard.shipping'
    label = 'dashboard_shipping'

