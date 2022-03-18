# pip install dash
# pip install fsspec
# pip install gcsfs 
# pip install pycountry_convert

import datetime
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha3

project_bucket_name = "cloud-project-bucket-ns-22"

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
            dcc.Input(id='input-on-submit', type='text', value="Batman", style={'display': 'inline-block'}),
            html.Button('Submit', id='submit-val', n_clicks=0, style={'display': 'inline-block'}),
        ]),
        
        html.Div(id="topic_container"),
        html.Br(),

        # Sample live maps
        html.H4('Live Tweet Sentiment Map'),
        html.Div(children=[
            dcc.Graph(id="live-update-sentiment-map"),
        ], style={"border":"2px black solid"}),
        html.Br(),

        # Tweet breakdown graphs
        html.H4('Tweet Breakdown'),
        html.Div(id='live-update-text'),
        html.Div(children=[
            dcc.Graph(id="live-update-sentiment-category-graph", style={'display': 'inline-block'}),
            dcc.Graph(id="live-update-sentiment-category-graph2", style={'display': 'inline-block'}),
            #dcc.Graph(id="live-update-sentiment-category-graph3", style={'display': 'inline-block'}),
        ], style={"border":"2px black solid"}),
        

        # Update interval for live graphs
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),

        # Stores for data sets
        dcc.Store(id='topic', data='Batman'),
        dcc.Store(id='df-sentiment-by-country'),
        dcc.Store(id='df-sentiment-by-category'),
    ]
)

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


# Live update Sentiment map
@app.callback(Output('live-update-sentiment-map', 'figure'),
               [
                   Input('interval-component', 'n_intervals'),
                   Input('df-sentiment-by-country', 'data'),
               ])
def live_update_sentiment_map(n, df_json):
    # Parse df
    df = pd.read_json(df_json[0], orient='split')

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


# Live update sentiment category pie chart
@app.callback(Output('live-update-sentiment-category-graph', 'figure'),
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
            color_discrete_map={'Neutral':'orange',
                                    'Positive':'green',
                                    'Negative':'red'}
        )
    else:
        return [""]
    
    return fig


# Live update country tweet count bar chart
@app.callback(Output('live-update-sentiment-category-graph2', 'figure'),
              [
                  Input('interval-component', 'n_intervals'),
                  Input('df-sentiment-by-country', 'data'),
              ])
def live_update_sentiment_category_graph2(n, df_json):

    if df_json is not None:
        # Parse df
        df = pd.read_json(df_json[0], orient='split')
        fig = px.bar(
            df, 
            title="Tweets By Country", 
            y="TweetCount", 
            x="Country",
            text_auto='.2s',
            log_y=True
        )
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    else:
        return [""]

    return fig

    
# Main
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(mode="inline")