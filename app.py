import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from StaticFunctions import load_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = load_data()

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['timestamp'],y=df['fat_percentage'],mode='markers'))
fig.update_layout(
    title="Fat Percentage",
    xaxis_title="Date",
    yaxis_title="Fat Percentage"
)

app.layout = html.Div(children=[
    html.H1(children='Body Measurements'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)