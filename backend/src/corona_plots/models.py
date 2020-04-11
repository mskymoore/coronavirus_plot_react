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


class CaseType(models.Model):
    confirmed = 'confirmed'
    deaths = 'deaths'
    recovered = 'recovered'
    case_type_choices =[
        (confirmed, 'confirmed'),
        (deaths, 'deaths'),
        (recovered, 'recovered')
    ]
    case_type = models.CharField(primary_key=True, max_length=100, default=confirmed, choices=case_type_choices)
    def __str__(self):
        return str(self.case_type)

class CountryRegion(models.Model):
    case_types = models.ManyToManyField(CaseType)
    region_country = models.CharField(primary_key=True, max_length=100, default='')
    def __str__(self):
        return str(self.region_country)

class ProvinceState(models.Model):
    case_types = models.ManyToManyField(CaseType)
    province_state = models.CharField(primary_key=True, max_length=100, default='')
    region_country = models.ForeignKey(CountryRegion, related_name='states', null=False, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.province_state)

class County(models.Model):
    case_types = models.ManyToManyField(CaseType)
    county = models.CharField(primary_key=True, max_length=100, default='')
    province_state = models.ForeignKey(ProvinceState, related_name='counties', null=False, on_delete=models.CASCADE)
    region_country = models.ForeignKey(CountryRegion, related_name='counties', null=False, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.county)

class Location(models.Model):
    case_types = models.ManyToManyField(CaseType)
    province_state = models.ForeignKey(ProvinceState, null=True, related_name='locations', on_delete=models.DO_NOTHING)
    region_country = models.ForeignKey(CountryRegion, null=True, related_name='locations', on_delete=models.DO_NOTHING)
    county = models.OneToOneField(County, null=True, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    friendly_name = models.CharField(max_length=100)
    friendly_hash = models.CharField(primary_key=True, max_length=100)
    def __str__(self):
        return self.friendly_name

class EntryDate(models.Model):
    date = models.DateField()
    location = models.ForeignKey(Location, related_name='entries', null=False, on_delete=models.DO_NOTHING)

class Entry(models.Model):
    value = models.IntegerField(default=0)
    case_status_type_id = models.ForeignKey(CaseType, on_delete=models.DO_NOTHING)

    def __str__(self):
       return str(self.date) + ':' + str(self.value)

    def __add__(self, other):
        self.value = self.value + other.value
    
    def __int__(self):
        return int(self.value)


class CountEntry(Entry):
    date = models.OneToOneField(EntryDate, null=False, on_delete=models.DO_NOTHING)
    
class CountIncreaseEntry(Entry):
    date = models.OneToOneField(EntryDate, null=False, on_delete=models.DO_NOTHING)

class CountPercentIncreaseEntry(Entry):
    date = models.OneToOneField(EntryDate, null=False, on_delete=models.DO_NOTHING)
