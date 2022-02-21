"""
yieldcurves.settings
~~~~~~~~~~~~~~~~~~~~

This module consolidates all of the project's settings.
"""

import os


__all__ = ("LOGGING_LEVEL", "LOGGING_FORMAT")


# General
# ----
LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
LOGGING_FORMAT = "%(levelname)s - yieldcurves.%(module)s.%(funcName)s - %(message)s"


# Investing Data
# ----
# Mininum number of valid yield points in a given date for the curve to be
# considered valid, i.e. row is not dropped.
MIN_VALID_CURVE_THRESHOLD = 2
