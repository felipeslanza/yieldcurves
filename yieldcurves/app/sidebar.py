import pandas as pd
import streamlit as st

from . import shared
from .loaders import load_country


__all__ = ("render_sidebar",)


def render_sidebar(target_country: str):
    st.sidebar.subheader("Settings")

    target_country = st.sidebar.text_input("Target country (full name)", value="Brazil")
    load_country(target_country.lower())

    st.sidebar.subheader("Select terms")

    for term in shared.bonds_tickers:
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            shared.bonds_active.remove(term)
