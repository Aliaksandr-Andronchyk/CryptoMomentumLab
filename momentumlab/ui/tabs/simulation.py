"""Tab 4 — the BTC <-> alts rotation backtest."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from ...strategy import Backtester, BacktestResult, StrategyConfig
from ..context import DashboardContext
from ..strategy_form import StrategyForm
from ..strategy_report import StrategyReportView
from .base import DashboardTab

BASE_ASSET = "BTC"


@st.cache_data(show_spinner="Симуляція…", max_entries=32)
def run_backtest(prices: pd.DataFrame, interval: str, start: str, end: str,
                 config_key: str, _config: StrategyConfig) -> BacktestResult:
    """The backtest keyed on its inputs, so a rerun caused by any other widget
    (a sort order, a log-scale toggle) does not simulate five years again.
    `_config` is not hashed; `config_key` (its repr) stands in for it."""
    return Backtester(_config, interval).run(
        prices, start=pd.Timestamp(start), end=pd.Timestamp(end))


class SimulationTab(DashboardTab):
    title = "🤖 Симуляція стратегії"

    def render(self, ctx: DashboardContext) -> None:
        st.subheader("Ротація BTC ↔ альткоїни за моментумом")

        if BASE_ASSET not in ctx.prices.columns:
            st.warning(
                f"Потрібен {BASE_ASSET} у списку монет («Показати» в бічній панелі) — "
                "він базовий (стабільний) актив стратегії.")
            return

        alt_universe = [c for c in ctx.coins if c != BASE_ASSET]
        if not alt_universe:
            st.info("Додайте в бічній панелі хоча б одну альткоїну крім BTC.")
            return

        choices = StrategyForm(BASE_ASSET, alt_universe).render()
        if not choices.pool:
            st.info("Пул альткоїнів порожній — нічого симулювати.")
            return

        settings = ctx.settings
        try:
            config = choices.to_config(settings.smoothing, settings.smoothing_days,
                                       settings.mode)
            result = run_backtest(
                ctx.prices[[BASE_ASSET] + choices.pool], settings.interval,
                str(ctx.low), str(ctx.high), repr(config), config)
        except ValueError as exc:
            st.error(str(exc))
            return

        StrategyReportView(result, ctx.charts).render()
