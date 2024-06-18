import json
from datetime import datetime, timedelta
import pandas as pd
import os
import schwabdev
import numpy as np

os.environ["PYDEVD_INTERRUPT_THREAD_TIMEOUT"] = "30"

import math

symbol_price = 0






class Get_option_chain:

    client: schwabdev.Client = None
    symbol_price = 0
    netPercentChange = 0
    filter_options = True

    def __init__(self, client) -> None:
        self.client = client
   
    def _filter_data(self, b):
        """Filter rows not relevant return true to filter the row"""
      
        if b["inTheMoney"] == True:
            return True
        if b["bidSize"] < 10 or b["askSize"] < 10:
            return True
      
    def _create_options_list(self, data, filter=True):
        df = pd.DataFrame()
        callExpDateMap = list(data)
        for extDate in callExpDateMap:
            for a in data[extDate]:
                for b in data[extDate][a]:
                    if self.filter_options == True:
                        if self._filter_data(b) == True:
                            continue

                    b["experationDate"] = extDate
                    b["optionDeliverablesList"] = 0
                    
                    if len(df) == 0:
                        df = pd.DataFrame(b, index=[0])
                    else:
                        df.loc[len(df)] = b
        return df

    def get_symbol(self, symbol="SOFI"):
        try:
            symbol_res = self.client.quote(symbol).json()
            print("Percentage change", symbol_res[symbol]["quote"]["netPercentChange"])
            return symbol_res[symbol]["quote"]["netPercentChange"]
        except:
            return "error try again " + symbol

    def get_option(self, **kwargs) -> pd:

        pass

    def get_options(self, symbol="SOFI", numdays_start= 0, numdays_end=30) -> pd:
        global symbol_price
        symbol = symbol.upper()
        symbol = symbol.strip()

        netPercentChange = self.get_symbol(symbol=symbol)

        today = datetime.now()
        future_date = today + timedelta(days=numdays_start)
        future_date = future_date.strftime("%Y-%m-%d")

        toDate = today + timedelta(days=numdays_end)
        toDate = toDate.strftime("%Y-%m-%d")
        print(future_date, toDate)
        try:
            res = self.client.option_chains(
                symbol=symbol, fromDate=future_date, toDate=toDate
            ).json()
            symbol_price = res["underlyingPrice"]
            print(res["symbol"], symbol_price)
            call_options = res["callExpDateMap"]
            put_options = res["putExpDateMap"]
            call_df = self._create_options_list(call_options)
            puts_df = self._create_options_list(put_options)
            frames = [call_df, puts_df]
            if len(frames) == 0 or (len(call_df) == 0 and len(puts_df) == 0):
                print("No Strikes found")
                return pd.DataFrame([["No striks found "]], columns=["Result"])

        except Exception as e:  # Catches any other exception
            print("Unexpected error:", e)
            return "Error found"

        columns_to_print = [
            "symbol",
            "putCall",
            "strikePrice",
            "experationDate",
            "bid",
            "ask",
            "bidSize",
            "askSize",
            "daysToExpiration",
            "intrinsicValue",
        ]
        frames1 = pd.concat(frames)
        
        
        return frames1[columns_to_print]
