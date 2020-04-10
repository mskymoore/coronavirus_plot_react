from rest_framework import serializers
from corona_plots.models import Location, HistoricEntry, ProvinceState
from corona_plots.models import CountryRegion, County



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('province_state',
                  'region_country',
                  'county',
                  'latitude',
                  'longitude',
                  'friendly_name',
                  'friendly_hash',
                  )

class HistoricEntrySerializer(serializers.ModelSerializer):
    province_state = serializers.CharField(source='location.province_state')
    region_country = serializers.CharField(source='location.region_country')
    county = serializers.CharField(source='location.county')

    class Meta:
        model = HistoricEntry
        fields = ('id',
                  'date',
                  'count',
                  'increase',
                  'province_state',
                  'region_country',
                  'county',
                  'location',
                  'case_status_type_id',
                  )

class HistoricEntryCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricEntry
        fields = ('count',)

class ProvinceStateSerializer(serializers.ModelSerializer):
    entries = serializers.StringRelatedField(many=True)
    class Meta:
        model = ProvinceState
        fields = ('province_state', 'entries')

class CountryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryRegion
        fields = ('region_country', 'entries')

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ('county', 'entries')
