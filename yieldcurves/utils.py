import logging
import re
from functools import lru_cache
from typing import List, Optional

import investpy
import numpy as np


__all__ = ("search_bonds", "sort_tickers")


logger = logging.getLogger(__name__)


@lru_cache(maxsize=32)
def search_country(query: str) -> Optional[List[str]]:
    """Search available bonds for a given country

    ...

    Parameters
    ----------
    query : str
        full name of target country (e.g. "united kingdom", *NOT* "uk")
    """
    try:
        res = investpy.search_bonds("full_name", query)
    except RuntimeError:
        logger.error("No countries found.")
    else:
        if res.country.unique().size != 1:
            logger.error(f"Ambiguous query [{query}].")
        else:
            return res.name.sort_values().tolist()


def sort_tickers(tickers: List[str]) -> List[str]:
    """Sort bond tickers by term"""

    def _custom_sorter(key: str) -> str:
        """Add higher prefix to years and sort as number (not alphabetically)"""
        number, period = key[:-1], key[-1]
        suffix = 10 if "Y" in period else 1

        return int(f"{suffix}{number}")

    terms = re.findall(r"\d+[MY]", "|".join(tickers))
    sorted_terms = sorted(terms, key=_custom_sorter)
    idx = [terms.index(i) for i in sorted_terms]

    return np.array(tickers)[idx].tolist()
