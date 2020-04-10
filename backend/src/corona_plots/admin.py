from django.contrib import admin

# Register your models here.
from .models import Location, HistoricEntry, ProvinceState, CountryRegion, County
from .models import CaseType

admin.site.register(Location)
admin.site.register(HistoricEntry)
admin.site.register(ProvinceState)
admin.site.register(CountryRegion)
admin.site.register(County)
admin.site.register(CaseType)
