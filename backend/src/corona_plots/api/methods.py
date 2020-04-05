from .coronaVars import case_status_type_names
from .models import Location, HistoricEntry
import plotly.offline as po
import plotly.express as px

def generate_percent_growth_series(y_axis_cases):
    
    y_axis_percent_growth = [0]
    for i in range(len(y_axis_cases))[1:]:
        if y_axis_cases[i-1] == 0:
            divisor = 100
        else:
            divisor = y_axis_cases[i-1]
        y_axis_percent_growth.append(((y_axis_cases[i] - y_axis_cases[i-1])/divisor)*100)
    
    return y_axis_percent_growth


def generate_series(series_type, location):
    entries = HistoricEntry.objects.filter(location=location,case_status_type_id=series_type).order_by('date')
    x_axis_cases = []
    y_axis_cases = []
    for entry in entries:
        x_axis_cases.append(str(entry.date))
        y_axis_cases.append(int(entry.count))

    y_axis_growth = [y_axis_cases[0]]
    for i in range(len(entries))[1:]:
        y_axis_growth.append(y_axis_cases[i] - y_axis_cases[i-1])
    
    y_axis_percent_growth = generate_percent_growth_series(y_axis_cases)

    
    return {
        'x_axis' : x_axis_cases,
        'cases' : y_axis_cases,
        'growth' : y_axis_growth,
        'percent_growth' : y_axis_percent_growth
    }


def generate_graph_div(series, series_type):
    x_axis_cases = series['x_axis']
    y_axis_cases = series['cases']
    y_axis_growth = series['growth']
    y_axis_percent_growth = series['percent_growth']

    fig_line = px.line(x=x_axis_cases, y=y_axis_cases, title=f'{series_type} cases', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} cases'})
    line_graph_div = po.plot(fig_line, auto_open=False, output_type="div", include_plotlyjs=False)
        
    fig_bar = px.bar(x=x_axis_cases, y=y_axis_growth, title=f'{series_type} growth', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} growth'})
    bar_graph_div = po.plot(fig_bar, auto_open=False, output_type="div", include_plotlyjs=False)

    fig_bar_perc = px.bar(x=x_axis_cases, y=y_axis_percent_growth, title=f'{series_type} percent growth', template="plotly_dark", labels={'x': 'date', 'y':f'{series_type} percent growth'})
    bar_perc_graph_div = po.plot(fig_bar_perc, auto_open=False, output_type="div", include_plotlyjs=False)

    return line_graph_div + bar_perc_graph_div + bar_graph_div


def plots2(request):
    location = request.GET['location']
    locations = Location.objects.filter(province_state=location).all()
    location_series = {}
    
    for sublocation in locations:
        location_series[sublocation.friendly_hash] = { series_type : generate_series(series_type, sublocation) for series_type in case_status_type_names[:2] }
    
    location_sum_series = {}

    for series_type in case_status_type_names[:2]:
        x_axis = location_series[next(iter(location_series))][series_type]['x_axis']
        y_axis_cases = [ 0 for i in x_axis ]
        y_axis_growth = y_axis_cases.copy()

        for sublocation in location_series:

            for i, count in enumerate(location_series[sublocation][series_type]['cases']):
                y_axis_cases[i] = y_axis_cases[i] + count

            for i, count in enumerate(location_series[sublocation][series_type]['growth']):
                y_axis_growth[i] = y_axis_growth[i] + count
            
        y_axis_percent_growth = generate_percent_growth_series(y_axis_cases)
            

        location_sum_series[series_type] = {
            'x_axis' : x_axis,
            'cases' : y_axis_cases,
            'growth' : y_axis_growth,
            'percent_growth' : y_axis_percent_growth
        }