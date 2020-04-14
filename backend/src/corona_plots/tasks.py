import csv, requests
from .models import Location, EntryDate, create_friendly_name, create_hash
from .models import County, ProvinceState, CountryRegion, CaseType
from .models import CountEntry, CountIncreaseEntry, CountPercentIncreaseEntry
from .coronaVars import county_key, province_key, country_key, lat_key
from .coronaVars import long_key, us_keys, global_keys, csv_global_urls, csv_us_urls
from .coronaVars import get_file, case_status_type_names
from celery import shared_task
from celery.signals import worker_ready
from datetime import datetime as dt
from datetime import timedelta as td
from hashlib import sha256


def get_state_location(locs, state, case_status_type_id):
    state_hash = create_hash(state.province_state)
    if state_hash not in locs:
        state = Location(
            province_state = state,
            friendly_name = state.province_state,
            friendly_hash = state_hash
        )
        state.save()
        state.case_types.add(case_status_type_id)
        return state
    locs[state_hash].case_types.add(case_status_type_id)
    return locs[state_hash]


def get_region_location(locs, region, case_status_type_id):
    region_hash = create_hash(region.region_country)
    if region_hash not in locs:
        region = Location(
            region_country = region,
            friendly_name = region.region_country,
            friendly_hash = region_hash

        )
        region.save()
        region.case_types.add(case_status_type_id)
        return region
    locs[region_hash].case_types.add(case_status_type_id)
    return locs[region_hash]



# csv_file: csv.DictReader
# case_status_type: string, one of ['confirmed', 'deaths', 'recovered']
def update_database(csv_file, case_status_type_id, column_keys, row_start):

    # hashtable the relevant objects for O(1) lookups
    csts = {cst.case_type : cst for cst in  CaseType.objects.all() }


    # if this case status type doesn't exist create it
    if case_status_type_id not in csts:
        case_status_type_id = CaseType(case_type=case_status_type_id)
        case_status_type_id.save()
    # otherwise grab the object from the hash table
    else:
        case_status_type_id = csts[case_status_type_id]


    # for each row in the csv file
    for row in csv_file:
        locs = { loc.friendly_hash: loc for loc in Location.objects.all() }
        province_state = { ps.province_state : ps for ps in ProvinceState.objects.all() }
        country_region = { cr.region_country : cr for cr in CountryRegion.objects.all() }
        counties = { cnty.county : cnty for cnty in County.objects.all() }

        # not all rows have a county entry
        county = None

        # if there is a county key present in the keys sent to this function
        if county_key in column_keys:
            # assign the couny accordingly
            county = row[column_keys[county_key]]

        # otherwise get values from row with keys sent to this function
        province = row[column_keys[province_key]]
        region = row[column_keys[country_key]]
        lat = row[column_keys[lat_key]]
        lon = row[column_keys[long_key]]

        # if there was a county
        if county:
            # include it in the friendly name
            friendly_name = create_friendly_name(province, region, county=county)
        else:
            # don't include it
            friendly_name = create_friendly_name(province, region)

        # create the friendly hash for this location for lookup in hash table
        friendly_hash = create_hash(friendly_name)
        
        # if the region isn't in the region hash table
        if region not in country_region:
            # create it
            region = CountryRegion(region_country=region)
        else:
            # grab it
            region = country_region[region]

        # try to add this case type to the region    
        region.save()
        region.case_types.add(case_status_type_id)
        

        # get or create a location object that is only associated with this region
        region_location = get_region_location(locs, region, case_status_type_id)

        if province != '':
            #if the state isn't in the state hash table
            if province not in province_state:
                # create it
                province = ProvinceState(
                    province_state = province,
                    region_country = region
                )
            else:
                # grab it
                province = province_state[province]


            # try to add this case type to the state
            province.save()
            province.case_types.add(case_status_type_id)
            
            # get or create a location object that is only assicated with this state
            state_location = get_state_location(locs, province, case_status_type_id)
        
        else:
            province = None
            state_location = None

        # if there was a county
        if county:
            # if the county isn't in the county hash table
            if county not in counties:
                # create it
                county = County(
                    county = county,
                    province_state = province,
                    region_country = region
                )
            else:
                # grab it
                county = counties[county]

            # try to add this case type to this county
            county.save()
            county.case_types.add(case_status_type_id)
            

        # if this location not in the hash table of locations
        if friendly_hash not in locs:
            # if there was a county
            if county:
                # create a location with a county
                location = Location(
                    county = county,
                    province_state = province,
                    region_country = region,
                    latitude = lat,
                    longitude = lon,
                    friendly_name = friendly_name,
                    friendly_hash = friendly_hash
                )
            else:
                # create a location with a null county
                location = Location(
                    province_state = province,
                    region_country = region,
                    latitude = lat,
                    longitude = lon,
                    friendly_name = friendly_name,
                    friendly_hash = friendly_hash
                )
        else:
            # grab it
            location = locs[friendly_hash]

        # try to add this case type to this location
        location.save()
        location.case_types.add(case_status_type_id)
        

        # get number entries of this type for this location 
        locations_entries = CountEntry.objects.filter(date__location=location, date__case_status_type_id=case_status_type_id) 
        num_historic_db_entries = len(locations_entries)

        # get all actual entries on this row
        list_row = [ item for item in row.items() ][row_start:]

        # if the number of entries for this row is equal to the number in the database
        if num_historic_db_entries == len(list_row):
            # no new entries, nothing to do
            print('no updates for', case_status_type_id)
            continue 

        one_day = td(days=1)

        # for each new entry
        for entry in list_row[num_historic_db_entries:]:

            the_date = dt.strptime(entry[0], '%m/%d/%y').date()
            previous_date = (dt.strptime(entry[0], '%m/%d/%y') - one_day).date()

            # try to get the previous date of this location for calculations if it exists
            try:
                previous_entry_date = EntryDate.objects.get(
                    date=previous_date,
                    location=location,
                    case_status_type_id=case_status_type_id
                )
                previous_date_count = previous_entry_date.countentry
                divisor = previous_date_count
                if int(divisor) == 0:
                    divisor = 100
            # it doesn't exist, fallback to default values
            except Exception as e:
                print(e)
                previous_date_count = 0
                divisor = 100

            # create a new EntryDate
            date = EntryDate(
                date = the_date,
                location = location,
                case_status_type_id = case_status_type_id
            )
            date.save()

            # crete a new CountEntry
            count_entry = CountEntry(
                date = date,
                value = int(entry[1])
                
            )
            count_entry.save()

            # create a new CountIncreaseEntry
            count_inc_entry = CountIncreaseEntry(
                date = date,
                value =  int(entry[1]) - int(previous_date_count)
            )
            count_inc_entry.save()

            # create a new CountPercentIncreaseEntry
            count_perc_inc_entry = CountPercentIncreaseEntry(
                date = date,
                value = 100*(int(count_inc_entry)/int(divisor))
            )
            count_perc_inc_entry.save()
            
            # if processing a US file
            
            
            # UPDATE STATE
            # get state location associated previous EntryDate object count
            if state_location:
                try:
                    previous_state_date = EntryDate.objects.get(
                        date=previous_date,
                        location=state_location,
                        case_status_type_id=case_status_type_id
                    )
                    previous_state_date_count = previous_state_date.countentry
                    state_divisor = previous_state_date_count
                    if int(state_divisor) == 0:
                        state_divisor = 100
                except Exception as e:
                    print(e)
                    previous_state_date_count = 0
                    state_divisor = 100

                # get or create the current state location EntryDate object
                try:
                    state_date = EntryDate.objects.get(
                        location=state_location,
                        date=date.date,
                        case_status_type_id = case_status_type_id
                        )
                except Exception as e:
                    print(e)
                    state_date = EntryDate(
                        date = the_date,
                        location = state_location,
                        case_status_type_id = case_status_type_id
                    )
                    state_date.save()

                # get and update or create the current state location CountEntry
                try:
                    state_date.countentry.value += count_entry.value
                    state_date.countentry.save()
                except Exception as e:
                    print(e)
                    state_count_entry = CountEntry(
                        date = state_date,
                        value = int(entry[1])

                    )
                    state_count_entry.save()

                # get and update or create the current state location CountIncreaseEntry
                try:
                    state_date.countincreaseentry.value += count_inc_entry.value
                    state_date.countincreaseentry.save()
                    state_inc_entry = state_date.countincreaseentry
                except Exception as e:
                    print(e)
                    state_inc_entry = CountIncreaseEntry(
                        date = state_date,
                        value = count_inc_entry.value
                    )
                    state_inc_entry.save()

                # get and update or create the current state location CountPercentIncreaseEntry
                try:
                    state_date.countpercentincreaseentry.value = 100*(int(state_inc_entry)/int(state_divisor))
                    state_date.countpercentincreaseentry.save()
                except Exception as e:
                    print(e)
                    state_perc_inc_entry = CountPercentIncreaseEntry(
                        date = state_date,
                        value = count_perc_inc_entry.value
                    )
                    state_perc_inc_entry.save()

                # UPDATE REGION
                if not county:
                    try:
                        previous_region_date = EntryDate.objects.get(
                            date=previous_date,
                            location=region_location,
                            case_status_type_id = case_status_type_id
                        )
                        previous_region_date_count = previous_region_date.countentry
                        region_divisor = previous_region_date_count
                        if int(region_divisor) == 0:
                            region_divisor = 100
                    except Exception as e:
                        print(e)
                        previous_region_date_count = 0
                        region_divisor = 100

                    try:
                        region_date = EntryDate.objects.get(
                            location=region_location,
                            date=date.date,
                            case_status_type_id=case_status_type_id
                            )
                    except Exception as e:
                        print(e)
                        region_date = EntryDate(
                            date = the_date,
                            location = region_location,
                            case_status_type_id = case_status_type_id
                        )
                        region_date.save()

                    try:
                        region_date.countentry.value += count_entry.value
                        region_date.countentry.save()
                    except Exception as e:
                        print(e)
                        region_count_entry = CountEntry(
                            date = region_date,
                            value = int(entry[1])
                        )
                        region_count_entry.save()

                    try:
                        region_date.countincreaseentry.value += count_inc_entry.value
                        region_date.countincreaseentry.save()
                        region_inc_entry = region_date.countincreaseentry
                    except Exception as e:
                        print(e)
                        region_inc_entry = CountIncreaseEntry(
                            date = region_date,
                            value = count_inc_entry.value
                        )
                        region_inc_entry.save()

                    try:
                        region_date.countpercentincreaseentry.value = 100*(int(region_inc_entry)/int(region_divisor))
                        region_date.countpercentincreaseentry.save()
                    except Exception as e:
                        print(e)
                        region_perc_inc_entry = CountPercentIncreaseEntry(
                            date = region_date,
                            value = count_perc_inc_entry.value
                        )
                        region_perc_inc_entry.save()


            print('new {status_type} historical entry {num} for {date} {location}'.format(
                status_type=case_status_type_id,
                num=entry[1],
                date=entry[0],
                location=location.friendly_name))


@shared_task
def do_data_update():
    csv_global_files = [get_file(csv_url) for csv_url in csv_global_urls]
    csv_us_files = [get_file(csv_url) for csv_url in csv_us_urls]

    for case_status_type_name, csv_file in zip(case_status_type_names, csv_global_files):
        update_database(csv_file, case_status_type_name, global_keys, 4)

    for case_status_type_name, csv_file in zip(case_status_type_names[:2], csv_us_files):
        if case_status_type_name == 'recovered':
            update_database(csv_file, case_status_type_name, us_keys, 11)
        else:
            update_database(csv_file, case_status_type_name, us_keys, 12)


# @worker_ready.connect
# def update_data(sender=None, conf=None, **kwargs):
#     do_data_update()