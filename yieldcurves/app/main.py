import streamlit as st

from yieldcurves import settings
from . import shared
from .sidebar import render_sidebar
from .plotting import plot_yield_curve


def run():
    st.set_page_config(**settings.ST_PAGE_CONFIG)

    # Layout
    cont0 = st.container()

    # Setup & get data
    render_sidebar(shared.target_country)
    cont0.subheader(f"Bond yields for {shared.target_country.title()}")

    # Content
    plot_yield_curve()
