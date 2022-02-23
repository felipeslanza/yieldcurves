"""
yieldcurves.app.plotting
~~~~~~~~~~~~~~~~~~~~~~~~

This module defines plotting helpers to be used in the app.
"""

import logging
from datetime import datetime
from typing import List, Union

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from yieldcurves.utils import get_terms, get_tickvals, sort_by_term
from yieldcurves import settings
from . import shared


__all__ = ("plot_yield_curve",)


logger = logging.getLogger(__name__)

# Globals
# ----
COLORS = px.colors.qualitative.Plotly


def plot_yield_curve(
    active_bonds: List[str],
    active_dates: List[Union[str, datetime]],
):
    sorted_tickers = sort_by_term(active_bonds)
    terms = get_terms(sorted_tickers)
    tickvals = get_tickvals(terms)

    data = shared.bonds_df.loc[active_dates, sorted_tickers].T
    data.index = tickvals
    data = data.reindex(np.arange(1, tickvals[-1] + 1))  # Reindex to longest mty
    max_tick = tickvals[-1] + 12 if "Y" in shared.bonds_terms[-1] else 1

    fig = go.Figure(
        layout=dict(
            height=700,
            width=1300,
            xaxis=dict(
                title="Terms",
                tickmode="array",
                tickvals=tickvals,
                ticktext=terms,
                range=[0, max_tick],
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                title="Yield %",
                showgrid=False,
            ),
        )
    )

    for i, (date, series) in enumerate(data.iteritems()):
        color = COLORS[i]

        # Add valid points
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series,
                mode="lines+markers",
                name=date.strftime(settings.DATE_FORMAT),
                marker=dict(color=color),
            )
        )

        # Add interpolated curve
        try:
            method = shared.interpolation_method
            curve = series.interpolate(method=method)
        except ValueError as e:
            logger.error("Not enough data for method {method}. Using `quadratic` instead")
            curve = series.interpolate(method="quadratic")

        fig.add_trace(
            go.Scatter(
                x=curve.index,
                y=curve,
                line=dict(width=0.75, color=color),
                showlegend=False,
            )
        )

    st.plotly_chart(fig)
