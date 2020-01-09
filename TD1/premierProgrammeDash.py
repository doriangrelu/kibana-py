# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

colors = {'background': '#111111', 'text': '#7FDBFF'}

# Un namespace Dash vers les polices CSS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# L'application dash qui agira comme un serveur local
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Le layout de l'application
# C'est un document html basique
app.layout = html.Div(children=[
    html.H1(children='Hello Miage',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),

    html.Div(children='''
        Dash: Un framework python pour visualisation web
        ''',
             style={
                 'textAlign': 'center'
             }
             ),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Aix'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Marseille'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'plot_bgcolor': colors['background'], 'paper_bgcolor': colors['background'],
                'font': {'color': colors['text']}
            }
        }
    )
]
    , style={'backgroundColor': colors['background']}
)

# On execute le serveur
# Le resultat est visible dans votre navigateur a l'adresse http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run_server(debug=True)
