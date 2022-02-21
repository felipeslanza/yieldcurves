import logging
import re
from functools import lru_cache
from typing import List

import investpy
import numpy as np


__all__ = ("search_country", "sort_tickers")


logger = logging.getLogger(__name__)


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
            tickers = res.name.sort_values().tolist()

    return tickers


def sort_tickers(tickers: List[str]) -> List[str]:
    """Sort bond tickers by term"""

    def _custom_sorter(key: str) -> str:
        """Add higher prefix to years and sort as number (not alphabetically)"""
        number, period = key[:-1], key[-1]
        suffix = {"Y": 100, "M": 1}[period]

        return int(f"{suffix}{number}")

    terms = re.findall(r"\d+[MY]", "|".join(tickers))
    sorted_terms = sorted(terms, key=_custom_sorter)
    idx = [terms.index(i) for i in sorted_terms]

    return np.array(list(tickers))[idx].tolist()
