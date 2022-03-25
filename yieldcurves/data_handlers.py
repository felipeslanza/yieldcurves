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
from .dbm import Manager
from .utils import flip_date_format, search_country


__all__ = (
    "get_recent_yield",
    "get_ohlc_yield_history",
)


logger = logging.getLogger(__name__)


# Globals
# ----
TODAY = datetime.today().date()
TODAY_STR = TODAY.strftime("%d/%m/%Y")
LOCAL_DB_MANAGER = Manager()


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
        df = _safely_get_ohlc_hist(ticker)
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


def _safely_get_ohlc_hist(
    ticker: str,
    from_date: str,
    to_date: str,
    manager: Manager,
) -> Optional[pd.DataFrame]:
    """Wrapper around `get_bond_historical_data` to handle connection errors"""
    if from_date == to_date:
        return

    df = None
    tries = 0
    while tries < settings.MAX_RETRIES_ON_CONNECTION_ERROR:
        try:
            df = investpy.get_bond_historical_data(
                ticker,
                from_date=from_date,
                to_date=to_date,
            )
            break
        except ConnectionError as e:
            logger.error(e)
            sleep(10)
        tries += 1

    if df is not None and manager is not None:
        cols = df.columns
        df.columns = pd.MultiIndex.from_product(((ticker,), cols))
        manager.write(df)
        df.columns = cols

    return df


def get_ohlc_yield_history(
    country_name: str,
    from_date: str = "01/01/2020",
    to_date: str = TODAY_STR,
    manager: Optional[Manager] = LOCAL_DB_MANAGER,
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
    logging.info(f"Getting yield data for [{country_name}]")

    tickers = search_country(country_name)
    if not tickers:
        return

    curve = {}
    for ticker in tickers:
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # WARNING: ticker naming convention in DB is different than `investpy`'s
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        db_ticker = ticker.lower().replace(" ", "_")

        # Try hitting local DB first (preliminary)
        if manager:
            from_date_ = flip_date_format(from_date)  # DB format
            to_date_ = flip_date_format(to_date)  # DB format

            df = manager.find(db_ticker, from_date_, to_date_)
            if df is None:
                df = pd.DataFrame()

            df = df.loc[from_date_:to_date_]
            if df.size > 1:
                # Fill missing data only
                if df.index[0] > pd.to_datetime(from_date_):
                    to_date2 = df.index[0] - pd.Timedelta("1D")
                    to_date2 = to_date2.strftime(settings.INVESTPY_DATE_FORMAT)
                    df_pre = _safely_get_ohlc_hist(ticker, from_date, to_date2, manager)
                    if df_pre is not None:
                        df = pd.concat([df_pre, df], axis=1).sort_index()
                if df.index[-1] < pd.to_datetime(to_date_):
                    from_date2 = df.index[-1] + pd.Timedelta("1D")
                    from_date2 = from_date2.strftime(settings.INVESTPY_DATE_FORMAT)
                    df_post = _safely_get_ohlc_hist(ticker, from_date2, to_date, manager)
                    if df_post is not None:
                        df = pd.concat([df_post, df], axis=1).sort_index()

                curve[db_ticker] = df
                continue

        # Query `investpy` instead
        df = _safely_get_ohlc_hist(ticker, from_date, to_date, manager)
        if df is not None:
            curve[ticker] = df

    if curve:
        return pd.concat(curve, axis=1)
