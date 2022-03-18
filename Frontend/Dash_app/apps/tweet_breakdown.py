import plotly.graph_objects as go
import pandas as pd

import dash
from dash import html, dcc, dash_table
# import dash_core_components as dcc
# import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from app import app
from datetime import datetime
import codecs
# https://github.com/plotly/dash-dangerously-set-inner-html
import dash_dangerously_set_inner_html

"""
dbc.Row([
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML(
        open("assets/world.html", 'r')),
    ]),
dbc.Row([
    dbc.Col(dbc.Card(html.H3(children='Daily sentiment by continent',
                             className="text-center text-light bg-dark"), body=True, color="dark")
    , className="mt-4 mb-4")
]),
"""

import dash
import dash_html_components as html
import base64

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M
dt_string = now.strftime("%d/%m/%Y %H:%M")
#image_filename = 'image_one.png' # replace with your own image
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#app.layout = html.Div([
#    html.Img(src='data:image/png;base64,{}'.format(encoded_image))
#])

# change to app.layout if running as single page app instead
first_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                html.H4('Live Tweet Sentiment Breakdown'),
                html.Div(children=[
                    dcc.Graph(id="live-update-sentiment-category-graph3"),  # fig_test
                ], style={"border": "2px black solid"}),
                html.Br(),
                # dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-2")),
            ],
                align="center",
            ),
        ]
    )
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                html.H4('Current Volume of Tweets'),
                html.Div(children=[
                    dcc.Graph(id="live-update-text"),  # fig_test
                ], style={"border": "2px black solid"}),
                html.Br(),
                # dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-2")),
            ],
                align="center",
            ),
        ]
    )
)


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Analysis of Tweets'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising the metadata of tweets'), className="mb-4")
        ]),

# for some reason, font colour remains black if using the color option
    dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Overall Tweet Sentiment',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),

    dbc.Row([
        dbc.Col(first_card, width=8),
        dbc.Col(second_card, width=4),
            ]
        ),
])
])


# Live update sentiment category pie chart
@app.callback(Output('live-update-sentiment-category-graph3', 'figure'),
              [
                  Input('interval-component', 'n_intervals'),
                  Input('df-sentiment-by-category', 'data'),
              ])
def live_update_sentiment_category_graph(n, df_json):
    if df_json is not None:
        # Parse df
        df = pd.read_json(df_json[0], orient='split')
        fig = px.pie(
            df,
            title="Sentiment By Category",
            values="TweetCount",
            names="Sentiment",
            color="Sentiment",
            color_discrete_map={'Neutral': 'orange',
                                'Positive': 'green',
                                'Negative': 'red'}
        )
    else:
        return [""]

    return fig


# Sample metrics with number of tweets and current date from last update
@app.callback(Output('live-update-text', 'children'),
              [
                  Input('interval-component', 'n_intervals'),
                  Input('df-sentiment-by-category', 'data'),
              ])
def update_metrics(n, df_json):
    tweet_count = 0
    if df_json is not None:
        # Parse df
        df = pd.read_json(df_json[0], orient='split')
        # Update tweet count
        tweet_count = df['TweetCount'].sum()
    date = datetime.datetime.now().strftime('%d/%m/%Y - %H:%M:%S')
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Last Update: {}'.format(date), style=style),
        html.Span('Tweet Count: {:,}'.format(tweet_count), style=style),
    ]

