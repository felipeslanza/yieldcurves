"""
yieldcurves.settings
~~~~~~~~~~~~~~~~~~~~

This module consolidates all of the project's settings.
"""

import os


# General
# ----
DATE_FORMAT = "%Y/%m/%d"  # pandas-like, same as in local DB
INVESTPY_DATE_FORMAT = "%d/%m/%Y"

# --------------------------------------------------------
# Logging settings are defined at '.streamlit/config.toml'
# --------------------------------------------------------


# Investing data
# ----
# Mininum number of valid yield points in a given date for the curve to be
# considered valid, i.e. row is not dropped.
MIN_VALID_CURVE_THRESHOLD = 2
MAX_RETRIES_ON_CONNECTION_ERROR = 3


# Streamlit app
# ----
ST_PAGE_CONFIG = dict(
    page_title="yieldcurves",
    layout="wide",
)
