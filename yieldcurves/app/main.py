"""
yieldcurves.app.main
~~~~~~~~~~~~~~~~~~~~

This module controls the app.
"""

import streamlit as st

from yieldcurves import settings
from . import shared
from .loaders import load_country
from .plotting import plot_yield_curve


def run():
    st.legacy_caching.caching.clear_cache()
    st.set_page_config(**settings.ST_PAGE_CONFIG)

    # Layout (pre-data)
    st.sidebar.header("Settings")
    cont0 = st.container()

    # Setup & get data
    target_country = st.sidebar.text_input("Target country (full name)", value="Brazil")
    load_country(target_country.lower())

    # Layout (post-data)
    cont0.subheader(f"Bond yields for [{shared.target_country.title()}]")
    st.sidebar.subheader("Select terms")
    for term in shared.bonds_tickers:
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            shared.bonds_active.remove(term)

    # Content
    plot_yield_curve(shared.bonds_active)
