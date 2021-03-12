import os

import gspread
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials


def load_data() -> pd.DataFrame:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['WEIGHT_DASHBOARD_CREDENTIALS_PATH'], scope)

    client = gspread.authorize(creds)
    sheet = client.open('Body Index')

    sheet_instance = sheet.get_worksheet(0)

    data = sheet_instance.get_all_values()
    headers = data.pop(0)

    df = pd.DataFrame(data, columns=headers)
    df = df.iloc[4:, :]
    df['timestamp'] = pd.to_datetime(df['Carimbo de data/hora'])
    df['weight'] = df['Weight'].astype('float64')
    df['fat_percentage'] = df['Fat Percentage'].astype('float64')
    df['muscle_percentage'] = df['Muscle Percentage'].astype('float64')
    df['root_metabolism'] = df['Root Metabolism'].astype('float64')
    df = df[['timestamp', 'weight', 'fat_percentage', 'muscle_percentage', 'root_metabolism']]
    df.set_index('timestamp', inplace=True)

    return df


def resample_every_day(df: pd.DataFrame) -> pd.DataFrame:
    d2 = df.resample('D').first()
    d2.fillna(method='ffill', inplace=True)
    return d2


def get_months_to_goal_percentage(column: pd.Series,percentage:float) -> float:
    # percentage = 15
    model = LinearRegression()
    model.fit(X=np.arange(len(column)).reshape(-1,1),y=column.values.reshape(-1,1))
    x = (percentage-model.intercept_)/model.coef_[0]
    return x/30

def months_to_goal_fat_percentage(goal_percentage: float, df: pd.DataFrame) -> pd.DataFrame:
    df['months_to_goal_percentage'] = df['fat_percentage'].rolling(30,min_periods=30).apply(get_months_to_goal_percentage,args=tuple([goal_percentage]))
    df = df.loc[abs(df['months_to_goal_percentage'])<=20.0]
    return df