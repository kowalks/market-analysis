import pandas as pd
import sqlalchemy

import streamlit as st

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write('')

def get_prices():
    engine = sqlalchemy.create_engine('sqlite:///db/market.db')
    df = pd.read_sql('select * from prices', con=engine)
    df = df.drop_duplicates()
    df = df.pivot(index=['ticker', 'date'], columns=['variable'], values='value')
    df = df.reset_index()
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_tickers():
    engine = sqlalchemy.create_engine('sqlite:///db/market.db')
    df = pd.read_sql('select * from tickers', con=engine)
    df = df.drop_duplicates()
    return df

def get_exchanges():
    engine = sqlalchemy.create_engine('sqlite:///db/market.db')
    df = pd.read_sql('select * from exchanges', con=engine)
    df = df.drop_duplicates()
    return df