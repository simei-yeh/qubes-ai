import pandas as pd

from qubes_ai.common import locate_on_or_after, weekly_resample

NAN = float("nan")

WINDOW_WEEKS = 13


def compute_outcomes(df: pd.DataFrame, pattern_start_date: str, pattern_end_date: str | None) -> dict:
    """Four outcome metrics measured from the breakout price at pattern_start_date:
    1. defined_favorable_move_pct - return to the close price 13 weeks out
    2. return_below_10dma_pct - return at first daily close below the 10-day SMA
    3. return_below_10wkma_pct - return at first weekly close below the 10-week SMA
    4. return_pattern_end_pct - simple return to pattern_end_date (null if not given)
    """
    i = locate_on_or_after(df, pattern_start_date)
    if i is None:
        return {}
    breakout_price = float(df.loc[i, "close"])
    start_ts = pd.Timestamp(pattern_start_date)

    window_end = start_ts + pd.Timedelta(weeks=WINDOW_WEEKS)
    window_end_i = locate_on_or_after(df, window_end)
    defined_favorable_move_pct = (
        (float(df.loc[window_end_i, "close"]) / breakout_price - 1) * 100 if window_end_i is not None else NAN
    )

    df = df.assign(sma_10=df["close"].rolling(10).mean())
    forward = df[df["time"] > start_ts]
    below_10dma = forward[forward["close"] < forward["sma_10"]]
    return_below_10dma_pct = (
        (float(below_10dma.iloc[0]["close"]) / breakout_price - 1) * 100 if not below_10dma.empty else NAN
    )

    weekly = weekly_resample(df)
    weekly["sma_10"] = weekly["close"].rolling(10).mean()
    weekly_forward = weekly[weekly["time"] > start_ts]
    below_10wkma = weekly_forward[weekly_forward["close"] < weekly_forward["sma_10"]]
    return_below_10wkma_pct = (
        (float(below_10wkma.iloc[0]["close"]) / breakout_price - 1) * 100 if not below_10wkma.empty else NAN
    )

    return_pattern_end_pct = NAN
    if pattern_end_date:
        end_i = locate_on_or_after(df, pattern_end_date)
        if end_i is not None:
            return_pattern_end_pct = (float(df.loc[end_i, "close"]) / breakout_price - 1) * 100

    return {
        "defined_favorable_move_pct": defined_favorable_move_pct,
        "return_below_10dma_pct": return_below_10dma_pct,
        "return_below_10wkma_pct": return_below_10wkma_pct,
        "return_pattern_end_pct": return_pattern_end_pct,
    }
