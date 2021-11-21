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

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME])
app = dash.Dash(__name__, external_stylesheets=["./assets/custom.css"])

colors = {
    'background': '#111111',
    'text': '#ffffff'
}

time_fig = generate_figures(colors)
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}
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
    dbc.Row(
        html.H1(
            children='United Jackets',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
    ),
    dbc.Col([
        html.Img(src=app.get_asset_url("rec_garching00048.png")),

    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}),
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
        ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
