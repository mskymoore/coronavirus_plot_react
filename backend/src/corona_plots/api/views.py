from rest_framework.generics import ListAPIView, RetrieveAPIView
from corona_plots.models import Location, EntryDate, ProvinceState
from corona_plots.models import CountryRegion, County, CaseType
from corona_plots.models import CountEntry, CountIncreaseEntry, CountPercentIncreaseEntry
from .serializers import LocationSerializer, EntryDateSerializer, CaseTypeSerializer
from .serializers import ProvinceStateSerializer, CountryRegionSerializer
from .serializers import CountySerializer, CaseTypeSerializer
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
    serializer_class = CountySerializer

    def get_queryset(self):
        if 'province_state' in self.kwargs:
            return County.objects.filter(
                province_state__province_state=self.kwargs['province_state']
            )

class CountyDetailView(RetrieveAPIView):
    queryset = County.objects.all()
    serializer_class = CountySerializer

class CountEntryListView(ListAPIView):
    pass


class CaseTypeListView(ListAPIView):
    serializer_class = CaseTypeSerializer

    def get_queryset(self):
        if 'hash' in self.kwargs:
            return CaseType.objects.filter(
                location__friendly_hash=self.kwargs['hash']
            )

class EntryDateListView(ListAPIView):
    serializer_class = EntryDateSerializer

    def get_queryset(self):
        if 'province_state' in self.kwargs:
            return EntryDate.objects.filter(
                        location__province_state=self.kwargs['province_state'],
                        location__region_country=None,
                        case_status_type_id=self.kwargs['case_status_type_id']
                   )
        elif 'region_country' in self.kwargs:
            return EntryDate.objects.filter(
                        location__region_country=self.kwargs['region_country'],
                        loaction__province_state=None,
                        case_status_type_id=self.kwargs['case_status_type_id']
                   )
        elif 'county' in self.kwargs:
            return EntryDate.objects.filter(
                        location__county=self.kwargs['county'],
                        case_status_type_id=self.kwargs['case_status_type_id']
                   )
        elif 'hash' in self.kwargs:
            return EntryDate.objects.filter(
                        location__friendly_hash=self.kwargs['hash'],
                        case_status_type_id=self.kwargs['case_status_type_id']
                   ) 
        else:
            return EntryDate.objects.none()



class EntryDateDetailView(RetrieveAPIView):
    queryset = EntryDate.objects.all()
    serializer_class = EntryDateSerializer

def GetSeries(request):
    locationFriendlyHash = request.GET['friendly_hash']
    caseType = request.GET['case_type']
    location = Location.objects.get(pk=locationFriendlyHash)
    response = generate_series(caseType, location)
    return HttpResponse(json.dumps(response))

