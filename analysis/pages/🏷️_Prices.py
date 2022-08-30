import streamlit as st
import altair as alt
from utils import get_prices, space

def get_chart(data):
    hover = alt.selection_single(
        fields=['date'],
        nearest=True,
        on='mouseover',
        empty='none',
    )

    lines = (
        alt.Chart(data, title='Evolution of stock closing prices')
        .mark_line()
        .encode(
            x='date',
            y='close',
            color='ticker',
            strokeDash='ticker',
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x='date',
            y='close',
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('date', title='Date'),
                alt.Tooltip('close', title='close (USD)'),
            ],
        )
        .add_selection(hover)
    )

    return (lines + points + tooltips).interactive()


df = get_prices()

st.set_page_config(page_title='Prices')
st.sidebar.markdown("# Prices 🏷️")


st.title('🏷️ Closing price analysis')
all_tickers = df['ticker'].unique()
tickers = st.multiselect('Choose stock tickers to visualize', all_tickers, all_tickers[:3])

space(1)

source = df[df.ticker.isin(tickers)]
chart = get_chart(source)
st.altair_chart(chart, use_container_width=True)