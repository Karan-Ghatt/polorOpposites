# Imports
from newsfetch.google import google_search
from newsfetch.news import newspaper

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
import openpyxl


import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

analyzer = SentimentIntensityAnalyzer()

# def my_function(topic, news site):
# for each news site, search topic
# and save results in dataframe



search = google_search('Kanye West', 'https://www.foxnews.com/')


posts = search.urls



list_headline = []

list_headline_tb_subjectivity = []
list_headline_tb_polarity = []
list_headline_vs_subjectivity = []

list_aricle = []

list_aricle_tb_subjectivity = []
list_aricle_tb_polarity = []
list_aricle_vs_subjectivity = []




for post in posts:

    raw_data = newspaper(post)
    headline = raw_data.headline
    article = raw_data.article

    blob_headline = TextBlob(headline)
    list_headline.append(headline)
    
    # Textblob Headline
    tb_subjectivity_headline = blob_headline.sentiment.subjectivity
    list_headline_tb_subjectivity.append(tb_subjectivity_headline)
    
    tb_polarity_headline = blob_headline.sentiment.polarity
    list_headline_tb_polarity.append(tb_polarity_headline)
    
    # Vader Headline
    vader_headline_sentiment = analyzer.polarity_scores(headline)
    vader_headline_coupound_score = vader_headline_sentiment.get("compound")
    list_headline_vs_subjectivity.append(vader_headline_coupound_score)


    
    
    blob_article = TextBlob(article)
    list_aricle.append(article)
    
    # Textblob article
    tb_subjectivity_article = blob_article.sentiment.subjectivity
    list_aricle_tb_subjectivity.append(tb_subjectivity_article)
    
    tb_polarity_article = blob_article.sentiment.polarity
    list_aricle_tb_polarity.append(tb_polarity_article)
    
    vader_article_sentiment = analyzer.polarity_scores(article)
    vader_article_coupound_score = vader_article_sentiment.get("compound")
    list_aricle_vs_subjectivity.append(vader_article_coupound_score)

   


# Number of record returned
number_of_record_returned = len(list_headline)
print(f"{number_of_record_returned} record returned")


# In[9]:


df = pd.DataFrame(list(zip(list_headline, 
                            list_headline_tb_subjectivity, 
                            list_headline_tb_polarity,
                            list_headline_vs_subjectivity, 
                            list_aricle, 
                            list_aricle_tb_subjectivity, 
                            list_aricle_tb_polarity, 
                            list_aricle_vs_subjectivity)),
                   columns = ['headline', 
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
fig = px.bar(sorted_df, x="headline", y="article_vad_comp", color="article_vad_comp_score", barmode="group")

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5(f"Headline {sorted_df.iat[0,0]}", className="card-title"),
            html.P(f"Headline {sorted_df.iat[0,4]}"),
        ]
    )
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This card also has some text content and not much else, but "
                "it is twice as wide as the first card."
            ),
            dbc.Button("Go somewhere", color="primary"),
        ]
    )
)

graph = dcc.Graph(
        id='example-graph',
        figure=fig
    ),


app.layout = html.Div(children=[
    html.H1(children='Polor Opposites'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),



    dbc.Row([
        dbc.Col(first_card, width=5),
        dbc.Col(second_card, width=5),
    ]),

    dbc.Row([
        graph
    ]),


])

if __name__ == '__main__':
    app.run_server(debug=False)





