import pandas as pd

from yieldcurves.utils import *


# Globals
# ----
tickers = ["Brazil 10Y", "Brazil 20Y", "Brazil 1Y", "Brazil 3M", "Brazil 11M"]
tickvals = [3, 11, 12, 120, 240]
sorted_tickers = ["Brazil 3M", "Brazil 11M", "Brazil 1Y", "Brazil 10Y", "Brazil 20Y"]


def test_sort_tickers_with_different_types():
    assert sort_tickers(tickers) == sorted_tickers
    assert sort_tickers(set(tickers)) == sorted_tickers
    assert sort_tickers(pd.DataFrame(columns=tickers)) == sorted_tickers


def test_get_tickvals():
    assert get_tickvals(sorted_tickers) == tickvals
