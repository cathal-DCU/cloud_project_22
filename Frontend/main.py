# pip install dash
# pip install pyorbital
# pip install fsspec
# pip install gcsfs 
# pip install pycountry_convert

import datetime
from logging import exception
from msilib.schema import Error
import traceback
from turtle import color

import dash
from dash import dcc, html
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from urllib.request import urlopen
import json
import requests
import numpy as np
import pandas as pd
import plotly.express as px
import random
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3

project_bucket_name = "cloud-project-bucket-ns-22"

#from pyorbital.orbital import Orbital
#satellite = Orbital('TERRA')
#external_stylesheets = []
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)
#app = JupyterDash(__name__)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1(id="title_container", children=["Live Update Tweet Sentiment Map"], style={"text-align": "center"}, ),
        
        html.H2('Enter a topic...'),
        html.Div(children=[
            dcc.Input(id='input-on-submit', type='text', style={'display': 'inline-block'}),
            html.Button('Submit', id='submit-val', n_clicks=0, style={'display': 'inline-block'}),
        ]),
        
        
        html.Div(id="topic_container"),
        html.Br(),

        # Sample live maps
        html.H4('Live Tweet Sentiment Map'),
        #dcc.Graph(id="sentiment_map", figure={}),
        html.Div(children=[
            dcc.Graph(id="live-update-sentiment-map"),
        ], style={"border":"2px black solid"}),
        html.Br(),

        # Tweet breakdown graphs
        html.H4('Tweet Breakdown'),
        html.Div(id='live-update-text'),
        #dcc.Graph(id='live-update-sentiment-category-graph'),
        html.Div(children=[
            dcc.Graph(id="live-update-sentiment-category-graph", style={'display': 'inline-block'}),
            dcc.Graph(id="live-update-sentiment-category-graph2", style={'display': 'inline-block'}),
        ], style={"border":"2px black solid"}),
        
        # # Sample live graphs
        # html.H4('TERRA Satellite Live Feed'),
        
        # dcc.Graph(id='live-update-graph'),
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
    Output(component_id="topic_container", component_property="children"),
    Input("submit-val", "n_clicks"),
    State('input-on-submit', 'value'),
)
def submit_topic(n_clicks, topic):
    print(topic)

    # Kick off topic in cloud - TODO
    # if n_clicks == 1:
    container = ["The topic chosen by user was: '{}'".format(topic)]
    return container


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-sentiment-map', 'figure'),
              Input('interval-component', 'n_intervals'),
              State('input-on-submit', 'value'))
def live_update_sentiment_map(n, topic):

    # Setup blank data frame
    df = pd.DataFrame({
        "Country": pd.Series(dtype='str')
        , "CountryCode": pd.Series(dtype='str')
        , "Sentiment" : pd.Series(dtype='float')
        , "TweetCount" : pd.Series(dtype='int')
    })

    #if topic is not None and n == 1:
    if topic is not None:
        try:
            # Get data frame for topic from cloud - this is a sample dataset
            #df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv")
            #df = pd.read_csv("gs://{}/Output/{}/2014_world_gdp_with_codes.csv".format(project_bucket_name, topic))
            #df.rename(columns={"GDP (BILLIONS)" : "Sentiment", "CODE" : "CountryCode", "COUNTRY" : "Country"}, inplace=True)
            df_url = "gs://{}/Output/{}/df_sentiment_by_country_streaming.csv".format(project_bucket_name, topic)
            print(df_url)
            df = pd.read_csv(df_url)
            
            # Set no location on map and convert country codes to 3 letter versions
            #df = df.copy()
            df["Country"].fillna('No Location', inplace=True)
            df["CountryCode"].fillna('AQ', inplace=True)
            df['CountryCode'] = df.CountryCode.apply(lambda x: country_name_to_country_alpha3(country_alpha2_to_country_name(x)))
            print(df.head(10))
            
            # To Show updates for testing
            #df_sentiment_map["Sentiment"] = df_sentiment_map["Sentiment"] * random.uniform(-1, 1) / df_sentiment_map["Sentiment"].abs().max()

        except Exception as e:
            print("Error accessing data..." + traceback.format_exc())

    # Sentiment map
    fig = px.choropleth(
        df,
        title="Sentiment Map",
        locations="CountryCode",
        color="Sentiment",
        range_color=(-1, 1),
        labels={'CountryCode':'Sentiment'},
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
    )
    #fig.update_geos(fitbounds="locations")

    return fig



@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'),
              State('input-on-submit', 'value'))
def update_metrics(n, topic):
    
    tweet_count = 0
    date = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    if topic is not None:
        try:
             # Get data frame for topic from cloud
            df_url = "gs://{}/Output/{}/df_sentiment_by_category_streaming.csv".format(project_bucket_name, topic)
            print(df_url)
            df = pd.read_csv(df_url)

            # Update tweet count
            tweet_count = df['TweetCount'].sum()
        except Exception as e:
            print("Error getting data..." + traceback.format_exc())

    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Last Update: {}'.format(date), style=style),
        html.Span('Tweet Count: {}'.format(tweet_count), style=style),
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-sentiment-category-graph', 'figure'),
              Input('interval-component', 'n_intervals'),
              State('input-on-submit', 'value'))
def live_update_sentiment_category_graph(n, topic):

    # Setup blank data frame
    df = pd.DataFrame({
        "Sentiment" : pd.Series(dtype='str')
        , "TweetCount" : pd.Series(dtype='int')
    })

    if topic is not None:
        try:
            # Get data frame for topic from cloud
            df_url = "gs://{}/Output/{}/df_sentiment_by_category_streaming.csv".format(project_bucket_name, topic)
            print(df_url)
            df = pd.read_csv(df_url)

        except Exception as e:
            print("Error accessing data..." + traceback.format_exc())

    #fig = px.pie(df, x="Sentiment", y="TweetCount", color="Sentiment", title="Sentiment Category Count")
    fig = px.pie(
        df, 
        title="Sentiment By Category", 
        values="TweetCount", 
        names="Sentiment", 
        color="Sentiment", 
        color_discrete_map={'Neutral':'orange',
                                 'Positive':'green',
                                 'Negative':'red'}
    )
    return fig



# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-sentiment-category-graph2', 'figure'),
              Input('interval-component', 'n_intervals'),
              State('input-on-submit', 'value'))
def live_update_sentiment_category_graph2(n, topic):

    # Setup blank data frame
    df = pd.DataFrame({
        "Country": pd.Series(dtype='str')
        , "CountryCode": pd.Series(dtype='str')
        , "Sentiment" : pd.Series(dtype='float')
        , "TweetCount" : pd.Series(dtype='int')
    })

    if topic is not None:
        try:
            # Get data frame for topic from cloud
            df_url = "gs://{}/Output/{}/df_sentiment_by_country_streaming.csv".format(project_bucket_name, topic)
            print(df_url)
            df = pd.read_csv(df_url)
            #print(df.head())
            df["Country"].fillna('No Location', inplace=True)
            df["CountryCode"].fillna('AQ', inplace=True)
            df['CountryCode'] = df.CountryCode.apply(lambda x: country_name_to_country_alpha3(country_alpha2_to_country_name(x)))

        except Exception as e:
            print("Error accessing data..." + traceback.format_exc())

    #fig = px.pie(df, x="Sentiment", y="TweetCount", color="Sentiment", title="Sentiment Category Count")
    fig = px.bar(
        df, 
        title="Tweets By Country", 
        y="TweetCount", 
        x="Country",
        text_auto='.2s',
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    return fig





# # Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(n):
#     satellite = Orbital('TERRA')
#     data = {
#         'time': [],
#         'Latitude': [],
#         'Longitude': [],
#         'Altitude': []
#     }

#     # Collect some data
#     for i in range(180):
#         time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
#         lon, lat, alt = satellite.get_lonlatalt(
#             time
#         )
#         data['Longitude'].append(lon)
#         data['Latitude'].append(lat)
#         data['Altitude'].append(alt)
#         data['time'].append(time)

#     # Create the graph with subplots
#     fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
#     fig['layout']['margin'] = {
#         'l': 30, 'r': 10, 'b': 30, 't': 10
#     }
#     fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

#     fig.append_trace({
#         'x': data['time'],
#         'y': data['Altitude'],
#         'name': 'Altitude',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)
#     fig.append_trace({
#         'x': data['Longitude'],
#         'y': data['Latitude'],
#         'text': data['time'],
#         'name': 'Longitude vs Latitude',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 2, 1)

#     return fig

    
# --------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(mode="inline")