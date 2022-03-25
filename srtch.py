# Imports
from newsfetch.google import google_search
from newsfetch.news import newspaper

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


#import numpy as np
#import matplotlib
#import openpyxl


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



search_topic = 'vladimir putin'
news_site = ['BBC NEWS', 'FOX NEWS']

search_function('Positive',search_topic, news_site[0])
search_function('Negative',search_topic, news_site[1])



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


pos_headline = positive_data_query.iat[0,3]
pos_article = positive_data_query.iat[0,7]
pos_comp_score = positive_data_query.iat[0,10]

neg_headline = negative_data_query.iat[0,3]
neg_article = negative_data_query.iat[0,7]
neg_comp_score = negative_data_query.iat[0,10]


print(f'''
        Pos Headline: {pos_headline}
        Pos Comp Score: {pos_comp_score}
        Pos Article: {pos_article}''')

print("##########")

print(f'''
        Pos Headline: {neg_headline}
        Pos Comp Score: {neg_comp_score}
        Pos Article: {neg_article}''')