from rest_framework import serializers
from corona_plots.models import Location, HistoricEntry


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('province_state',
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
        fields = ('date',
                  'count',
                  'location',
                  'case_status_type_id'
                  )
