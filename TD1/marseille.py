# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import csv

if __name__ == '__main__':
    # Les trois tableaux qui vont nous servir pour afficher le graphique
    tempsMax = []
    tempsMin = []
    dates = []

    # on ouvre le csv/json/txt et on recupere les valeurs que l'on stocke dans ces tableaux
    with open("meteoMarseille2018.csv", "r") as infile:
        lines = csv.DictReader(infile, delimiter=",", lineterminator="\n")
        headers = lines.fieldnames

        for line in lines:
            dates.append(line[headers[0]])
            tempsMax.append(float(line[headers[1]]))
            tempsMin.append(float(line[headers[2]]))

    # Les namespace Dash
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # Le layout qui sera affiche
    app.layout = html.Div(children=[
        html.H1(children='La météo en 2018'),
        dcc.Graph(
            id='graphe_meteo_marseille',
            figure={
                'data': [
                    {'x': dates, 'y': tempsMax, 'mode': 'lines', 'name': 'Orange', 'line': {'color': '#F07200'}},
                    {'x': dates, 'y': tempsMin, 'mode': 'lines', 'name': 'Bleu', 'line': {'color': '#1D96D3'}}
                ],
                'layout': {
                    'title': u'Evolution des températures à Marseille en 2018',
                    # TODO
                    # Il faut enlever tous les ticks sur l'axe des X
                    # Pour cela, il faut ajouter un tableau de tickvals et un tableau avec des ticktext
                    'xaxis': {"showgrid": False, "gridcolor": "#00B050", "tickvals": [], "ticktexts": []},

                    # TODO
                    # Il faudrait pouvoir avoir un tick tout les 5 degres et aller de -5 a 35 degres
                    # Il faut que les axes -5 et +35 soient visibles egalement
                    # Il faut jouer sur les attributs range, ticks, tick0, dtick
                    # La ligne sur l'axe du zero devrait pouvoir s'enlever aussi
                    'yaxis': {}
                }
            }
        )
    ])
    app.run_server(debug=True)
