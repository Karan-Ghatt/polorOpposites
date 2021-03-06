# Imports
from newsfetch.google import google_search
from newsfetch.news import newspaper

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
import openpyxl

import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__,  external_stylesheets=[dbc.themes.BOOTSTRAP])




df = pd.read_excel('output_2 (version 1).xlsb.xlsx')

sorted_df = df.sort_values(by=['article_vad_comp'])
fig = px.bar(sorted_df, x="headline", y="article_vad_comp", color="article_vad_comp_score", barmode="group")

# Example figure from data
graph = dcc.Graph(
    id='example-graph',
    figure=fig
)



# Search box
search_box = html.Div(
    [
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [dcc.Textarea(
                    id='textarea-state-example',
                    value='Search Topic',
                    style={'width': '100%', 'height': 50},
    ),
    html.Button('Search', id='submit_search', n_clicks=0)]
                ),
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'})
            ]
        )
    ])



# Negative sentiment card
first_card =dbc.Card(
    [
        dbc.CardHeader(f"Polarity Score: {df.iat[0,8]}"),
        dbc.CardBody(
            [
                html.H4(f"{df.iat[0,1]}", className="card-title"),
                html.P(f"{df.iat[0,5]}", className="card-text"),
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={"width": "40rem",
           "height": "30rem",
           "margin-top": "2rem"},
)

# Posative sentiment card
second_card =dbc.Card(
    [
        dbc.CardHeader(f"Polarity Score: {df.iat[7,8]}"),
        dbc.CardBody(
            [
                html.H4(f"{df.iat[7,1]}", className="card-title"),
                html.P(f"{df.iat[7,5]}", className="card-text"),
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={"width": "40rem",
           "height": "30rem",
           "margin-top": "2rem"},
)



# Main body of page
main_body = html.Div(
    [
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4('Positive Sentiment'),
                                html.Hr(),
                                dcc.Dropdown(
                                    id='page2-dropdown',
                                    options=[
                                        {'label': '{}'.format(i), 'value': i} for i in [
                                            'United States', 'Canada', 'Mexico'
                                        ]
                                    ]
                                ),
                                html.Div(id='selected-dropdown'),
                                second_card,
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.H4('Negative Sentiment'),
                                html.Hr(),
                                dcc.Dropdown(
                                    id='page2-buttons',
                                    options=[
                                        {'label': '{}'.format(i), 'value': i} for i in [
                                            'United States', 'Canada', 'Mexico'
                                        ]
                                    ]
                                ),
                                html.Div(id='selected-dropdown-2'),
                                first_card,
                            ],
                            width=6
                        )
                    ]
                ),
            ]
        )
    ])


# App Layout
app.layout = html.Div(children=[
    html.H1(children='Polor Opposites'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    search_box,
    main_body,
])

@app.callback(

    # Search Box
    Output('textarea-state-example-output', 'children'),

    # Drop down 1
    Output("page2-dropdown", "children"),

    # search box
    Input('submit_search', 'n_clicks'),

    # Dropdown
    Input("page2-dropdown", "value"),

    # submit button
    State('textarea-state-example', 'value')
)



def update_output(n_clicks, value, search_value, dd_value):

    if not search_value:
        raise PreventUpdate
    if n_clicks > 0:
        print('Search Topic: \n{}'.format(value))
        print(f'Drop Down: {dd_value}')





if __name__ == '__main__':
    app.run_server(debug=False)





