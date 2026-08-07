import pandas as pd
import talib


def add_indicators(df: pd.DataFrame, ema_multiplier: float = 1.25) -> pd.DataFrame:
    """Append EMA10/20, SMA50/100, EMA10 x multiplier, ATR14, and ADR14 to OHLCV bars."""
    df = df.copy()
    close = df["close"].to_numpy(dtype="float64")
    high = df["high"].to_numpy(dtype="float64")
    low = df["low"].to_numpy(dtype="float64")

    df["ema_10"] = talib.EMA(close, timeperiod=10)
    df["ema_20"] = talib.EMA(close, timeperiod=20)
    df["sma_50"] = talib.SMA(close, timeperiod=50)
    df["sma_100"] = talib.SMA(close, timeperiod=100)
    df["ema_10_x_multiplier"] = df["ema_10"] * ema_multiplier
    df["atr_14"] = talib.ATR(high, low, close, timeperiod=14)
    # ADR = SMA(high - low, 14), in price points
    df["adr_14"] = talib.SMA(high - low, timeperiod=14)
    # ADR% = SMA(100 * high / low, 14) - 100
    df["adr_14_pct"] = talib.SMA(100 * high / low, timeperiod=14) - 100
    return df
