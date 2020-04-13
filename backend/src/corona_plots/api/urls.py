from django.urls import path
from .views import LocationListView, LocationDetailView
from .views import EntryDateListView, EntryDateDetailView
from .views import ProvinceStateListView, ProvinceStateDetailView
from .views import CountryRegionListView, CountryRegionDetailView
from .views import CountyListView, CountyDetailView, GetSeries
from .views import CaseTypeListView

urlpatterns = [
    path('locations', LocationListView.as_view()),
    path('counties/<province_state>', CountyListView.as_view()),
    path('states/<region_country>', ProvinceStateListView.as_view()),
    path('regions', CountryRegionListView.as_view()),
    path('location/<pk>', LocationDetailView.as_view()),
    path('location/entries/<case_status_type_id>/<hash>', EntryDateListView.as_view()),
    path('location/case_types/<hash>', CaseTypeListView.as_view()),
    path('region_entries/<case_status_type_id>/<region_country>', EntryDateListView.as_view()),
    path('state_entries/<case_status_type_id>/<province_state>', EntryDateListView.as_view()),
    path('county_entries/<case_status_type_id>/<county>', EntryDateListView.as_view()),
]