"""
yieldcurves.settings
~~~~~~~~~~~~~~~~~~~~

This module consolidates all of the project's settings.
"""

import os


# General
# ----
DATE_FORMAT = "%Y-%m-%d"

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
LOGGING_FORMAT = "%(levelname)s - yieldcurves.%(module)s.%(funcName)s - %(message)s"


# Investing data
# ----
# Mininum number of valid yield points in a given date for the curve to be
# considered valid, i.e. row is not dropped.
MIN_VALID_CURVE_THRESHOLD = 2


# Streamlit app
# ----
ST_PAGE_CONFIG = dict(
    page_title="yieldcurves",
    layout="wide",
)
