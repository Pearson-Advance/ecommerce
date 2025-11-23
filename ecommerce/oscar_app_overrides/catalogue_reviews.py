from django.apps import AppConfig


class CatalogueReviewsConfig(AppConfig):
    """Wrapper AppConfig for Oscar's catalogue reviews app.

    This sets a unique label so Django doesn't see a duplicate "reviews" label
    when the dashboard reviews app is also installed.
    """
    name = 'oscar.apps.catalogue.reviews'
    label = 'catalogue_reviews'

