from django.db import models
from django.utils import timezone
from hashlib import sha256
import pickle


def create_friendly_name(province, region, county=''):
    if str(province) == '' and str(county) == '':
        return str(region)
    elif str(province) == '':
        return str(county) + ', ' + str(region)
    elif str(county) == '':
        return str(province) + ', ' + str(region)
    else:
        return str(county) + ', ' + str(province) + ', ' + str(region)


def create_hash(friendly_name):
    return sha256(friendly_name.encode()).hexdigest()

class ProvinceState(models.Model):
    province_state = models.CharField(primary_key=True, max_length=100, default='')
    def __str__(self):
        return str(self.province_state)

class CountryRegion(models.Model):
    region_country = models.CharField(primary_key=True,max_length=100, default='')
    def __str__(self):
        return str(self.region_country)

class County(models.Model):
    county = models.CharField(primary_key=True, max_length=100, default='')
    def __str__(self):
        return str(self.county)

class Location(models.Model):
    province_state = models.ForeignKey(ProvinceState, on_delete=models.DO_NOTHING)
    region_country = models.ForeignKey(CountryRegion, on_delete=models.DO_NOTHING)
    county = models.ForeignKey(County, on_delete=models.DO_NOTHING)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=100)
    friendly_hash = models.CharField(max_length=100)
    def __str__(self):
        return self.friendly_name


class HistoricEntry(models.Model):
    date = models.DateField()
    count = models.IntegerField(default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    case_status_type_id = models.CharField(max_length=25)
    def __str__(self):
       return str(self.date) + ':' + str(self.count)