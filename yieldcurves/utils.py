import logging
import re
from functools import lru_cache
from typing import List

import investpy
import numpy as np
import pandas as pd


__all__ = (
    "get_terms",
    "get_tickvals",
    "interpolate_curve",
    "search_country",
    "sort_by_term",
)


logger = logging.getLogger(__name__)


def get_terms(tickers: List[str]) -> List[str]:
    """Map tickers to bond terms, e.g. Brazil 5Y -> 5Y"""
    return re.findall(r"\d+[MY]", "|".join(tickers))


def get_tickvals(terms: List[str]) -> List[int]:
    """Map terms to an integer (for setting x-axis when plotting)

    ...

    Parameters
    ----------
    terms : List[str]
    """
    if len(set(terms)) != len(terms):
        raise ValueError("Bond terms must be unique")

    vals = [None] * len(terms)
    for i, term in enumerate(terms):
        if "M" in term:
            val = int(term[:-1])
        elif "Y" in term:
            val = int(term[:-1]) * 12
        else:
            raise ValueError(f"Unrecognized period [{term}]")
        vals[i] = val

    # If resulting tickvals are not monotonic, input was likely not sorted
    if not pd.Series(vals).is_monotonic:
        return get_tickvals(sort_by_term(terms))
    return vals


def interpolate_curve(data: pd.Series, method: str) -> pd.Series:
    """Wrapper to interpolate a curve by gradually stepping "down" in method"""
    curve = None
    try:
        curve = data.interpolate(method=method)
    except ValueError:
        logger.error(f"Not enough data for method `{method}`. Using `quadratic`.")
        try:
            curve = data.interpolate(method="quadratic")
        except ValueError:
            logger.error(f"Not enough data for method `quadratic`. Using `linear`.")
            curve = data.interpolate(method="linear")

    return curve


def _is_valid_ticker(ticker: str) -> bool:
    """Helper to drop tickers/terms with unwanted patterns"""
    restricted = ["Overnight", "W"]
    for el in restricted:
        if el in ticker:
            return False
    return True


@lru_cache(maxsize=32)
def search_country(query: str) -> List[str]:
    """Search available bonds for a given country

    ...

    Parameters
    ----------
    query : str
        full name of target country (e.g. "united kingdom", *NOT* "uk")
    """
    tickers = []
    try:
        res = investpy.search_bonds("full_name", query)
    except RuntimeError:
        logger.error("No countries found.")
    else:
        if res.country.unique().size != 1:
            logger.error(f"Ambiguous query [{query}].")
        else:
            tickers = res.name.tolist()

    return list(filter(_is_valid_ticker, tickers))


def sort_by_term(tickers: List[str]) -> List[str]:
    """Sort bond tickers by term

    ...

    Parameters
    ----------
    tickers : List[str]
        list of tickers containg a valid term, e.g. ["foo 1y", "foo 20y"]
    """

    def _custom_sorter(key: str) -> str:
        """Add higher prefix to years and sort as number (not alphabetically)"""
        number, period = key[:-1], key[-1]
        suffix = {"Y": 10000, "M": 100, "W": 1}[period]

        return int(f"{suffix}{number}")

    terms = get_terms(tickers)
    sorted_terms = sorted(terms, key=_custom_sorter)
    idx = [terms.index(i) for i in sorted_terms]

    return np.array(list(tickers))[idx].tolist()
