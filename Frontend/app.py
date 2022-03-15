# pip install dash
# pip install pyorbital

import datetime

import dash
from dash import dcc, html
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from pyorbital.orbital import Orbital

from urllib.request import urlopen
import json
import requests
import numpy as np
import pandas as pd
import plotly.express as px


satellite = Orbital('TERRA')
#external_stylesheets = []
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
#app = JupyterDash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1(id="title_container", children=["Live Tweet Sentiment Map - Please submit a topic..."], style={"text-align": "center"}, ),
        html.Div(dcc.Input(id='input-on-submit', type='text')),
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(id="sentiment_map", figure={}),

        # Sample live graphs
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        #dcc.Graph(id='live-update-map'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ]
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id="title_container", component_property="children"),
        Output(component_id="output_container", component_property="children"),
        Output(component_id="sentiment_map", component_property="figure"),
    ],
    [
        Input("submit-val", "n_clicks"),
        #Input('interval-component', 'n_intervals')
    ]
    ,
    State('input-on-submit', 'value')
)
#def submit_topic(n_clicks, n_intervals, topic):
def submit_topic(n_clicks, topic):
    print(n_clicks)
    print(topic)

    # Update title and info
    title = "Live Tweet Sentiment Map for Topic: '{}'".format(topic)
    container = "The topic chosen by user was: '{}'".format(topic)

    # Get data frame for topic from cloud - this is a sample dataset
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv")
    df_max_scaled = df.copy()
    df_max_scaled["GDP (BILLIONS)"] = df_max_scaled["GDP (BILLIONS)"] /df_max_scaled["GDP (BILLIONS)"].abs().max()

    # Sample map
    fig = px.choropleth(
        df_max_scaled,
        locations="CODE",
        color="GDP (BILLIONS)",
        range_color=(-1, 1),
        labels={'CODE':'GDP (BILLIONS)'},
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
        title="Sentiment Map",
    )

    return title, container, fig


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Latitude': [],
        'Longitude': [],
        'Altitude': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        lon, lat, alt = satellite.get_lonlatalt(
            time
        )
        data['Longitude'].append(lon)
        data['Latitude'].append(lat)
        data['Altitude'].append(alt)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Altitude'],
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Longitude'],
        'y': data['Latitude'],
        'text': data['time'],
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig
    
# --------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(mode="inline")