import plotly.graph_objects as go
import pandas as pd

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
            html.H5("Top 25 most common words", className="card-title"),
            dbc.Row([
                dbc.Col(html.Img(src="/assets/image_three.png")),
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
            html.H5("Wordcloud of most common words", className="card-title"),
            dbc.Row([
                dbc.Col(html.Img(src="/assets/image_four.png")),
                # dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-2")),
            ],
                align="center",
            ),
        ]
    )
)

third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Proportion of Tweets by country", className="card-title"),
            dbc.Row([
                dbc.Col(html.Img(src="/assets/image_one.png")),
                # dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-2")),
            ],
                align="center",
            ),
        ]
    )
)


fourth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Analysis of sentiment per category", className="card-title"),
            dbc.Row([
                dbc.Col(html.Img(src="/assets/image_two.png")),
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
            dbc.Col(dbc.Card(html.H3(children='Most commonly tweeted words',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='* after removal of stopwords and non-standard characters')
                    , className="mb-5")
        ]),
    dbc.Row([
        dbc.Col(first_card, width=8),
        dbc.Col(second_card, width=4),
            ]
        ),

    dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Tweet Breakdown',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-4")
        ]),
    dbc.Row([
        dbc.Col(third_card, width=6),
        dbc.Col(fourth_card, width=6),
            ]
        ),

    dbc.Row([
        # dbc.Col(dcc.Graph(id='total_pie_cases_or_deaths'), width=4),
        # dbc.Col(dcc.Graph(id='total_line_cases_or_deaths'), width=8)
    ]),
])
])

# page callbacks
# display pie charts and line charts to show number of cases or deaths
# @app.callback()
"""
@app.callback([Output('pie_cases_or_deaths', 'figure'),
               Output('line_cases_or_deaths', 'figure'),
               Output('total_pie_cases_or_deaths', 'figure'),
               Output('total_line_cases_or_deaths', 'figure')],
              [Input('cases_or_deaths', 'value')])
"""

def update_graph(choice):

    fig = go.Figure(data=[
        go.Pie(labels=df3['continentExp'], values=df3[choice])
        ])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=0))

    dff = df2.copy()
    dff = pd.pivot_table(dff, values=choice, index=['date'], columns='continentExp')

    fig2 = go.Figure()
    for col in dff.columns:
        fig2.add_trace(go.Scatter(x=dff.index, y=dff[col].values,
                                 name=col,
                                 mode='markers+lines'))

    fig2.update_layout(yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    fig3 = go.Figure(data=[
        go.Pie(labels=df4.index, values=df4[choice])
        ])

    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    dff2 = df5.copy()
    dff2 = pd.pivot_table(dff2, values=choice, index=['date'], columns='continentExp')

    fig4 = go.Figure()
    for col in dff2.columns:
        fig4.add_trace(go.Scatter(x=dff2.index, y=dff2[col].values,
                                 name=col,
                                 mode='markers+lines'))

    fig4.update_layout(yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    return fig, fig2, fig3, fig4