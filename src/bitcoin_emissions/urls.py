from django.urls import path
from .views import Co2AndElectricityView, StartFetchingView, ImportPoolData, CleanAllTables

urlpatterns = [
    path('co2_and_electricity_date_range/', Co2AndElectricityView.as_view(), name="get_metrics"),
    path('start_fetching/', StartFetchingView.as_view(), name="start_fetching"),
    path('import_excel/', ImportPoolData.as_view(), name="import_data"),
    path('clean_db/', CleanAllTables.as_view(), name="clean_db")
]