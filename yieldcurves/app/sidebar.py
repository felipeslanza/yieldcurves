from typing import Tuple

import pandas as pd
import streamlit as st

from yieldcurves.data_handlers import get_yield_curve


__all__ = ("render_sidebar",)


def render_sidebar() -> Tuple[str, pd.DataFrame]:
    st.sidebar.subheader("Settings")

    target_country = st.sidebar.text_input("Target country (full name)")
    if target_country:
        bonds_df = get_yield_curve(target_country)

        st.sidebar.subheader("Columns display")

        for term in bonds_df.columns:
            st.sidebar.checkbox(term, value=True)

        return (target_country, bonds_df)
