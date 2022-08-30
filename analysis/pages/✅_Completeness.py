import streamlit as st
import pandas as pd

from utils import get_prices, get_tickers, get_exchanges

st.set_page_config(page_title='Completeness', page_icon="✅", layout='wide')
st.markdown('''

# Completeness ✅

In this page, we visually inspect data to get insights on how to use them. 
Below we have our three tables with its content. The prices dataframe is
pivoted, so we can get all variables for a single date/ticker.

''')


prices = get_prices()
st.markdown("## 1. Prices dataframe")
st.dataframe(prices)

tickers = get_tickers()
st.markdown("## 2. Tickers dataframe")
st.dataframe(tickers)

exchanges = get_exchanges()
st.markdown("## 3. Exchanges dataframe")
st.dataframe(exchanges)
