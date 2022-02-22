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
    # Config
    st.legacy_caching.caching.clear_cache()
    st.set_page_config(**settings.ST_PAGE_CONFIG)

    # Layout (pre-data)
    st.sidebar.header("Settings")
    cont0 = st.container()

    # Setup & load data
    target_country = st.sidebar.text_input("Country (full name)", value="Brazil").lower()
    load_country(target_country)

    # Layout (post-data)
    cont0.subheader(f"Bond yields for [{shared.target_country.title()}]")
    st.sidebar.subheader("Select terms")
    for term in shared.bonds_tickers:
        val = st.sidebar.checkbox(term, value=True)
        if val:
            shared.bonds_active.add(term)
        else:
            shared.bonds_active.remove(term)

    #### TEMP ####
    #### TEMP ####

    # Content
    plot_yield_curve(
        active_bonds=shared.bonds_active,
        # active_dates=shared.selected_dates,
        # ++++++++++++++++++++++++++++++++++++++++++++++
        active_dates=["2022-2-17", "2022-1-27"],  # TEMP
        # ++++++++++++++++++++++++++++++++++++++++++++++
    )
