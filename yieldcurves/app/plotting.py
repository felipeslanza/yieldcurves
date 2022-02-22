"""
yieldcurves.app.plotting
~~~~~~~~~~~~~~~~~~~~~~~~

This module defines plotting helpers to be used in the app.
"""

import logging

import numpy as np
import plotly.express as px
import streamlit as st

from yieldcurves.utils import get_terms, get_tickvals, sort_by_term
from yieldcurves import settings
from . import shared
from .loaders import load_country


__all__ = ("plot_yield_curve",)


logger = logging.getLogger(__name__)


def plot_yield_curve(active_bonds: list):
    sorted_tickers = sort_by_term(active_bonds)
    tickvals = get_tickvals(shared.bonds_terms)

    data = shared.bonds_df[sorted_tickers]
    # ++++++++++++++++++++++++++++++++++++
    data = data.tail(3).T  # (!) Temporary
    # ++++++++++++++++++++++++++++++++++++
    data.columns = data.columns.strftime(settings.DATE_FORMAT)
    data.index = tickvals
    data = data.reindex(np.arange(1, tickvals[-1] + 1))  # Reindex to longest mty

    fig = px.scatter(data, width=1300, height=700)
    fig.update_layout(
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=get_terms(sorted_tickers),
        )
    )
    st.plotly_chart(fig)
