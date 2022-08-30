import json
import logging
import pandas as pd
from etl import LoadDB, HTTPConnector, DBConnector, Transform, ExtractHTTP
from credentials import API_KEY

def transform_operation(content, **kwargs):
    content = json.loads(content)

    records = [content['results']]
    df = pd.DataFrame.from_records(records)

    # NOTE:  Dropping unsupported columns. In the real world, we should transform
    # this columns into strings or use a database that supports JSON (for example PostgreSQL)
    df = df.drop(columns=['address', 'branding', 'ticker_suffix'], errors='ignore')

    return df


def tickers_pipeline(ticker='AAPL'):
    """ETL Pipeline for tickers
    
    Pipeline for ingestion on Polygon API to get price data. It consists of three steps:
        - Extract step: extracts from Polygon API raw data
        - Transform step: transforms raw data into a Pandas DataFrame
        - Load step: loads the pandas dataframe into the projected Databrase
    """
    
    logging.info(f'Price pipeline for {ticker}') 

    url = f'https://api.polygon.io/v3/reference/tickers/{ticker}'
    params = {
        'apiKey': API_KEY
    }
    
    with HTTPConnector() as session:
        extract = ExtractHTTP().run(url, session, params=params)

    transform = Transform(transform=transform_operation).run(extract)
    
    table = 'tickers'
    with DBConnector() as conn:
        load = LoadDB(table).run(transform, conn)

    return load