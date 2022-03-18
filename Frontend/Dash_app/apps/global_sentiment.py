import plotly.graph_objects as go
import pandas as pd
import datetime
from logging import exception
from msilib.schema import Error
import traceback
from turtle import color, width

import dash
from dash import dcc, html
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from urllib.request import urlopen
import json
#import requests
import numpy as np
import pandas as pd
import plotly.express as px
import random
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3
import dash
from dash import html, dcc, dash_table
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime
import codecs
# https://github.com/plotly/dash-dangerously-set-inner-html
import dash_dangerously_set_inner_html


project_bucket_name = "cloud-project-bucket-ns-22"



# get_df_sentiment_by_country_streaming = pd.read_csv(
#     "C:/Users/catha/PycharmProjects/finalproject/Frontend/Dash_app/apps/Output_Batman_df_sentiment_by_country_streaming.csv")
# get_df_sentiment_by_category_streaming = pd.read_csv(
#     "C:/Users/catha/PycharmProjects/finalproject/Frontend/Dash_app/apps/Output_Batman_df_sentiment_by_category_streaming.csv")

# total_sentiment = get_df_sentiment_by_country_streaming


# negative_sentiment = get_df_sentiment_by_country_streaming[(get_df_sentiment_by_country_streaming["Sentiment"] < 0)]
# positive_sentiment = get_df_sentiment_by_country_streaming[(get_df_sentiment_by_country_streaming["Sentiment"] > 0)]
# neutral_sentiment = get_df_sentiment_by_country_streaming[(get_df_sentiment_by_country_streaming["Sentiment"] == 0)]
# print(neutral_sentiment.head(5))

# country_json = get_df_sentiment_by_country_streaming.to_json()
# category_json = get_df_sentiment_by_category_streaming.to_json()


# def dataframe_chooser(value):
#     if value == 'total_sentiment':
#         return total_sentiment
#     elif value == 'positive_sentiment':
#         return positive_sentiment
#     elif value == 'negative_sentiment':
#         return negative_sentiment
#     else:
#         return neutral_sentiment


{'label': 'Total Sentiment', 'value': 'total_sentiment'},
{'label': 'Positive Sentiment', 'value': 'positive_sentiment'},
{'label': 'Negative Sentiment', 'value': 'negative_sentiment'},
{'label': 'Neutral Sentiment', 'value': 'neutral_sentiment'}

import dash
import dash_html_components as html

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M
dt_string = now.strftime("%d/%m/%Y %H:%M")

# needed if running single page dash app instead
# external_stylesheets = [dbc.themes.LUX]

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Sentiment Worldwide at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")
        ]),
        # choose between cases or deaths
        dcc.Dropdown(
            id='sentiment_of_interest',
            options=[
                {'label': 'Total Sentiment', 'value': 'total_sentiment'},
                {'label': 'Positive Sentiment', 'value': 'positive_sentiment'},
                {'label': 'Negative Sentiment', 'value': 'negative_sentiment'},
                {'label': 'Neutral Sentiment', 'value': 'neutral_sentiment'},
            ],
            value='cases per 1 mil',
            # multi=True,
            style={'width': '50%'}
        ),
        # for some reason, font colour remains black if using the color option
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='World Heatmap',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
        dbc.Row([
            html.H4('Live Tweet Sentiment Map'),
            html.Div(children=[
                dcc.Graph(id="live-update-sentiment-map"),  # fig_test
            ], style={"border": "2px black solid"}),
            html.Br(),
        ],
            align="center",
        ),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Daily Sentiment by Continent',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Latest update: ' + dt_string, className="text-center"),
                    width=4, className="mt-4"),
            dbc.Col(html.H5(children='Line Graph Visual: ' + dt_string, className="text-center"), width=8,
                    className="mt-4"),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id='pie_cases_or_deaths'), width=4),
            dbc.Col(dcc.Graph(id='line_cases_or_deaths'), width=8)
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Cumulative sentiment by continent',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Latest update: ' + dt_string, className="text-center"),
                    width=4, className="mt-4"),
            dbc.Col(html.H5(children='Cumulative figures: ' + dt_string, className="text-center"), width=8,
                    className="mt-4"),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id='total_pie_cases_or_deaths'), width=4),
            dbc.Col(dcc.Graph(id='total_line_cases_or_deaths'), width=8)
        ]),

        # Update interval for live graphs
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),

        # Stores for data sets
        dcc.Store(id='topic', data="Batman"),
        dcc.Store(id='df-sentiment-by-country'),
        dcc.Store(id='df-sentiment-by-category'),
    ])
])



@app.callback(
    [
        Output('df-sentiment-by-country', 'data'),
        Output('df-sentiment-by-category', 'data'),
    ],
    [
        Input('interval-component', 'n_intervals'),
        Input('df-sentiment-by-country', 'data'),
        Input('topic', 'data'),
    ]
)
def update_data(n_intervals, df_sentiment_by_country_json, topic):

    if df_sentiment_by_country_json is not None:

        df_sentiment_by_country_old = pd.read_json(df_sentiment_by_country_json[0], orient='split')
        print("Saved data...")
        print(df_sentiment_by_country_old.head())

    df = get_df_sentiment_by_country_streaming(topic)
    df_country_json = df.to_json(date_format='iso', orient='split')

    df = get_df_sentiment_by_category_streaming(topic)
    df_category_json = df.to_json(date_format='iso', orient='split')

    return [df_country_json], [df_category_json]

def get_df_sentiment_by_country_streaming(topic):
    if topic is None:
        # Setup blank data frame
        df = pd.DataFrame({
            "Country": pd.Series(dtype='str')
            , "CountryCode": pd.Series(dtype='str')
            , "Sentiment" : pd.Series(dtype='float')
            , "TweetCount" : pd.Series(dtype='int')
        })
        return df
    else:
        df_url = "gs://{}/Output/{}/df_sentiment_by_country_streaming.csv".format(project_bucket_name, topic)
        print(df_url)
        df = pd.read_csv(df_url)
        
        # Set no location on map to antartica and convert country codes to 3 letter versions
        df["Country"].fillna('No Location', inplace=True)
        df["CountryCode"].fillna('AQ', inplace=True)
        df['CountryCode'] = df.CountryCode.apply(lambda x: country_name_to_country_alpha3(country_alpha2_to_country_name(x)))
        print(df.head(10))
        return df
    
def get_df_sentiment_by_category_streaming(topic):
    if topic is None:
        # Setup blank data frame
        df = pd.DataFrame({
            "Sentiment" : pd.Series(dtype='str')
            , "TweetCount" : pd.Series(dtype='int')
        })
        return df
    else:
        # Get data frame for topic from cloud
        df_url = "gs://{}/Output/{}/df_sentiment_by_category_streaming.csv".format(project_bucket_name, topic)
        print(df_url)
        df = pd.read_csv(df_url)
        print(df.head(10))
        return df


# Live update Sentiment map
# @app.callback(Output('live-update-sentiment-map', 'figure'),
#               [
#                   Input('sentiment_of_interest', 'value'),
#               ])
@app.callback(Output('live-update-sentiment-map', 'figure'),
               [
                   Input('interval-component', 'n_intervals'),
                   Input('df-sentiment-by-country', 'data'),
               ])
def live_update_sentiment_map(n, df_json):
    # Parse df
    df = pd.read_json(df_json[0], orient='split')

    #df = dataframe_chooser("total_sentiment")
    # Sentiment map
    colorscale = [
        [0, 'rgb(31,120,180)'],
        [0.35, 'rgb(166, 206, 227)'],
        [0.75, 'rgb(251,154,153)'],
        [1, 'rgb(227,26,28)']
    ]
    fig = px.choropleth(
        df,
        title="Sentiment Map",
        locations="CountryCode",
        color="Sentiment",
        range_color=(-1, 1),
        hover_name="Country",
        labels={'CountryCode': 'Sentiment'},
        color_continuous_scale=px.colors.diverging.RdBu,
        color_continuous_midpoint=0,
    )

    # fig.update_layout(
    #     autosize=False,
    #     margin=dict(l=60, r=60, t=50, b=50, autoexpand=True),
    #     # margin = dict(
    #     #         l=0,
    #     #         r=0,
    #     #         b=0,
    #     #         t=0,
    #     #         pad=4,
    #     #         autoexpand=True
    #     #     ),
    #         width=800,
    #     #     height=400,
    # )
    return fig

