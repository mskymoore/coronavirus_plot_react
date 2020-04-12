from django.urls import path
from .views import LocationListView, LocationDetailView
from .views import EntryDateListView, EntryDateDetailView
from .views import ProvinceStateListView, ProvinceStateDetailView
from .views import CountryRegionListView, CountryRegionDetailView
from .views import CountyListView, CountyDetailView, GetSeries

urlpatterns = [
    path('locations', LocationListView.as_view()),
    path('location/<pk>', LocationDetailView.as_view()),
    path('region_entries/<case_status_type_id>/<region_country>', EntryDateListView.as_view()),
    path('state_entries/<case_status_type_id>/<province_state>', EntryDateListView.as_view()),
    path('county_entries/<case_status_type_id>/<county>', EntryDateListView.as_view()),
]