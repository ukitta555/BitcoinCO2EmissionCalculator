from django.urls import path
from .views import Co2AndElectricityView

urlpatterns = [
    path('co2_and_electricity_date_range/', Co2AndElectricityView.as_view(), name="get_metrics")
]