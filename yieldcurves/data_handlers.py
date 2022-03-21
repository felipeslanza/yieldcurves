"""
yieldcurves.data_handlers
~~~~~~~~~~~~~~~~~~~~~~~~~

This module defines functions to get yield data.
"""

import logging
from datetime import datetime
from time import sleep
from typing import Optional

import pandas as pd
import investpy

from . import settings
from .utils import search_country


__all__ = (
    "get_recent_yield",
    "get_ohlc_yield_history",
)


logger = logging.getLogger(__name__)


# Globals
# ----
TODAY = datetime.today().date()
TODAY_STR = TODAY.strftime("%d/%m/%Y")


def get_recent_yield(
    country_name: str,
    field: str = "Close",
    n_rows: int = 22,
) -> Optional[pd.DataFrame]:
    """Returns the most recent yield data for `country_name`

    ...

    Parameters
    ----------
    country_name : str
    field : str
        target field in OHLC, one of {Close, Open, High Low}
    n_rows : int
        # of rows to be returned
    """
    tickers = search_country(country_name)

    data = {}
    for ticker in tickers:
        tries = 0
        while tries < settings.MAX_RETRIES_ON_CONNECTION_ERROR:
            try:
                df = investpy.get_bond_recent_data(ticker)
                break
            except ConnectionError as e:
                logger.error(e)
                sleep(10)
            tries += 1
        data[ticker] = df[field].rename(ticker)

    if data:
        df = pd.DataFrame(data)
        return df.tail(n_rows).dropna(thresh=settings.MIN_VALID_CURVE_THRESHOLD)


def get_ohlc_yield_history(
    country_name: str,
    from_date: str = "01/01/2020",
    to_date: str = TODAY_STR,
) -> Optional[pd.DataFrame]:
    """Returns historical OHLC yield data for all bonds issued by `country_name`

    ...

    Parameters
    ----------
    country_name : str
    from_date : str
        start date in "DD/MM/YYYY" format
    to_date : str
        end date in "DD/MM/YYYY" format
    """
    tickers = search_country(country_name)

    if tickers:
        logging.info(f"Getting yield data for [{country_name}]")

        curve = {}
        kwargs = {"from_date": from_date, "to_date": to_date}
        for ticker in tickers:
            tries = 0
            while tries < settings.MAX_RETRIES_ON_CONNECTION_ERROR:
                try:
                    df = investpy.get_bond_historical_data(ticker, **kwargs)
                    break
                except ConnectionError as e:
                    logger.error(e)
                    sleep(10)
                tries += 1

            curve[ticker] = df

        if curve:
            return pd.concat(curve, axis=1)
