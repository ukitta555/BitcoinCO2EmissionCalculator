from django.urls import path
from .views import Co2AndElectricityPerLocationView, Co2AndElectricityPerPoolView

urlpatterns = [
    path('co2_and_electricity_date_range/', Co2AndElectricityPerLocationView.as_view(), name="get_metrics"),
    path('co2_and_electricity_per_pool/', Co2AndElectricityPerPoolView.as_view(), name="get_metrics_per_pool")
]