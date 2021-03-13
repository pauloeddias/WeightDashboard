from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dateutil import relativedelta

from StaticFunctions import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
global clicks, df, d2
df, d2 = get_dataframes()
clicks = 0

weight, fat_percentage, fat_mass, muscle_percentage, muscle_mass, months_to_goal_percentage = make_plots(df, d2)

app.layout = html.Div(children=[
    html.H1(children='Body Measurements',
            style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
    html.Button('Update', id='submit-val', n_clicks=0, style={'float': 'right'}),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        initial_visible_month=datetime.now() - relativedelta.relativedelta(months=3),
        start_date=datetime.now() - relativedelta.relativedelta(months=3),
        end_date=datetime.now(),
        style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}
    ),
    html.Div([
        dcc.Graph(
            id='weight',
            figure=weight
        ),
        dcc.Graph(
            id='fat_percentage',
            figure=fat_percentage
        ),
        dcc.Graph(
            id='muscle_percentage',
            figure=muscle_percentage
        ),
        dcc.Graph(
            id='fat_mass',
            figure=fat_mass
        ),
        dcc.Graph(
            id='muscle_mass',
            figure=muscle_mass
        ),
        dcc.Graph(
            id='months_to_goal_percentage',
            figure=months_to_goal_percentage,
            style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}
        )
    ],
        style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
    )])


@app.callback(
    [dash.dependencies.Output('weight', 'figure'),
     dash.dependencies.Output('fat_percentage', 'figure'),
     dash.dependencies.Output('fat_mass', 'figure'),
     dash.dependencies.Output('muscle_percentage', 'figure'),
     dash.dependencies.Output('muscle_mass', 'figure'),
     dash.dependencies.Output('months_to_goal_percentage', 'figure'),
     dash.dependencies.Output('months_to_goal_percentage', 'start_date'),
     dash.dependencies.Output('months_to_goal_percentage', 'end_date')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('submit-val', 'n_clicks')])
def update_figure(start_date, end_date, n_clicks):
    global clicks, df, d2
    if n_clicks != clicks:
        clicks = n_clicks
        df, d2 = get_dataframes()
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    month_df = d2[(d2.index >= start_date) & (d2.index <= end_date)]

    we, fp, fm, mp, mm, mtgp = make_plots(filtered_df, month_df)
    sd = df.index[-1] - relativedelta.relativedelta(months=3)
    return we, fp, fm, mp, mm, mtgp, sd, df.index[-1]


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')])
def update_output(n_clicks):
    return f'The button has been clicked {n_clicks} times'


if __name__ == '__main__':
    app.run_server(debug=True)
