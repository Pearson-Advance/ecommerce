from oscar.apps.dashboard.catalogue import apps


class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    name = 'ecommerce.extensions.dashboard.catalogue'
    label = 'dashboard_catalogue'
