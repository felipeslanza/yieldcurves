import plotly.express as px
import streamlit as st

from . import shared
from .sidebar import render_sidebar
from yieldcurves.utils import sort_tickers


def run():
    st.set_page_config(layout="wide")

    # Layout
    cont0 = st.container()

    # Setup & get data
    render_sidebar(shared.target_country)
    cont0.subheader(f"Bond yields for {shared.target_country.title()}")

    # Content
    if shared.bonds_active:
        active_tickers = sort_tickers(shared.bonds_active)
        df = shared.bonds_df[active_tickers]
        data = df.tail(5).T

        fig = px.line(data, width=1300, height=700)
        st.plotly_chart(fig)
