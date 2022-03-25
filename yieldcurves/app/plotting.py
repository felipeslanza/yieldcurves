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
from streamlit.delta_generator import DeltaGenerator

from yieldcurves.utils import get_terms, get_tickvals, interpolate_curve, sort_by_term
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
    container: DeltaGenerator,
):
    sorted_tickers = sort_by_term(active_bonds)
    terms = get_terms(sorted_tickers)
    tickvals = get_tickvals(terms)

    idx = shared.bonds_df.index
    for i, date in enumerate(active_dates):
        if date not in idx:
            logger.warning(f"{date} not found in index. Stepping to closest date.")
            try:
                new_date = idx[idx.searchsorted(date)].strftime(settings.DATE_FORMAT)
            except IndexError:
                new_date = idx[-1].strftime(settings.DATE_FORMAT)
            active_dates[i] = new_date

    data = shared.bonds_df.loc[active_dates, sorted_tickers].T
    data.index = tickvals
    data = data.reindex(np.arange(1, tickvals[-1] + 1))  # Reindex to longest mty
    max_tick = tickvals[-1] + 12 if "y" in shared.bonds_terms[-1] else 1

    fig = go.Figure(
        layout=dict(
            margin=dict(l=10, r=40, t=25, b=15),
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
                zeroline=False,
            ),
            legend=dict(
                yanchor="bottom",
                y=0.03,
                xanchor="right",
                x=0.98,
                bordercolor="#d3d3d3",
                borderwidth=1,
            ),
        )
    )

    for i, (date, series) in enumerate(data.iteritems()):
        color = COLORS[i]

        # Add valid points
        fig.add_trace(
            go.Scatter(
                x=series.index,
                y=series.values,
                mode="lines+markers",
                name=date.strftime(settings.DATE_FORMAT),
                marker=dict(color=color),
            )
        )

        # Add interpolated curve
        curve = interpolate_curve(series, method=shared.interpolation_method)
        if curve is not None:
            fig.add_trace(
                go.Scatter(
                    x=curve.index,
                    y=curve.values,
                    line=dict(width=0.75, color=color),
                    showlegend=False,
                )
            )

    container.subheader("Yield curve")
    container.plotly_chart(fig, use_container_width=True)
