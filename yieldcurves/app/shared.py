"""
yieldcurves.app.shared
~~~~~~~~~~~~~~~~~~~~~~

This module defines variables shared across the app.
"""

import pandas as pd

target_country: str = ""

bonds_df: pd.DataFrame = pd.DataFrame()
bonds_tickers: list = []
bonds_active: set = set()
