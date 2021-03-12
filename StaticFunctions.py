import pandas as pd


def load_data():
    df = pd.read_html(
        'https://docs.google.com/spreadsheets/d/1UdohGMcpFfyhzNRt2qo6Jngj0t_yF5hOXL83TQcEAU8/edit?usp=sharing')
    df = df[0][['A', 'B', 'C', 'D', 'E']]
    data_hora = df['A'].tolist()[5:]
    weight = df['B'].tolist()[5:]
    fat_perc = df['C'].tolist()[5:]
    musc_perc = df['D'].tolist()[5:]
    rm = df['E'].tolist()[5:]

    df = pd.DataFrame(
        {
            'timestamp': data_hora,
            'weight': weight,
            'fat_percentage': fat_perc,
            'muscle_percentage': musc_perc,
            'root_metabolism': rm
        },
    )
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['weight'] = df['weight'].astype('float64')
    df['fat_percentage'] = df['fat_percentage'].astype('float64')
    df['muscle_percentage'] = df['muscle_percentage'].astype('float64')
    df['root_metabolism'] = df['root_metabolism'].astype('float64')
    return df
