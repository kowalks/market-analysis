import datetime
import json
import logging
import pandas as pd
from etl import LoadDB, HTTPConnector, DBConnector, Transform, ExtractHTTP
from credentials import API_KEY

def transform_operation(content, **kwargs):
    content = json.loads(content)

    records = content['results']
    df = pd.DataFrame.from_records(records)
    cols = {
        'c': 'close',
        'h': 'high',
        'l': 'low',
        'n': 'transactions',
        'o': 'open',
        't': 'date',
        'v': 'volume',
        'vw': 'vwap'
    }
    df = df.rename(columns=cols)
    for k,v in kwargs.items():
        df[k] = v

    ids = ['ticker', 'date']
    variables = ['close', 'high', 'low', 'transactions', 'open', 'volume', 'vwap']
    df = df.melt(id_vars=ids, value_vars=variables)
    df['date'] = pd.to_datetime(df['date'], unit='ms')

    return df


def prices_pipeline(ticker='AAPL', initial_date=datetime.date(2020,1,1), end_date=None):
    """ETL Pipeline for prices
    
    Pipeline for ingestion on Polygon API to get price data. It consists of three steps:
        - Extract step: extracts from Polygon API raw data
        - Transform step: transforms raw data into a Pandas DataFrame
        - Load step: loads the pandas dataframe into the projected Databrase
    """
    if not end_date:
        end_date = datetime.date.today()
    
    logging.info(f'Price pipeline for {ticker} from {initial_date} to {end_date}')

    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{initial_date}/{end_date}'
    params = {
        'adjusted': 'true',
        'apiKey': API_KEY
    }
    
    with HTTPConnector() as session:
        extract = ExtractHTTP().run(url, session, params=params)

    transform = Transform(transform=transform_operation).run(extract, ticker=ticker)
    
    table = 'prices'
    with DBConnector() as conn:
        load = LoadDB(table).run(transform, conn)

    return load