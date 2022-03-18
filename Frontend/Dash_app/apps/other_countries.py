import plotly.graph_objects as go
import pandas as pd

from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M
dt_string = now.strftime("%d/%m/%Y %H:%M")


def countries_list(df):
    return df['countriesAndTerritories'].unique()
available_countries=countries_list(df)

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Sentiment Worldwide at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")
        ]),
    dcc.Dropdown(
        id='cases_or_deaths',
        options=[
            {'label': 'Total Sentiment', 'value': 'total_sentiment'},
            {'label': 'Positive Sentiment', 'value': 'positive_sentiment'},
            {'label': 'Negative Sentiment', 'value': ''},
            {'label': 'Neutral Sentiment', 'value': ''},
        ],
        value='cases per 1 mil',
        #multi=True,
        style={'width': '50%'}
        ),

        dbc.Row([
            dbc.Col(html.H5(children='Latest update: 7 June 2020', className="text-center"),
                    width=4, className="mt-4"),
            dbc.Col(html.H5(children='Cumulative figures', className="text-center"), width=8,
                    className="mt-4"),
        ]),

    dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Figures by country',
                                 className="text-center text-light bg-dark"), body=True, color="dark")
        , className="mb-4")
        ]),

    dcc.Dropdown(
        id='countries',
        options=[{'label': i, 'value': i} for i in available_countries],
        value=['Sweden', 'Switzerland'],
        multi=True,
        style={'width': '70%', 'margin-left': '5px'}
    ),

    dbc.Row([
        dbc.Col(html.H5(children='Daily figures', className="text-center"),
                className="mt-4"),
    ]),

    dcc.Graph(id=''),

    dbc.Row([
        dbc.Col(html.H5(children='Cumulative figures', className="text-center"),
                className="mt-4"),
    ]),

    dcc.Graph(id='total'),

])


])




# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)