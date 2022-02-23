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


__all__ = ("load_country",)


@st.cache
def load_country(target_country: str):
    #  df = get_ohlc_yield_history(target_country)
    #  df = df.xs("Close", 1, 1)
    #### TEMP ####
    df = pd.read_pickle(f"/home/fsl/code/yieldcurves/{target_country}.pkl")
    #### TEMP ####

    # Updated shared variables
    if target_country != shared.target_country:
        shared.target_country = target_country
        shared.bonds_df = df
        shared.bonds_tickers = sort_by_term(list(df))
        shared.bonds_terms = get_terms(shared.bonds_tickers)
        shared.bonds_active = set()  # Must re-set active state


def load_active_bonds():
    for term in shared.bonds_tickers:
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            with suppress(KeyError):
                shared.bonds_active.remove(term)
