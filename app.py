import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

from StaticFunctions import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = load_data()

d2 = resample_every_day(df)
d2 = months_to_goal_fat_percentage(goal_percentage=8, df=d2)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['fat_percentage'], mode='markers'))
fig.update_layout(
    title="Fat Percentage",
    xaxis_title="Date",
    yaxis_title="Fat Percentage"
)

f2 = go.Figure()
f2.add_trace(go.Scatter(x=d2.index, y=d2['months_to_goal_percentage'], mode='markers'))
f2.update_layout(
    title="Months To Goal Percentage",
    xaxis_title="Date",
    yaxis_title="Months To Goal Percentage"
)

app.layout = html.Div(children=[
    html.H1(children='Body Measurements'),
    dcc.Graph(
        id='months_fat',
        figure=f2
    ),

    dcc.Graph(
        id='fat_percentage',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
