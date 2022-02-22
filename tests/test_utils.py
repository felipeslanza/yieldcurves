import pandas as pd
import pytest

from yieldcurves.utils import *


# Globals
# ----
tickers = ["Brazil 10Y", "Brazil 20Y", "Brazil 1Y", "Brazil 3M", "Brazil 11M"]
tickvals = [3, 11, 12, 120, 240]
sorted_tickers = ["Brazil 3M", "Brazil 11M", "Brazil 1Y", "Brazil 10Y", "Brazil 20Y"]
sorted_terms = ["3M", "11M", "1Y", "10Y", "20Y"]


def test_sort_by_term_with_different_types():
    assert sort_by_term(tickers) == sorted_tickers
    assert sort_by_term(set(tickers)) == sorted_tickers
    assert sort_by_term(pd.DataFrame(columns=tickers)) == sorted_tickers


def test_get_tickvals():
    with pytest.raises(ValueError):
        get_tickvals(["11M", *sorted_terms])
    assert get_tickvals(sorted_terms) == tickvals
