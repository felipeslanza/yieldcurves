import logging
from datetime import datetime
from typing import Optional

import pandas as pd
import investpy


__all__ = ("get_yield_curve",)


logger = logging.getLogger(__name__)


# Globals
# ----
TODAY = datetime.today().date()
TODAY_STR = TODAY.strftime("%d/%m/%Y")


def get_yield_curve(
    country_name: str,
    from_date: str = "01/01/1990",
    to_date: str = TODAY_STR,
) -> Optional[pd.DataFrame]:
    """Returns historical yield data for all bonds issued by `country_name`

    ...

    Parameters
    ----------
    country_name : str
    from_date : str
        start date in DD/MM/YYYY format
    to_date : str
        end date in DD/MM/YYYY format
    """
    tickers = search_country(country_name)

    if tickers:
        logging.info(f"Getting yield data for [{country_name}]")

        curve = {}
        for ticker in tickers:
            df = investpy.get_bond_historical_data(
                ticker,
                from_date=from_date,
                to_date=to_date,
            )
            curve[ticker] = df

        return pd.concat(curve, axis=1)
