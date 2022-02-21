import logging
from functools import lru_cache
from typing import List, Optional

import investpy


__all__ = ("search_bonds",)


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
