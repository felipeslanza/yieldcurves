import streamlit as st

from yieldcurves.data_handlers import get_ohlc_yield_history
from . import shared


__all__ = ("render_sidebar",)


def render_sidebar(target_country: str):
    st.sidebar.subheader("Settings")

    target_country = st.sidebar.text_input("Target country (full name)")

    # Trigger `shared` update
    if target_country != shared.target_country:
        df = get_ohlc_yield_history(target_country)
        df = df.xs("Close", 1, 1)

        # Updated shared variables
        shared.target_country = target_country
        shared.bonds_df = df
        shared.bonds_tickers = sorted(df)
        # shared.bonds_tickers = sorted(df.columns.get_level_values(0).unique())

    st.sidebar.subheader("Select issuances")

    for term in shared.bonds_tickers:
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            shared.bonds_active.remove(term)
