import pandas as pd


def locate_on_or_after(df: pd.DataFrame, date: str) -> int | None:
    """Index of the first row with time >= date, or None if date is past the end of df."""
    matches = df.index[df["time"] >= pd.Timestamp(date)]
    return matches[0] if len(matches) > 0 else None


def weekly_resample(df: pd.DataFrame) -> pd.DataFrame:
    """Resample daily OHLCV bars into Friday-anchored weekly bars. (to find, i.e. 10-wk MA)"""
    weekly = (
        df.set_index("time")
        .resample("W-FRI")
        .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
        .dropna()
        .reset_index()
    )
    return weekly
