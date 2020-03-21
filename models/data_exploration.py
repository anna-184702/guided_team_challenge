from bpd_api_python_lib import *
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import chart_studio.plotly as py

def plot_data_by_state():
    us_states = pd.read_csv("us_state_list.csv")
    us_state_list = us_states['Abbreviation']
    state_numbers = []
    for state in us_state_list:
        filters = {"state": [state], 
        "site_year": {"min": 2014.0, "max": 2014.08333}}
        eui_dict = histogram(group_by = ["electric_eui"], filters=filters)
        num_buildings = eui_dict['totals']['number_of_matching_buildings']
        state_numbers.append(num_buildings)

    us_states['Count'] = state_numbers

    data = [ dict(
            type='choropleth',
            autocolorscale = False,
            locations = us_states['Abbreviation'],
            z = us_states['Count'].astype(float),
            locationmode = 'USA-states',
            marker = dict(
                line = dict (
                    color = 'rgb(255,255,255)',
                    width = 2
                )
            ),
            colorbar = dict(
                title = "Millions USD"
            )
        ) ]

    layout = dict(
                title = 'Number of buildings in the BPD database by state',
                geo = dict(
                    scope='usa',
                    projection=dict( type='albers usa' ),
                    showlakes = True,
                    lakecolor = 'rgb(255, 255, 255)',
                ),
            )

    fig = dict( data=data, layout=layout )

    py.sign_in('Anna8128', '46zTykSNwaQwgnc6LM7Y')

    py.plot( fig)
