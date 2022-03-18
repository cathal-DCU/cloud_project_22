from dash import html, dcc, dash_table
#import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Enter your topic of interest", className="card-title"),
            html.P("Then click 'Submit' and start exploring"),
            dcc.Input(id='input-on-submit', type='text', debounce=True, pattern=u"^[a-z]+$",
                      style={'display': 'inline-block'}),
            dbc.Button('Submit', id='submit-val', n_clicks=0, style={'display': 'inline-block'}, color="primary"),
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

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)