# https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599

from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
from app import server
from app import app, server
# import all pages in the app
from apps import global_sentiment, us_sentiment, home, other_countries, tweet_breakdown

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("Global Sentiment", href="/global_sentiment"),
        #dbc.DropdownMenuItem("US sentiment", href="/sentiment_usa"),
        #dbc.DropdownMenuItem("Other countries", href="/sentiment_other"),
        #dbc.DropdownMenuItem("Overall Tweet Breakdown", href="/tweet_breakdown"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/twitter_logo.jpg", height="75px"), style={"margin-right": "22rem"}),
                        dbc.Col(dbc.NavbarBrand("Sentiment Explorer", className="ml-5",style ={'width':'26vH','height':'80px'})),
                    ],
                    align="center",
                ),
                href="/home",
            ),

            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,style={"margin-left": "22rem"}
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/global_sentiment':
        return global_sentiment.layout
    elif pathname == '/sentiment_usa':
        return us_sentiment.layout
    elif pathname == '/sentiment_other':
        return other_countries.layout
    elif pathname == '/tweet_breakdown':
        return tweet_breakdown.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True) # port=5500