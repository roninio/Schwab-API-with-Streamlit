import json
from time import sleep
import numpy as np
import pandas as pd
from lightweight_charts import Chart
import streamlit as st
from src.client import get_client
from streamlit_lightweight_charts import renderLightweightCharts
from datetime import datetime

symbol = "TSDD"

# @st.cache_data
def get_data(atr_period=22, atr_multiplier=3.0, show_labels=True, use_close=True, highlight_state=True):
    client = get_client()
    df1 = client.price_history(symbol, periodType="day", period="10", frequencyType="minute", frequency=10).json()
    candles_data = df1["candles"]
    transformed_data = []

    # Iterate over the candles data
    for candle in candles_data:
        # Create a new dictionary with the desired format
        new_entry = candle
        new_entry["time"] = candle["datetime"]

        # Append the new dictionary to the transformed_data list
        transformed_data.append(new_entry)
    return transformed_data


data_list = get_data()

def chaikin_money_flow(data) -> pd.DataFrame:
    # calculete Chaikin Money Flow

    # Calculate Money Flow Multiplier
    df["mfm"] = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / np.where(
        df["high"] != df["low"], df["high"] - df["low"], 1
    )

    # Calculate Money Flow Volume
    df["mfv"] = df["mfm"] * df["volume"]

    # Calculate 20-period CMF
    volume_sum = df["volume"].rolling(window=20, min_periods=1).sum()
    df["cmf"] = np.where(
        volume_sum != 0, df["mfv"].rolling(window=20, min_periods=1).sum() / volume_sum, 0
    )
    return df

df = pd.DataFrame(data_list)
df = chaikin_money_flow(df)

# Calculate 30-period moving average
df["ma30"] = df["close"].rolling(window=30, min_periods=1).mean()

# df.round(2)


# st.line_chart(df, x="datetime", y="close")
data_list = df.to_dict("records")

# print(data_list)
chartOptions = {
    "height": 690,
    "layout": {"textColor": "black", "background": {"type": "solid", "color": "white"}},
    "watermark": {
        "visible": True,
        "fontSize": 48,
        "horzAlign": "center",
        "vertAlign": "center",
        "color": "rgba(171, 71, 188, 0.3)",
        "text": symbol,
    },
}

# print(df)
seriesCandlestickChart = [
    {
        "type": "Candlestick",
        "data": data_list,
        "options": {
            "upColor": "#26a69a",
            "downColor": "#ef5350",
            "borderVisible": False,
            "wickUpColor": "#26a69a",
            "wickDownColor": "#ef5350",
        },
    },
    {
        "type": "Line",
        "data": df[["time", "ma30"]]
        .rename(columns={"ma30": "value"})
        .to_dict("records"),
        "options": {
            "color": "blue",
        },
    },
    {
        "type": "Histogram",
        "data": df[["time", "cmf"]].rename(columns={"cmf": "value"}).to_dict("records"),
        "options": {
            "color": "#26a69a",
            "priceFormat": {
                "type": "volume",
            },
            "priceScaleId": "",  # set as an overlay setting,
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0.7,
                "bottom": 0,
            }
        },
    },
]

st.subheader(f"Candlestick Chart for {symbol}")

renderLightweightCharts(
    [{"chart": chartOptions, "series": seriesCandlestickChart}], "priceAndVolume"
)
