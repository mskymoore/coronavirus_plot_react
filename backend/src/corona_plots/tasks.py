import csv, requests
from .models import Location, HistoricEntry, create_friendly_name, create_hash
from .models import County, ProvinceState, CountryRegion, CaseType
from .coronaVars import global_province_key, global_country_key, csv_global_urls 
from .coronaVars import global_lat_key, global_long_key
from .coronaVars import us_county_key, us_province_key, us_country_key, csv_us_urls
from .coronaVars import us_lat_key, us_long_key
from .coronaVars import get_file, case_status_type_names
from celery import shared_task
from celery.signals import worker_ready
from datetime import datetime as dt
from hashlib import sha256
from .methods import get_plots


# csv_file: csv.DictReader
# case_status_type: string, one of ['confirmed', 'deaths', 'recovered']
def update_database_global(csv_file, case_status_type_id):

    locs = { loc.friendly_hash: loc for loc in Location.objects.all() }
    province_state = { ps.province_state : ps for ps in ProvinceState.objects.all() }
    country_region = { cr.region_country : cr for cr in CountryRegion.objects.all() }
    county = { cnty.county : cnty for cnty in County.objects.all() }

    # DEBUG
    row_num = 0

    for row in csv_file:
        # DEBUG
        if row_num == 5:
            break
        province = row[global_province_key]
        region = row[global_country_key]
        lat = row[global_lat_key]
        lon = row[global_long_key]

        friendly_name = create_friendly_name(province, region)
        friendly_hash = create_hash(friendly_name)
        
        if friendly_hash not in locs:
            location = Location(
                province_state = province,
                region_country = region,
                latitude = lat,
                longitude = lon,
                friendly_name = friendly_name,
                friendly_hash = friendly_hash
            )
            location.save()
        else:
            location = locs[friendly_hash]

        locations_entries = HistoricEntry.objects.filter(location_id=location, case_status_type_id=case_status_type_id) 
        num_historic_db_entries = len(locations_entries)
        
        list_row = [ item for item in row.items() ][4:]

        if num_historic_db_entries == len(list_row):
            # no new entries, nothing to do
            print('no updates for', case_status_type_id)
            break 

        for entry in list_row[num_historic_db_entries:]:
            HistoricEntry(
                date = dt.strptime(entry[0], '%m/%d/%y').strftime('%Y-%m-%d'),
                location = location,
                count = int(entry[1]),
                case_status_type_id = case_status_type_id
            ).save()
            print('new {status_type} historical entry {num} for {date} {location}'.format(
                status_type=case_status_type_id,
                num=entry[1],
                date=entry[0],
                location=location.friendly_name))
        # DEBUG
        row_num = row_num + 1


# csv_file: csv.DictReader
# case_status_type: string, one of ['confirmed', 'deaths', 'recovered']
def update_database_us(csv_file, case_status_type_id):

    locs = { loc.friendly_hash: loc for loc in Location.objects.all() }
    province_state = { ps.province_state : ps for ps in ProvinceState.objects.all() }
    country_region = { cr.region_country : cr for cr in CountryRegion.objects.all() }
    counties = { cnty.county : cnty for cnty in County.objects.all() }
    csts = {cst.case_type : cst for cst in  CaseType.objects.all() }

    if case_status_type_id not in csts:
        case_status_type_id = CaseType(case_type=case_status_type_id)
        case_status_type_id.save()
    # DEBUG
    row_num = 0

    for row in csv_file:
        # DEBUG
        
        county = row[us_county_key]
        province = row[us_province_key]
        region = row[us_country_key]
        lat = row[us_lat_key]
        lon = row[us_long_key]


        friendly_name = create_friendly_name(province, region, county=county)
        friendly_hash = create_hash(friendly_name)
        
        if county not in counties:
            county = County(county=county)
            county.save()
        
        if province not in province_state:
            province = ProvinceState(province_state=province)
            province.save()
        
        if region not in country_region:
            region = CountryRegion(region_country=region)
            region.save()


        if friendly_hash not in locs:
            location = Location(
                county = county,
                province_state = province,
                region_country = region,
                latitude = lat,
                longitude = lon,
                friendly_name = friendly_name,
                friendly_hash = friendly_hash
            )
            location.save()
        else:
            location = locs[friendly_hash]

        locations_entries = HistoricEntry.objects.filter(location=location, case_status_type_id=case_status_type_id) 
        num_historic_db_entries = len(locations_entries)
        
        list_row = [ item for item in row.items() ][12:]

        if num_historic_db_entries == len(list_row):
            # no new entries, nothing to do
            print('no updates for', case_status_type_id)
            break 

        for entry in list_row[num_historic_db_entries:]:
            HistoricEntry(
                date = dt.strptime(entry[0], '%m/%d/%y').strftime('%Y-%m-%d'),
                location = location,
                count = int(entry[1]),
                case_status_type_id = case_status_type_id
            ).save()
            print('new {status_type} historical entry {num} for {date} {location}'.format(
                status_type=case_status_type_id,
                num=entry[1],
                date=entry[0],
                location=location.friendly_name))
        # DEBUG
        row_num = row_num + 1


@shared_task
def do_data_update():
    csv_global_files = [get_file(csv_url) for csv_url in csv_global_urls]
    csv_us_files = [get_file(csv_url) for csv_url in csv_us_urls]
    
    #for case_status_type_name, csv_file in zip(case_status_type_names, csv_global_files):
    #    update_database_global(csv_file, case_status_type_name)

    for case_status_type_name, csv_file in zip(case_status_type_names[:2], csv_us_files):
        update_database_us(csv_file, case_status_type_name)
    

@worker_ready.connect
def update_data(sender=None, conf=None, **kwargs):
    do_data_update()