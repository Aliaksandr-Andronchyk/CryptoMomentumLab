"""Tab 5 — raw numbers, CSV export and the state of the disk cache."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ...timeframe import window_label
from ..context import DashboardContext
from ..services import cache_directory, cache_status
from .base import DashboardTab


@st.cache_data(show_spinner=False, max_entries=16)
def csv_bytes(frame: pd.DataFrame) -> bytes:
    """Serialising five years of candles takes longer than drawing a tab, and
    the download buttons ask for it on every rerun — so it is keyed on the frame."""
    return frame.to_csv().encode()


class DataTab(DashboardTab):
    title = "🧾 Дані"

    def render(self, ctx: DashboardContext) -> None:
        settings = ctx.settings

        st.subheader("Знімок моментуму")
        st.dataframe(ctx.snapshot.round(1), width="stretch")

        window = st.selectbox("Вікно для експорту", ctx.windows,
                              index=len(ctx.windows) - 1,
                              format_func=window_label, key="export_win")
        label = window_label(window)
        st.download_button(
            f"⬇ CSV: моментум {label}",
            csv_bytes(ctx.in_range(ctx.panel[window])),
            file_name=f"momentum_{settings.exchange}_{settings.interval}_{label}.csv",
            mime="text/csv",
        )
        st.download_button(
            "⬇ CSV: ціни",
            csv_bytes(ctx.in_range(ctx.prices)),
            file_name=f"prices_{settings.exchange}_{settings.interval}.csv",
            mime="text/csv",
        )

        with st.expander("Кеш на диску"):
            st.dataframe(cache_status(), width="stretch")
            st.caption(f"Каталог: `{cache_directory()}`")
