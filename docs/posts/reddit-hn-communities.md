# Reddit, Hacker News, dev-сообщества

Тон везде: разработчик показывает открытый инструмент и просит критику. Не «сигналы», не «доходность». В r/algotrading и на HN самореклама с цифрами доходности получает минусы и бан, а честный разбор ограничений получает обсуждение.

## r/algotrading (Show & Tell / Strategy)

**Title:** Open-source momentum rotation lab for crypto: annualized momentum across windows + BTC↔alts backtest. Looking for holes in the methodology.

**Body:**

I've been working on a small open-source tool (Python, Streamlit) that does two things:

1. Puts momentum of top coins on one scale. For a window of W days: ln(P_t / P_{t−W}) · 365/W, optionally on smoothed prices (SMA/EMA/ZLEMA, period in days). 7-day and 1-year windows end up on the same axis.
2. Backtests a rotation rule on that signal: BTC is the base, an alt gets one of K slots when its momentum beats BTC by more than an entry edge, loses it below an exit edge (hysteresis). Two sizing modes: event-driven (spend base/free_slots on entry, never resize) and periodic target-weight 1/K.

Default preset over 5y of Binance 2h candles, 10 bps per leg: strategy 6.4x vs BTC hold 1.6x, max DD −69% vs −77%, 314 trades, last 12 months flat vs BTC.

Known problems I'm fixing next, and where I'd like your input:
- Fills at the same bar's close the signal uses. Moving to next-bar open.
- Survivorship: the pool is today's liquid alts. Need point-in-time universe.
- Thresholds are in pp of annualized momentum, which means different things on a 7d vs 365d window. Considering vol-normalizing (z-score).
- In-sample parameter choice. Planning walk-forward + parameter heatmaps.

Anything else that would make you dismiss this backtest?

Repo: github.com/Acnologiak/CryptoMomentumLab. The core (data/analytics/strategy) has no Streamlit dependency, 54 tests.

## r/CryptoCurrency (Tools/Analysis)

**Title:** I built an open-source dashboard that compares momentum of top coins on one scale (% per year) and backtests BTC↔alts rotation. Feedback welcome.

**Body:** короткая версия поста выше без деталей формул, с тремя оговорками и ссылкой на репозиторий. Без цифр доходности в заголовке.

## Hacker News (Show HN)

**Title:** Show HN: Crypto Momentum Lab – annualized momentum across windows and rotation backtests, open source

**First comment (от автора):**

Author here. The tool rescales momentum over any window to percent-per-year so windows are comparable, then backtests a two-threshold rotation rule between BTC and alts. Layered Python: data (exchange clients + parquet cache), analytics, strategy, and a Streamlit UI on top; the core has no UI dependency.

What I'd most like feedback on is the backtest methodology: it currently fills at the signal bar's close, uses today's coin universe, and the default parameters came from an in-sample grid. I know each of these inflates results and I'm fixing them in that order. If you've dealt with point-in-time crypto universes, I'd love pointers.

## Habr / DOU (статья, тезисы)

Заголовок: «Моментум на одной шкале: как сравнить неделю и год и не обмануть себя бэктестом».

План:
1. Проблема сравнения окон, формула, почему лог-режим.
2. Сглаживание в днях, ZLEMA.
3. Правило ротации, гистерезис, два режима сайзинга.
4. Архитектура: три слоя, тесты, побитовая сверка движка.
5. Результаты и то, что их завышает. Честно, с таблицей.
6. Ускорение Streamlit-приложения в 9 раз: tz-aware даты в plotly, векторизация бухгалтерии движка, кеш бэктеста.
7. Что дальше и где код.

Пункт 6 сам по себе годится в отдельную короткую статью, инженерам он интереснее доходности.

## Product Hunt / каталоги

**Tagline:** Momentum of top crypto coins on one scale, plus rotation backtests. Open source.
**Description (260):** Crypto Momentum Lab rescales momentum over any look-back window to percent per year, so a 7-day and a 1-year trend sit on one axis. It ranks coins, and backtests a BTC↔alts rotation rule with fees and a trade journal. Open source, self-hostable, research tool, not financial advice.
