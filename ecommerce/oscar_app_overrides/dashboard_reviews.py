from django.apps import AppConfig


class DashboardReviewsConfig(AppConfig):
    """Wrapper AppConfig for Oscar's dashboard reviews app.

    Sets a unique label to avoid collision with the catalogue reviews label.
    """
    name = 'oscar.apps.dashboard.reviews'
    label = 'dashboard_reviews'

