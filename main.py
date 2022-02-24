# BOTH SIDES
# Project to aggregate news, assign topic and give sentiment/"spiciness"
# then, for a given topic, display two articles that are oppose to each other

# MVP #
# First:  Aggregate/Scrape news articles
# Second: Store articles and give score
# Third:  Display article on screen
# Fourth: Display two articles on screen
# Fifth:  Display two articles of opposing position on screen
# Re-asses

# Modules to scrape/get news (maybe news-fetch package)
# Module for sentiment analysis, VADER or TextBlob
# Module for web development, maybe Dash or Flask

# Need a way to store the data
# Using NumPy arrays/Pandas could be an option
# Schema for table:
# Headline,
# Article,
# Headline TB polarity Score,
# Headline TB polarity,
# Headline TB subjectivity Score,
# Headline TB subjectivity,
# Headline VS compound Score,
# Headline VS compound,
# Article TB polarity Score,
# Article TB polarity,
# Article TB subjectivity Score,
# Article TB subjectivity,
# Article VS compound Score,
# Article VS compound,


# NewsFetch - newspaper().keyword
# Keywords
# headline
# name(s) of author(s)
# publication date
# publication
# category
# source_domain
# article
# summary
# keyword
# url
# language


# For Vader:
# positive sentiment: compound score >= 0.05
# neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
# negative sentiment: compound score <= -0.05

# For TextBlob:
#   if score < 0:
#     return ‘Negative’
#   elif score == 0:
#     return ‘Neutral’
#   else:
#     return ‘Positive’

from newsfetch.google import google_search
from newsfetch.news import newspaper
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

analyzer = SentimentIntensityAnalyzer()

search = google_search('vladimir putin', 'https://www.bbc.co.uk/news/')

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


# Creating Dataframe of returned data
df = pd.DataFrame(list(zip(list_headline,
                           list_headline_tb_subjectivity,
                           list_headline_tb_polarity,
                           list_headline_vs_subjectivity,
                           list_aricle,
                           list_aricle_tb_subjectivity,
                           list_aricle_tb_polarity,
                           list_aricle_vs_subjectivity)),
                  columns=['headline',
                           'headline_tb_subj',
                           'headline_tb_pola',
                           'headline_vad_sub',
                           'article',
                           'article_tb_subj',
                           'article_tb_pola',
                           'article_vad_sub'])
