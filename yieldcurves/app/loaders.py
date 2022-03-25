"""
yieldcurves.app.loaders
~~~~~~~~~~~~~~~~~~~~~~~

This module defines data loaders to be used by the app.
"""

from contextlib import suppress

import pandas as pd
import streamlit as st

from yieldcurves.data_handlers import get_ohlc_yield_history
from yieldcurves.utils import get_terms, sort_by_term
from . import shared


__all__ = ("load_active_bonds", "load_country")


def load_active_bonds():
    # monthly_count = 0
    for term in shared.bonds_tickers:
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # TODO: unselect vertices when multiple monthly issuances are available
        # if "m" in term:
        #     monthly_count += 1
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            with suppress(KeyError):
                shared.bonds_active.remove(term)


def _reset_shared(target_country: str, df: pd.DataFrame):
    shared.target_country = target_country
    shared.bonds_df = df
    shared.bonds_tickers = sort_by_term(list(df))
    shared.bonds_terms = get_terms(shared.bonds_tickers)
    shared.bonds_active = set()  # Must reset active state


def load_country(target_country: str):
    df = get_ohlc_yield_history(target_country)
    if df is None:
        _reset_shared(target_country, pd.DataFrame())
    else:
        df = df.xs("close", 1, 1)
        if target_country != shared.target_country:
            _reset_shared(target_country, df)
