from rest_framework import serializers
from corona_plots.models import Location, HistoricEntry, ProvinceState
from corona_plots.models import CountryRegion, County



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id',
                  'province_state',
                  'region_country',
                  'county',
                  'latitude',
                  'longitude',
                  'friendly_name',
                  'friendly_hash'
                  )

class HistoricEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricEntry
        fields = ('id',
                  'date',
                  'count',
                  'location',
                  'case_status_type_id'
                  )

class ProvinceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvinceState
        fields = ('province_state')

class CountryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRegion
        fields = ('region_country')

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ('county')