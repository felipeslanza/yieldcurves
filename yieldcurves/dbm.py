"""
yieldcurves.dbm
~~~~~~~~~~~~~~~

Database manager to persist/cache requests to investpy
"""

import logging
import re
from typing import Optional, Union

import pandas as pd
import pymongo

from .utils import flip_date_format


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
            self.collection.create_index("country")
            self.collection.create_index("bond")
            self.collection.create_index("dates")

            # Required to ensure uniqueness on (date, cnpj) pair
            self.collection.create_index(
                [
                    ("country", pymongo.ASCENDING),
                    ("bond", pymongo.ASCENDING),
                    ("dates", pymongo.ASCENDING),
                ],
                unique=True,
            )

    def find(
        self,
        ticker: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Optional[Union[pd.Series, pd.DataFrame]]:
        """Query a ticker from the database

        ....

        Parameters
        ----------
        ticker : str
        from_date : str
            in YYYY-MM-DD format
        to_date : str
            in YYYY-MM-DD format
        """
        query = {"bond": ticker.lower()}
        if from_date or to_date:
            query["dates"] = {}
            if from_date:
                query["dates"]["$gte"] = pd.to_datetime(flip_date_format(from_date))
            if to_date:
                query["dates"]["$lte"] = pd.to_datetime(flip_date_format(to_date))

        out = dict(_id=0, dates=1, close=1, open=1, high=1, low=1)
        obj = list(self.collection.find(query, out))
        if obj:
            assert len(obj) == 1
            return pd.DataFrame(obj[0]).set_index("dates")

    def write(self, data: pd.DataFrame):
        """Write multiple time series with yield data (as
        returned from `investpy`) to the database

        ...

        Parameters
        ----------
        data : pd.DataFrame
        """
        assert data.index.is_monotonic, "Data must already be sorted"
        assert data.columns.nlevels > 1, "Columns must be MultiIndex"

        data.rename(str.lower, axis=1, inplace=True)
        bonds = data.columns.get_level_values(0)
        country = re.sub(" ", "_", re.findall(r"([a-zA-Z\s]{2,}) ", bonds[0])[0])
        for ticker, df in data.groupby(bonds, axis=1):
            df = df[ticker]  # Drop level 0
            ticker = ticker.replace(" ", "_")
            db_obj = self.collection.find_one({"bond": ticker})

            # New data
            if not db_obj:
                new_obj = {
                    "country": country,
                    "bond": ticker,
                    "dates": df.index.tolist(),
                    **dict(zip(df.columns, df.T.values.tolist())),
                }
                logger.info(f"Inserting new {ticker} to DB")
                self.collection.insert_one(new_obj)

            # Existing data, append each field
            else:
                try:
                    last_date = db_obj["dates"][-1]
                except IndexError:
                    last_date = None

                df = df.loc[last_date:]
                new_obj = {"$push": {"dates": {"$each": df.index.tolist()}}}
                for field, series in df.iteritems():
                    new_obj["$push"][field] = {"$each": series.tolist()}
                logger.info(f"Updating existing {ticker} in DB")
                self.collection.update_one({"bond": ticker}, new_obj)
