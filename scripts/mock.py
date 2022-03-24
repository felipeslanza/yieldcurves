from yieldcurves.data_handlers import *
from yieldcurves.dbm import Manager


if __name__ == "__main__":
    # Setup
    # ----
    dbm = Manager()
    df = get_ohlc_yield_history("brazil")

    # Run
    # ----
    dbm.write(df)
    bz1 = dbm.find("brazil_3m")
