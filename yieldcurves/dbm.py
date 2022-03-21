"""
yieldcurves.dbm
~~~~~~~~~~~~~~~

Database manager to persist/cache requests to investpy
"""

import logging
from typing import Optional

import pandas as pd
import pymongo


__all__ = ("Manager",)


logger = logging.getLogger(__name__)


# Globals
# ----
DEFAULT_CLIENT_SETTINGS = {
    "connectTimeoutMS": 2500,
    "serverSelectionTimeoutMS": 2500,
    "retryWrites": True,
}


class Manager:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 27017,
        *,
        db: str = "yieldcurvesDB",
        collection: str = "bonds",
        username: Optional[str] = None,
        password: Optional[str] = None,
        **client_settings,
    ):
        self.host = self.parse_host(host)
        self.port = port
        self.db = db
        self.collection = collection
        self.username = username
        self.password = password

        self.client_settings = {
            **DEFAULT_CLIENT_SETTINGS,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            **client_settings,
        }

        self.setup()

    @staticmethod
    def parse_host(host: str) -> str:
        """Simple util to infer correct schema from user-provided `host`"""
        if len(host.split("//")) > 1:
            # Prefix is present
            return host
        elif host.endswith("mongodb.net"):
            # Single host resolving to multiple hosts (e.g. Atlas)
            return f"mongodb+srv://{host}"
        else:
            # Single host
            return f"mongodb://{host}"

    def setup(self):
        """Connect to the server and setup collection indexes"""
        try:
            self.client = pymongo.MongoClient(**self.client_settings)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            logger.error(f"Failed to setup to database - {e}")
        else:
            self.db = self.client[self.db]
            self.collection = self.db[self.collection]

            # Required to speed up query
            self.collection.create_index("date")
            self.collection.create_index("fund_cnpj")

            # Required to ensure uniqueness on (date, cnpj) pair
            self.collection.create_index(
                [
                    ("country", pymongo.ASCENDING),
                    ("bond", pymongo.ASCENDING),
                ],
                unique=True,
            )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # TODO: implement those
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def write_series(self, series: pd.Series, name: str = ""):
        """Write a single time series with yield data to the database

        ...

        Parameters
        ----------
        series : pd.Series
        """
        assert series.size, "Empty `Series`"

        name = name or series.name
        assert len(name.split("|")) == 2, "Incorrect name, must be 'TICKER|FIELD'"

        raise NotImplementedError()

    def write_df(self, df: pd.DataFrame):
        """Write multiple time series with yield data to the database

        ...

        Parameters
        ----------
        df : pd.DataFrame
        """
        assert df.size, "Empty `DataFrame`"

        raise NotImplementedError()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
