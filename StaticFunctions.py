import os

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


def load_data():
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

    return df
