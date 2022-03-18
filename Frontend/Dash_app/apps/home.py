from app import app, server
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Enter your topic of interest", className="card-title"),
            html.P("Then click 'Submit' and start exploring"),
            dcc.Input(id='input-on-submit', type='text', value="eg Batman", style={'display': 'inline-block'}),
            html.Button('Submit', id='submit-val', n_clicks=0, style={'display': 'inline-block'}),
        ]
    )
)

second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("ACCESS THE CODE USED TO BUILD THIS DASHBOARD", className="card-title"),
            dbc.Button("GITHUB", href="https://github.com/cathal-DCU/cloud_project_22", color="primary"),
        ]
    )
)

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Sentiment Explorer dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Explore the sentiment for topics that are of interest to you in real time!!'
                                     )
                    , className="text-center")
            ]
        ),

        dbc.Row([
            dbc.Col(html.H5(children='Insert your topic of interest in the search box below, then explore the breakdown of the topic in the Global Sentiment, US '
                                     'sentiment and Individual country pages. Each map is interactive so check out the sentiment in an individual country by hovering your cursor.')
                    , className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='* please note that specific countries may not show if there has been no tweets with location data for that country in the time period')
                    , className="mb-3")
        ]),
        dbc.Row([
        dbc.Col(first_card, width=8),
        dbc.Col(second_card, width=4),
            ]
        ),

        html.A("Special thanks to Matt Hamm for the Twitter icon above",
               href="https://www.flickr.com/photos/73532212@N00/3344975506")

    ])

])


# ------------------------------------------------------------------------------
# Submit topic
@app.callback(
    [
        Output("topic", "data"),
        Output(component_id="topic_container", component_property="children"),
    ],
    Input("submit-val", "n_clicks"),
    State('input-on-submit', 'value'),
)
def submit_topic(n_clicks, topic):
    print(topic)

    # Kick off topic in cloud - TODO
    clean_topic = topic
    if topic is not None:
        clean_topic = topic.strip()
        if len(clean_topic) == 0:
            clean_topic = None

    container = ["The topic chosen by user was: '{}'".format(topic)]
    return clean_topic, container

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)