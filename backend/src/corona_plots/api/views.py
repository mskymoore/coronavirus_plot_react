from rest_framework.generics import ListAPIView, RetrieveAPIView
from corona_plots.models import Location, HistoricEntry, ProvinceState
from corona_plots.models import CountryRegion, County, CaseType
from .serializers import LocationSerializer, HistoricEntrySerializer
from .serializers import ProvinceStateSerializer, CountryRegionSerializer
from .serializers import CountySerializer
from corona_plots.methods import generate_series
from django.http import HttpResponse
import json


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


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

class HistoricEntryListView(MultipleFieldLookupMixin, ListAPIView):
    queryset = HistoricEntry.objects.all()
    serializer_class = HistoricEntrySerializer
    lookup_fields = ('pk', 'province_state')


class HistoricEntryDetailView(RetrieveAPIView):
    queryset = HistoricEntry.objects.all()
    serializer_class = HistoricEntrySerializer

def GetSeries(request):
    locationFriendlyHash = request.GET['friendly_hash']
    caseType = request.GET['case_type']
    location = Location.objects.get(pk=locationFriendlyHash)
    response = generate_series(caseType, location)
    return HttpResponse(json.dumps(response))

