import logging
from typing import Optional

import investpy


__all__ = ("search_bonds",)


logger = logging.getLogger(__name__)


def search_country(query: str) -> Optional[str]:
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
            return res.name.tolist()
