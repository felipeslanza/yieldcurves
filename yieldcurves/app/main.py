"""
yieldcurves.app.main
~~~~~~~~~~~~~~~~~~~~

This module controls the app.
"""

import streamlit as st

from yieldcurves import settings
from . import shared
from .input_handlers import (
    render_country_selector,
    render_dates_selector,
    render_interpolation_selector,
)
from .loaders import load_active_bonds, load_country
from .plotting import plot_yield_curve


def run():

    try:
        # Config
        st.set_page_config(**settings.ST_PAGE_CONFIG)

        # Layout (pre-data)
        st.sidebar.header("Settings")
        cont0 = st.container()
        target_country = render_country_selector(st.sidebar)

        # Setup & load data
        load_country(target_country)  # cached
        st.sidebar.subheader("Active terms")
        load_active_bonds()
        shared.interpolation_method = render_interpolation_selector(st.sidebar)

        if shared.target_country:
            # Layout (post-data)
            cont0.title(f"Bond yields: *{shared.target_country.title()}*")
            left0, right0 = cont0.columns([0.8, 0.2])
            selected_dates = render_dates_selector(right0)

            # Content
            plot_yield_curve(
                active_bonds=shared.bonds_active,
                active_dates=selected_dates,
                container=left0,
            )
    except Exception as e:
        print(e)
        breakpoint()
