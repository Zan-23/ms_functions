# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import State
from dash_bootstrap_components import Input
from dash_html_components import Output

from data_preparation import generate_figures

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])
# app = dash.Dash(__name__, external_stylesheets=["./assets/custom.css"])

colors = {
    'background': '#111111',
    'text': '#ffffff'
}

time_fig = generate_figures(colors)

card_group = dbc.CardGroup([
    dbc.Card(
        dbc.CardBody([
                html.H5("Defected images 24h", className="card-title"),
                html.P("12%", className="card-text"),
            ])
    ),
    dbc.Card(
        dbc.CardBody([
                html.H5("7 day rolling average", className="card-title"),
                html.P("5%", className="card-text"),
        ])
    )],className="mt-4 shadow",
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    dbc.NavbarSimple(
        brand="United Jackets Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
        style={'margin-bottom': '25px', 'text-transform': "uppercase"},
        className="g-0"
    ),
    dbc.Col([
        #   "rec_garching00048.png"
        html.Img(src=app.get_asset_url("rec_test.jfif"),
                 style={'width': '500px', 'display': 'inline-block', 'vertical-align': 'top'}),

    ], style={'width': '39%', 'display': 'inline-block', 'vertical-align': 'top'}),
    dbc.Col(
        [
            # dbc.Row(
            #     html.Div(children='Dash: A web application framework for your data.', style={
            #         'textAlign': 'center',
            #         'color': colors['text']
            #     })
            # ),
            dbc.Row(
                dcc.Graph(
                    id='example-graph-2',
                    figure=time_fig,
                    animate=True
                )
            ),
            dbc.Col([card_group]),
        ], style={'width': '59%', 'display': 'inline-block', 'vertical-align': 'top'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
