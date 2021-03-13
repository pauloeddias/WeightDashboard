from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dateutil import relativedelta

from StaticFunctions import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = load_data()
date_min = df.index[0]
date_max = df.index[-1]

d2 = resample_every_day(df)
d2 = months_to_goal_fat_percentage(goal_percentage=8, df=d2)

weight, fat_percentage, fat_mass, muscle_percentage, muscle_mass, months_to_goal_percentage = make_plots(df, d2)

app.layout = html.Div(children=[
    html.H1(children='Body Measurements',
            style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date_min,
        max_date_allowed=date_max,
        initial_visible_month=datetime.now() - relativedelta.relativedelta(months=3),
        start_date=datetime.now() - relativedelta.relativedelta(months=3),
        end_date=date_max,
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
     dash.dependencies.Output('months_to_goal_percentage', 'figure')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_figure(start_date, end_date):
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    month_df = d2[(d2.index >= start_date) & (d2.index <= end_date)]

    we, fp, fm, mp, mm, mtgp = make_plots(filtered_df, month_df)

    return we, fp, fm, mp, mm, mtgp

if __name__ == '__main__':
    app.run_server(debug=True)
