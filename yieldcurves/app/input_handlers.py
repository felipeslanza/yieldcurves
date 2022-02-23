from datetime import datetime
from typing import List

import pandas as pd
from streamlit.delta_generator import DeltaGenerator

from yieldcurves import settings
from . import shared


__all__ = (
    "render_country_selector",
    "render_dates_selector",
    "render_interpolation_selector",
)


def render_country_selector(
    container: DeltaGenerator,
    default: str = "Brazil",
) -> str:
    return container.text_input(
        label="Country (full name)",
        value=default,
    ).lower()


def render_dates_selector(container: DeltaGenerator) -> List[str]:
    container.subheader("Dates")

    today = datetime.today().date()
    d0_val = today.strftime(settings.DATE_FORMAT)
    d1_val = (today - pd.Timedelta("30d")).strftime(settings.DATE_FORMAT)
    d2_val = (today - pd.Timedelta("365d")).strftime(settings.DATE_FORMAT)

    d0 = container.text_input("#1: ", value=d0_val)
    d1 = container.text_input("#2: ", value=d1_val)
    d2 = container.text_input("#3: ", value=d2_val)

    return d0, d1, d2


def render_interpolation_selector(container: DeltaGenerator):
    return container.radio(
        label="Interpolation method",
        options=["cubic", "quadratic", "linear"],
        index=0,
    )
