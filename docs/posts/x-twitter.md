# X / Twitter

## Bio

Crypto Momentum Lab. Annualized momentum of top coins on one scale + BTC↔alts rotation backtest. Open source. Research tool, not financial advice.

## Launch thread (English)

1/
Comparing a +6% week to a +40% year is meaningless. We built a tool that puts every look-back window on one scale: % per year.

Crypto Momentum Lab, open source, live dashboard. 🧵

2/
Method: for a window of W days, momentum = ln(P_t / P_{t−W}) · 365 / W. Log mode by default, because compounding a good week into a year gives +285,000% p.a. and a useless chart.

Smoothing in days, not bars, so changing the candle interval keeps the meaning.

3/
On top: a rotation rule. BTC is the base. An alt earns one of K slots when its momentum beats BTC by more than an entry edge. It gives the slot back when the edge falls below an exit edge. Two thresholds = hysteresis = no flapping on noise.

4/
Backtest, default preset, Binance, 5y, 10 bps fees:
strategy +543% vs BTC hold +59%
max DD −69% vs −77%
314 trades, fees ate 55% of starting capital
last 12 months: flat vs BTC

5/
Now the honest part. Three things inflate that number:
• fills at the same bar's close the signal was computed on
• the alt pool is today's liquid coins (survivorship)
• thresholds tuned on the same history

Fixing these first. Numbers before/after will be public.

6/
Code: 3 layers (data / analytics / strategy) with zero Streamlit dependency, 54 tests, engine bit-for-bit verified against the original. Full page recompute on 5y of 2h candles × 10 coins: ~3s.

github.com/Acnologiak/CryptoMomentumLab

7/
Roadmap: honest backtest → daily signals → public paper-trading log → API.
Not financial advice. Past performance ≠ future results.
Feedback from quants especially welcome.

## Короткий пост (русский)

Собрали инструмент, который кладёт моментум топ-монет на одну шкалу (% годовых) и проверяет ротацию BTC↔альты на истории. Открытый код, живой дашборд.

Бэктест красивый, но мы сами перечислили, что его завышает, и чиним это первым. Подробности в треде.
