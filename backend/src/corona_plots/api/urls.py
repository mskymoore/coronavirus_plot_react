from django.urls import path
from .views import LocationListView, LocationDetailView
from .views import HistoricEntryListView, HistoricEntryDetailView
from .views import ProvinceStateListView, ProvinceStateDetailView
from .views import CountryRegionListView, CountryRegionDetailView
from .views import CountyListView, CountyDetailView, GetSeries

urlpatterns = [
    path('locations', LocationListView.as_view()),
    path('location/<pk>', LocationDetailView.as_view()),
    path('province_states', ProvinceStateListView.as_view()),
    path('province_state/<pk>', ProvinceStateDetailView.as_view()),
    path('country_regions', CountryRegionListView.as_view()),
    path('country_reigion/<pk>', CountryRegionDetailView.as_view()),
    path('counties', CountyListView.as_view()),
    path('county/<pk>', CountyDetailView.as_view()),
    path('historic_entries', HistoricEntryListView.as_view()),
    path('historic_entry/<province_state>', HistoricEntryListView.as_view()),
    path('province_state/<province_state>', HistoricEntryDetailView.as_view()),
    path('region_country/<pk>', HistoricEntryListView.as_view()),
    path('county/<location.county>', HistoricEntryListView.as_view()),
    path('coordinate/<location.latitude>,<location.longitude>', HistoricEntryListView.as_view()),
    path('series/', GetSeries)
]