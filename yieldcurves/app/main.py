import streamlit as st

from .sidebar import render_sidebar


__all__ = ("run",)


def run():
    st.set_page_config(layout="wide")

    res = render_sidebar()
    if res is not None:
        target_country, bonds_df = res
