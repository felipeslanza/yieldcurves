"""
yieldcurves.app.shared
~~~~~~~~~~~~~~~~~~~~~~

This module defines variables shared across the app.
"""

from typing import List, Set

import pandas as pd


target_country: str = ""

bonds_df: pd.DataFrame = pd.DataFrame()
bonds_tickers: List[str] = []
bonds_terms: List[str] = []
bonds_active: Set[str] = set()

selected_dates: List[str] = []
