import logging

import numpy as np
import plotly.express as px
import streamlit as st

from yieldcurves.utils import get_tickvals, sort_by_term
from . import shared


__all__ = ("plot_yield_curve",)


logger = logging.getLogger(__name__)


def plot_yield_curve():
    if not shared.bonds_active:
        logger.error("No data to plot")
    else:
        active_tickers = sort_by_term(shared.bonds_active)
        tickvals = get_tickvals(shared.bonds_terms)

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
