from rest_framework.generics import ListAPIView, RetrieveAPIView
from corona_plots.models import Location, HistoricEntry, ProvinceState
from corona_plots.models import CountryRegion, County, Plot, CaseType
from .serializers import LocationSerializer, HistoricEntrySerializer
from .serializers import ProvinceStateSerializer, CountryRegionSerializer
from .serializers import CountySerializer, PlotSerializer
from corona_plots.methods import get_plots, generate_series
from django.http import HttpResponse
import json


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

class PlotDetailView(RetrieveAPIView):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer

class PlotsListView(ListAPIView):
    queryset = Plot.objects.all()
    serializer_class = PlotSerializer

def GetSeries(request):
    locationFriendlyHash = request.GET['friendly_hash']
    caseType = request.GET['case_type']
    location = Location.objects.all().filter(friendly_hash=locationFriendlyHash).first()
    response = generate_series(caseType, location)
    return HttpResponse(json.dumps(response))

def PlotsGen(request):
    locationFriendlyHash = request.GET['friendly_hash']
    location = Location.objects.all().filter(friendly_hash=locationFriendlyHash).first()
    case_types = ['confirmed', 'deaths']
    for case_type in case_types:
        aPlot = Plot(
            case_type = CaseType(case_type=case_type),
            location = location,
            name = location.friendly_hash + case_type,
            friendly_name = location.friendly_name + ' ' + case_type,
            plot = get_plots(location, case_type)
        )
        aPlot.save()
    return HttpResponse(json.dumps(f'{location.friendly_name} {case_types} plots generated'))



    

