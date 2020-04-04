from django.urls import path
from .views import LocationListView, LocationDetailView
from .views import HistoricEntryListView, HistoricEntryDetailView

urlpatterns = [
    path('', LocationListView.as_view()),
    path('<pk>', LocationDetailView.as_view())
]