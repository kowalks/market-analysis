import logging
import pandas as pd
import time
import subprocess
from pipelines import prices_pipeline, tickers_pipeline, exchanges_pipeline


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    exchanges_pipeline()

    # NOTE: Polygon API only work for 5 requests/minute, so we are limiting for only 2 tickers
    tickers = ['AAPL', 'GOOGL']

    for ticker in tickers:
        prices_pipeline(ticker)
        tickers_pipeline(ticker)
    
    subprocess.run(['streamlit', 'run', 'analysis/📈_Home.py'])
