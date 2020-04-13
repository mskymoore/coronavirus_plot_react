from rest_framework import serializers
from corona_plots.models import Location, EntryDate, ProvinceState, CaseType
from corona_plots.models import CountryRegion, County, CountEntry
from corona_plots.models import CountIncreaseEntry, CountPercentIncreaseEntry



class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('case_types',
                  'province_state',
                  'region_country',
                  'county',
                  'latitude',
                  'longitude',
                  'friendly_hash',
                  'friendly_name'
                  )

class EntryDateSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='countentry.value')
    count_increase = serializers.IntegerField(source='countincreaseentry.value')
    count_percent_increase = serializers.IntegerField(source='countpercentincreaseentry.value')
    class Meta:
        model = EntryDate
        fields = ('date',
                  'count',
                  'count_increase',
                  'count_percent_increase'
                  )

class CaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseType
        fields = ('case_type',)


class CountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountEntry
        fields = ('count',)

class CountIncreaseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountIncreaseEntry
        fields = ('count_increase',)

class CountPercentIncreaseEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountPercentIncreaseEntry
        fields = ('count_percent_increase',)

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
