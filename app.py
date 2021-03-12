from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dateutil import relativedelta

from StaticFunctions import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = load_data()
date_min = df.index[0]
date_max = df.index[-1]

d2 = resample_every_day(df)
d2 = months_to_goal_fat_percentage(goal_percentage=8, df=d2)

fat_percentage = make_line_plot(x=df.index, y=df['fat_percentage'], title='Fat Percentage', xaxis_title='Date',
                                yaxis_title="Fat Percentage")
muscle_percentage = make_line_plot(x=df.index, y=df['muscle_percentage'], title='Muscle Percentage', xaxis_title='Date',
                                   yaxis_title="Muscle Percentage")
months_to_goal_percentage = make_line_plot(x=d2.index, y=d2['months_to_goal_percentage'], mode='markers',
                                           title='Months To Goal Percentage', xaxis_title='Date',
                                           yaxis_title="Months To Goal Percentage")
fat_mass = make_line_plot(x=df.index, y=df['fat_mass'], title='Fat Mass', xaxis_title='Date',
                          yaxis_title="Fat Mass (Kg)")
muscle_mass = make_line_plot(x=df.index, y=df['muscle_mass'], title='Muscle Mass', xaxis_title='Date',
                             yaxis_title="Muscle Mass (Kg)")

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
    [dash.dependencies.Output('fat_percentage', 'figure'),
     dash.dependencies.Output('fat_mass', 'figure'),
     dash.dependencies.Output('muscle_percentage', 'figure'),
     dash.dependencies.Output('muscle_mass', 'figure'),
     dash.dependencies.Output('months_to_goal_percentage', 'figure')],
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])
def update_figure(start_date=date_min, end_date=date_max):
    filtered_df = df[(df.index >= start_date) & (df.index <= end_date)]
    month_df = d2[(d2.index >= start_date) & (d2.index <= end_date)]

    fp = make_line_plot(x=filtered_df.index, y=filtered_df['fat_percentage'], title='Fat Percentage',
                        xaxis_title='Date',
                        yaxis_title="Fat Percentage")
    mp = make_line_plot(x=filtered_df.index, y=filtered_df['muscle_percentage'], title='Muscle Percentage',
                        xaxis_title='Date',
                        yaxis_title="Muscle Percentage")
    fm = make_line_plot(x=filtered_df.index, y=filtered_df['fat_mass'], title='Fat Mass', xaxis_title='Date',
                        yaxis_title="Fat Mass (Kg)")
    mm = make_line_plot(x=filtered_df.index, y=filtered_df['muscle_mass'], title='Muscle Mass', xaxis_title='Date',
                        yaxis_title="Muscle Mass (Kg)")
    mtgp = make_line_plot(x=month_df.index, y=month_df['months_to_goal_percentage'], mode='markers',
                          title='Months To Goal Percentage', xaxis_title='Date',
                          yaxis_title="Months To Goal Percentage")

    return fp, fm, mp, mm, mtgp


if __name__ == '__main__':
    app.run_server(debug=True)
