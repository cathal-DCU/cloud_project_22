import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M
dt_string = now.strftime("%d/%m/%Y %H:%M")


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Sentiment per U.S. state at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the United States'), className="mb-4")
        ]),

# for some reason, font colour remains black if using the color option
    dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='U.S. States Heatmap',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
    dbc.Row([
            dbc.Col(html.Img(src="/assets/us_states.html", height="75px")),
            #dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-2")),
                    ],
                    align="center",
                ),

    dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Daily Sentiment by US State',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
    dbc.Row([
        dbc.Col(html.H5(children='Number of Tweets per State: '+dt_string, className="text-center"),
                         width=4, className="mt-4"),
        dbc.Col(html.H5(children='Number of Tweets per State Line Graph: '+dt_string, className="text-center"), width=8, className="mt-4"),
        ]),



        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Cumulative sentiment by state',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Latest update: '+dt_string, className="text-center"),
                    width=4, className="mt-4"),
            dbc.Col(html.H5(children='Cumulative figures: '+dt_string, className="text-center"), width=8,
                    className="mt-4"),
        ]),

    dbc.Row([

    ]),
])
])

