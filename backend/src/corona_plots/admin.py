from django.contrib import admin

# Register your models here.
from .models import Location, EntryDate, ProvinceState, CountryRegion, County
from .models import CaseType, CountEntry, CountIncreaseEntry, CountPercentIncreaseEntry

admin.site.register(Location)
admin.site.register(EntryDate)
admin.site.register(CountEntry)
admin.site.register(CountIncreaseEntry)
admin.site.register(CountPercentIncreaseEntry)
admin.site.register(ProvinceState)
admin.site.register(CountryRegion)
admin.site.register(County)
admin.site.register(CaseType)
