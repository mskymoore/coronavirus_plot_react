import csv, requests
from github import Github


def get_file(csv_url):
    return csv.DictReader(requests.get(csv_url).iter_lines(decode_unicode=True))

county_key = 'county_key'
province_key = 'province_key'
country_key = 'country_key'
lat_key = 'lat_key'
long_key = 'long_key'

global_keys = {
    province_key : 'Province/State',
    country_key : 'Country/Region',
    lat_key : 'Lat',
    long_key : 'Long'
}

us_keys = {
    county_key : 'Admin2',
    province_key : 'Province_State',
    country_key : 'Country_Region',
    lat_key : 'Lat',
    long_key : 'Long_'
}

g = Github("34a2755ef5ef33b83bf7bcf4614a27f6287d5589")
repo = g.get_repo("CSSEGISandData/COVID-19")

confirmed_path_global = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_path_global = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_path_global = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

confirmed_path_us = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
deaths_path_us = "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

confirmed_global = repo.get_contents(confirmed_path_global)
deaths_global = repo.get_contents(deaths_path_global)
recovered_global = repo.get_contents(recovered_path_global)

confirmed_us = repo.get_contents(confirmed_path_us)
deaths_us = repo.get_contents(deaths_path_us)

case_status_type_names = ['confirmed', 'deaths', 'recovered']
csv_global_github_files = [confirmed_global, deaths_global, recovered_global]
csv_us_github_files = [confirmed_us, deaths_us]

csv_global_urls = [github_file.download_url for github_file in csv_global_github_files]
csv_us_urls = [github_file.download_url for github_file in csv_us_github_files]