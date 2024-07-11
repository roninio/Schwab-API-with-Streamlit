import json
import pandas as pd
import streamlit as st

# from menu import menu_with_redirect
from src.client import get_client
from src.account import AccountInfo

st.title("Account details")


def _get_account_class():
    client = get_client()
    ac = AccountInfo(client)
    return ac


def _get_client():

    account_number = _get_account_class().account
    st.write("Account number:", account_number)


from collections.abc import MutableMapping


def flatten_list(lst):
    result = []
    for i in lst:
        if isinstance(i, list):
            result.extend(flatten_list(i))
        else:
            result.append(i)
    return result


def orders():
    orders = _get_account_class().get_orders(days_to_lookback=12)
    # print(type(orders))
    # print(orders)
    if "message" in orders:
        orders = "No orders found on account"
        return
    # print(orders)
    # return
    if orders == None or len(orders) == 0:
        orders = "No orders found on account"
        # st.write(orders)
    else:
        st.markdown("### Orders")
        # data = json.loads(orders)
        # print(orders)
        # keys = ["assetType", "symbol"]
        # table = [
        #     [name] + [person[key] for key in keys] for name, person in orders.items()
        # ]
        import json

        table_data = []
        from tabulate import tabulate

        for x in orders:
            keys = x.keys()
            #     print(keys)
            values = x.values()

            #     print((values))
            #     # flattened_data = flatten_list(list(values))
            #     # print(flattened_data)
            #     # Convert dict_keys and dict_values to lists
            keys_list = list(keys)
            values_list = list(values)

            #     # Iterate over the elements
            #     for i in range(len(keys_list)):
            #         key = keys_list[i]
            #         value = values_list[i]
            #         # Do something with the key and value
            #         print(f"Key: {key}, Value: {value}")
            #     return

            table_data.append(values_list)
        #     # print(values)
        # keys = orders[0].keys()
        # print(keys)
        df = pd.DataFrame(table_data)
        df = df[~df.iloc[:, 11].apply(lambda x: isinstance(x, list))]

        st.table(df)
        return
        df = pd.DataFrame(v)
        st.table(df)
        return
        from tabulate import tabulate

        data = orders
        # Define the keys you want to include in the table
        a = []
        for o in orders:
            b = {}
            b["orderId"] = o["orderId"]
            if "orderLegCollection" in o:

                b["assetType"] = o["orderLegCollection"][0]["instrument"]["assetType"]
                b["symbol"] = o["orderLegCollection"][0]["instrument"]["symbol"]
                b["description"] = o["orderLegCollection"][0]["instrument"][
                    "description"
                ]
                if "enteredTime" in o["orderLegCollection"][0]["instrument"]:
                    b["enteredTime"] = o["orderLegCollection"][0]["instrument"][
                        "enteredTime"
                    ]
                if "enteredTime" in o:
                    b["enteredTime"] = o["enteredTime"]
                # if "status" in o["orderLegCollection"][0]["instrument"]:
                if "status" in o:
                    b["status"] = o["status"]
                # if "status" in o["orderLegCollection"][0]["instrument"]:
                # b["status"] = o["orderLegCollection"][0]["orderStatus"]
                # o["statusDescription"] = o["orderLegCollection"][0]["orderStatusDescription"]

                # print(o)

            a.append(b)
        st.table(a)


_get_client()
orders()
