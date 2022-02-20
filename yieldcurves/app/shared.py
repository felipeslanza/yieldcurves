import pandas as pd

# App globals
# ----
target_country: str = ""

bonds_df: pd.DataFrame = pd.DataFrame()
bonds_tickers: list = []
bonds_active: set = set()
