import plotly.express as px
import streamlit as st

from . import shared
from .sidebar import render_sidebar


def run():
    st.set_page_config(layout="wide")

    render_sidebar(shared.target_country)

    if shared.bonds_active:
        df = shared.bonds_df[shared.bonds_active]
        fig = px.scatter(df.iloc[-1])
        st.plotly_chart(fig)
