from django.contrib import admin

# Register your models here.
from .models import Location, HistoricEntry

admin.site.register(Location)
admin.site.register(HistoricEntry)