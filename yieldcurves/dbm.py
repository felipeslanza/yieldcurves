"""
yieldcurves.dbm
~~~~~~~~~~~~~~~

Database manager to persist/cache requests to investpy
"""

import logging
import re
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

    def write_data(self, data: pd.DataFrame):
        """Write multiple time series with yield data (as
        returned from `investpy`) to the database

        ...

        Parameters
        ----------
        data : pd.DataFrame
        """
        data.rename(str.lower, axis=1, inplace=True)
        bonds = data.columns.get_level_values(0)
        country = re.sub(" ", "_", re.findall(r"([a-zA-Z\s]{2,}) ", bonds[0])[0])
        for ticker, df in data.groupby(bonds, axis=1):
            df = df[ticker]  # Drop level 0
            ticker = re.sub(" ", "_", ticker)
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
                new_obj = {"$push", {"dates": {"$each": df.index.tolist()}}}
                for field, series in df.iteritems():
                    new_obj["$push"][field] = {"$each": series.tolist()}
                logger.info(f"Updating existing {ticker} in DB")
                self.collection.updateOne({"bond": ticker}, new_obj)
