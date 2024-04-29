# app.py
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from collections import deque


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=100,  # Fast enough to avoid flickering, adjust based on performance
        n_intervals=0
    )
])

# Adjust size based on how much data you want to show at once
X = deque(maxlen=20)
Y = deque(maxlen=20)


@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph_scatter(n):
    print(f"X: {X} Y: {Y}")  # Debugging line
    if len(X) == 0 or len(Y) == 0:
        raise PreventUpdate
    data = go.Scatter(x=list(X), y=list(Y), mode='lines+markers')
    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                yaxis=dict(range=[min(Y), max(Y)]),
                                title="Real-time Cumulative Rewards")}


if __name__ == '__main__':
    app.run_server(debug=True)
