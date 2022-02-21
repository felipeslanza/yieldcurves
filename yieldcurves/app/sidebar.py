import pandas as pd
import streamlit as st

from yieldcurves.data_handlers import get_ohlc_yield_history
from yieldcurves.utils import sort_tickers
from . import shared


__all__ = ("render_sidebar",)


def render_sidebar(target_country: str):
    st.sidebar.subheader("Settings")

    target_country = st.sidebar.text_input("Target country (full name)")

    # Trigger `shared` update
    if target_country != shared.target_country:
        # df = get_ohlc_yield_history(target_country)
        # df = df.xs("Close", 1, 1)

        #### TEMP ####
        df = pd.read_pickle("/home/fsl/code/yieldcurves/temp.pkl")
        #### TEMP ####

        # Updated shared variables
        shared.target_country = target_country
        shared.bonds_df = df
        shared.bonds_tickers = sort_tickers(list(df))

    st.sidebar.subheader("Select issuances")

    for term in shared.bonds_tickers:
        print("---> ", term, shared.bonds_active)
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            shared.bonds_active.remove(term)
