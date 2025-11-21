import dash
import dash_cytoscape as cyto
from dash import html, dcc

app = dash.Dash(__name__)

# Convertit votre topologie en éléments Cytoscape
elements = [
    {'data': {'id': 'R1', 'label': 'Routeur 1'}},
    {'data': {'id': 'R2', 'label': 'Routeur 2'}},
    {'data': {'source': 'R1', 'target': 'R2', 'label': '10.0.2.0/30'}}
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='network-graph',
        elements=elements,
        style={'width': '100%', 'height': '600px'},
        layout={'name': 'cose'}
    ),
    dcc.Interval(id='refresh', interval=5000)
])

if __name__ == '__main__':
    app.run_server(debug=True)