"""
yieldcurves.app.main
~~~~~~~~~~~~~~~~~~~~

This module controls the app.
"""

import streamlit as st

from yieldcurves import settings
from . import shared
from .loaders import load_active_bonds, load_country
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

    st.sidebar.subheader("Active terms")
    load_active_bonds()

    shared.interpolation_method = st.sidebar.radio(
        "Interpolation method", options=["cubic", "quadratic", "linear"], index=0
    )

    # Layout (post-data)
    cont0.subheader(f"Bond yields: *{shared.target_country.title()}*")

    # Content
    plot_yield_curve(
        active_bonds=shared.bonds_active,
        # active_dates=shared.selected_dates,
        # ++++++++++++++++++++++++++++++++++++++++++++++
        active_dates=["2022-2-17", "2022-1-27"],  # TEMP
        # ++++++++++++++++++++++++++++++++++++++++++++++
    )
