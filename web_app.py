import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from newsfetch.google import google_search
from newsfetch.news import newspaper

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import pandas as pd
import sqlalchemy as db


engine = db.create_engine('sqlite://', echo=False)
analyzer = SentimentIntensityAnalyzer()

sentiment_list = []
news_source = []

headlines = []
headlines_tb_subjectivity = []
headlines_tb_polarity = []
headlines_vs_subjectivity = []

articles = []
article_tb_subjectivity = []
article_tb_polarity = []
article_vs_subjectivity = []


def search_function(sentiment, topic, source):

    sources_dict = {
        'BBC NEWS': 'https://www.bbc.co.uk/news/',
        'FOX NEWS': 'https://www.foxnews.com/',
        'CNN': '',
        'CNBC': ''
    }

    search = google_search(topic, sources_dict.get(source))

    posts = search.urls

    for post in posts:
        raw_data = newspaper(post)
        headline = raw_data.headline
        article = raw_data.article


        # Sentiment From Source
        sentiment_list.append(sentiment)

        # News Source
        news_source.append(source)

        blob_headline = TextBlob(headline)
        headlines.append(headline)

        # Textblob Headline
        tb_subjectivity_headline = blob_headline.sentiment.subjectivity
        headlines_tb_subjectivity.append(tb_subjectivity_headline)

        tb_polarity_headline = blob_headline.sentiment.polarity
        headlines_tb_polarity.append(tb_polarity_headline)

        # Vader Headline
        vader_headline_sentiment = analyzer.polarity_scores(headline)
        vader_headline_coupound_score = vader_headline_sentiment.get("compound")
        headlines_vs_subjectivity.append(vader_headline_coupound_score)

        blob_article = TextBlob(article)
        articles.append(article)

        # Textblob article
        tb_subjectivity_article = blob_article.sentiment.subjectivity
        article_tb_subjectivity.append(tb_subjectivity_article)

        tb_polarity_article = blob_article.sentiment.polarity
        article_tb_polarity.append(tb_polarity_article)

        vader_article_sentiment = analyzer.polarity_scores(article)
        vader_article_coupound_score = vader_article_sentiment.get("compound")
        article_vs_subjectivity.append(vader_article_coupound_score)

    # Number of record returned
    number_of_record_returned = len(headlines)
    print(f"{number_of_record_returned} record returned")


    df = pd.DataFrame(list(zip(sentiment_list,
                               news_source,
                               headlines,
                               headlines_tb_subjectivity,
                               headlines_tb_polarity,
                               headlines_vs_subjectivity,
                               articles,
                               article_tb_subjectivity,
                               article_tb_polarity,
                               article_vs_subjectivity)),
                      columns=['sentiment',
                               'news_source',
                               'headline',
                               'headline_tb_subj',
                               'headline_tb_pola',
                               'headline_vad_comp',
                               'article',
                               'article_tb_subj',
                               'article_tb_pola',
                               'article_vad_comp'])

    # Setting headline scores
    def set_headline_tb_subjectivity_score(row):
        if row["headline_tb_subj"] > 0:
            return "positive"
        elif row["headline_tb_subj"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(headline_tb_subjectivity_score=df.apply(set_headline_tb_subjectivity_score, axis=1))

    def set_headline_tb_polarity_score(row):
        if row["headline_tb_pola"] > 0:
            return "positive"
        elif row["headline_tb_pola"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(headline_tb_polarity_score=df.apply(set_headline_tb_polarity_score, axis=1))

    def set_headline_vad_comp_score(row):
        if row["headline_vad_comp"] > 0:
            return "positive"
        elif row["headline_vad_comp"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(headline_vad_comp_score=df.apply(set_headline_vad_comp_score, axis=1))

    # Setting article scores
    def set_article_tb_subjectivity_score(row):
        if row["article_tb_subj"] > 0:
            return "positive"
        elif row["article_tb_subj"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(article_tb_subjectivity_score=df.apply(set_article_tb_subjectivity_score, axis=1))

    def set_article_tb_polarity_score(row):
        if row["article_tb_pola"] > 0:
            return "positive"
        elif row["article_tb_pola"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(article_tb_polarity_score=df.apply(set_article_tb_polarity_score, axis=1))

    def set_article_vad_comp_score(row):
        if row["article_vad_comp"] > 0:
            return "positive"
        elif row["article_vad_comp"] == 0:
            return "neutral"
        else:
            return "negative"

    df = df.assign(article_vad_comp_score=df.apply(set_article_vad_comp_score, axis=1))
    sorted_df = df.sort_values(by=['article_vad_comp'])
    sorted_df.to_sql('results_table', con = engine, if_exists='append')



### CREATING DASH APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])



navbar = html.Header([
                    html.H1("Polor Opposite"),
                ], style={"margin-left": "15px"}
                )



card_six = dbc.Card([
    dbc.CardHeader("Positive Sentiment Source"),
    dbc.CardBody([
        dcc.Dropdown(id='positive_source',
                     style={'color': 'black'},
                     options=[{'label': 'KS', 'value': '1'},
                                {'label': 'OH', 'value': '2'},
                                {'label': 'NJ', 'value': '3'},
                                ],
                     value='')
    ])
])

card_one = dbc.Card([
    dbc.CardHeader("Negative Sentiment Source"),
    dbc.CardBody([
        dcc.Dropdown(id='negative_source',
                     style={'color': 'black'},
                     options=[{'label': '415', 'value': '415'},
                              {'label': '408', 'value': '408'},
                              {'label': '510', 'value':'510'},
                              ],
                     value='')
    ])
])

card_five = dbc.Card([
    dbc.CardHeader("Search Topic"),
    dbc.CardBody([
        dcc.Input(id='search_topic', value='10', type="search")
    ])
])




output_card = dbc.Card([
    dbc.CardHeader("Positive Sentiment"),
    dbc.CardBody([
        html.Div(id="my_output")]
    )],
    color="white",
    inverse=False,
    className="w-75 mb-3")


output_card_2 = dbc.Card([
    dbc.CardHeader("Negative Sentiment"),
    dbc.CardBody([
        html.Div(id="my_output_2")]
    )],
    color="dark",
    inverse=False,
    className="w-75 mb-3")


app.layout = html.Div([

    html.Div([navbar]),

    html.Br(),

    html.Center([
        dbc.Row([
            dbc.Col(card_six, width="auto"),
            dbc.Col(card_one, width="auto"),
            dbc.Col(card_five, width="auto")
        ], justify="center")
    ]),

    html.Br(),

    html.Center([
        dbc.Row([
            dbc.Col(dbc.Button("Analyse", id='button', n_clicks=None)),
            dbc.Col(dbc.Button('Reset', id='reset_button', n_clicks=0))
        ])
    ]),

    html.Br(),

    html.Center([
        dbc.Row([
            dbc.Col(output_card),
            dbc.Col(output_card_2)])
    ]),

])

@app.callback(
    [
        Output(component_id='my_output', component_property='children'),
        Output(component_id='my_output_2', component_property='children')
    ],
    [
        Input(component_id='positive_source', component_property='value'),
        Input(component_id='negative_source', component_property='value'),
        Input(component_id='search_topic', component_property='value'),

        Input(component_id='button', component_property='n_clicks')
    ]
)

def update_output_div(positive_source, negative_source, search_topic,
                      n):

    if n > 0:

        print(f"Positive Source: {positive_source}")
        print(f"Negative Source: {negative_source}")
        print(f"Search Topic: {search_topic}")

        # TESTING TOPICS AND SOURCES
        search_topic = 'Kanye West'
        news_site = ['BBC NEWS', 'FOX NEWS']

        # MAIN FUNC
        search_function('Positive', search_topic, news_site[0])
        search_function('Negative', search_topic, news_site[1])

        positive_data_query = pd.read_sql(
            f"""
        SELECT * FROM
        results_table
        WHERE news_source = '{str(news_site[0])}'
        AND article_vad_comp = (SELECT MAX(article_vad_comp) 
                                FROM results_table
                                WHERE news_source = '{str(news_site[0])}' )
        LIMIT 1
        """, engine)
        print('POSITIVE')
        print(positive_data_query)

        negative_data_query = pd.read_sql(
            f"""
        SELECT * FROM
        results_table
        WHERE news_source = '{str(news_site[1])}'
        AND article_vad_comp = (SELECT MIN(article_vad_comp) 
                                FROM results_table
                                WHERE news_source = '{str(news_site[1])}')
        LIMIT 1
        """, engine)
        print('NEGATIVE')
        print(negative_data_query)



        # selecting single value from df


        return f"Output: {positive_data_query}", f"Output 2: {negative_data_query}"
    else:
        raise PreventUpdate






@app.callback(Output('button','n_clicks'),
             [Input('reset_button','n_clicks')])
def update(reset):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)