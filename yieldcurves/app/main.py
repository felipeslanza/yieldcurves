import numpy as np
import plotly.express as px
import streamlit as st

from . import shared
from .sidebar import render_sidebar
from yieldcurves.utils import get_tickvals, sort_tickers


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
        tickvals = get_tickvals(active_tickers)

        data = shared.bonds_df[active_tickers]
        # ++++++++++++++++++++++++++++++++++++
        data = data.tail(3).T  # (!) Temporary
        # ++++++++++++++++++++++++++++++++++++
        data.index = tickvals
        data = data.reindex(np.arange(1, tickvals[-1] + 1))  # Reindex to longest mty

        fig = px.scatter(data, width=1300, height=700)
        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=tickvals,
                ticktext=active_tickers,
            )
        )
        st.plotly_chart(fig)
