from rest_framework.generics import ListAPIView, RetrieveAPIView
from corona_plots.models import Location, HistoricEntry, ProvinceState
from corona_plots.models import CountryRegion, County
from .serializers import LocationSerializer, HistoricEntrySerializer
from .serializers import ProvinceStateSerializer, CountryRegionSerializer
from .serializers import CountySerializer


class LocationListView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailView(RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class ProvinceStateListView(ListAPIView):
    queryset = ProvinceState.objects.all()
    serializer_class =  ProvinceStateSerializer

class ProvinceStateDetailView(RetrieveAPIView):
    queryset = ProvinceState.objects.all()
    serializer_class = ProvinceStateSerializer

class CountryRegionListView(ListAPIView):
    queryset = CountryRegion.objects.all()
    serializer_class = CountryRegionSerializer

class CountryRegionDetailView(RetrieveAPIView):
    queryset = CountryRegion.objects.all()
    serializer_class = CountryRegionSerializer

class CountyListView(ListAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class CountyDetailView(RetrieveAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class HistoricEntryListView(ListAPIView):
    queryset = HistoricEntry.objects.all()
    serializer_class = HistoricEntrySerializer

class HistoricEntryDetailView(RetrieveAPIView):
    queryset = HistoricEntry.objects.all()
    serializer_class = HistoricEntrySerializer