import pandas as pd
import streamlit as st

from yieldcurves.data_handlers import get_ohlc_yield_history
from yieldcurves.utils import sort_by_term
from . import shared


__all__ = ("load_country",)


@st.cache
def load_country(target_country: str):
    #### TEMP ####
    # df = get_ohlc_yield_history(target_country)
    # df = df.xs("Close", 1, 1)
    df = pd.read_pickle("/home/fsl/code/yieldcurves/temp.pkl")
    #### TEMP ####

    # Updated shared variables
    shared.target_country = target_country
    shared.bonds_df = df
    shared.bonds_tickers = sort_by_term(list(df))
    shared.bonds_terms = get_terms(shared.bonds_tickers)
