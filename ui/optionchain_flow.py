import logging
import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import schwabdev


from src.get_optionchains import Get_option_chain

filename = os.path.basename(__file__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(filename)s] -  %(message)s",
)


st.set_page_config(layout="wide")

if "stage" not in st.session_state:
    st.session_state.stage = 0


# Stage function to update the stage saved in session state
def set_stage(stage):
    st.session_state.stage = stage


if "current_price" not in st.session_state:
    st.session_state.current_price = ""

if "chain_list" not in st.session_state:
    st.session_state.chain_list = pd.DataFrame()

if "netPercentChange" not in st.session_state:
    st.session_state.netPercentChange = ""


@st.cache_resource
def get_client(name="A"):
    global client

    load_dotenv()
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")
    client = schwabdev.Client(app_key, app_secret, show_linked=False)
    # print(client.accounts.accountNumbers().json())
    client.update_tokens_auto()  # update tokens automatically (except refresh token)
    st.session_state.client = client
    return client


left_column, right_column = st.columns(2)


def get_symbol_chain():

    form = left_column.form(key="get_symbol")
    symbol = form.text_input("Enter symbol")
    filter = form.checkbox(
        "Filter", value=True, help="Filter option chains( bidsize, spread size)"
    )
    sigma = form.selectbox("Sigma filter", options=["No Sigma", 1, 2, 2.5, 3], index=3)
    submit = form.form_submit_button("Submit")

    if submit:
        symbol = symbol.upper()
        symbol = symbol.strip()
        get_symbol_data(symbol, filter, sigma)


# @st.cache_resource
def get_data(symbol, filter, sigma):
    client = get_client("schwab")
    get_option_chain = Get_option_chain(client)
    print(filter)
    get_option_chain.filter_optionchains = filter
    data = get_option_chain.get_options(symbol, sigma)
    current_price = get_option_chain.symbol_price
    return data, current_price, get_option_chain.netPercentChange


def get_symbol_data(symbol, filter=True, sigma=1):
    data, current_price, netPercentChange = get_data(symbol, filter, sigma)
    st.session_state.current_price = current_price
    st.session_state.netPercentChange = netPercentChange
    if st.session_state.current_price == 0:
        st.markdown(f"Symbol '{symbol}' Not found")
        return
    st.session_state.chain_list = data


def color_survived(val):
    color = "green" if val > 0 else "red"
    return f"background-color: {color}"


def dataframe_with_selections(init_value: bool = False) -> pd.DataFrame:
    if st.session_state.current_price == 0:
        # st.markdown(f"Symbol '{symbol}' Not found")
        return
    right_column.markdown(f"**Current price:** ***{st.session_state.current_price}***")
    right_column.markdown(
        f"**Precent changed for today price: {st.session_state.netPercentChange}**"
    )
    df = st.session_state.chain_list
    if len(df) == 0:
        return ""

    df_with_selections = df.copy()

    df_with_selections.insert(0, "Select", init_value)
    df_with_selections.style.apply(lambda x: "background-color: red")
    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        # disabled=True,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        # disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    if len(selected_rows) >= 1:

        a = selected_rows.drop("Select", axis=1)
        st.write("Create order for selection:")
        st.write(a)
        st.session_state.created_order = a
        st.session_state.stage = 2
    else:
        st.session_state.stage = 1


get_symbol_chain()
selection = dataframe_with_selections()


def set_stage(stike):

    dictionary = Contract.dataframe_row_to_dict(stike)
    # values = stike.values.tolist()
    # keys = stike.columns.values.tolist()
    # dictionary = dict(zip(keys, values[0]))

    contract = Contract(**dictionary)
    logging.info(f"Contract create for strike {contract} ")
    buy = BuySellStrategy(contract=contract, client=get_client("schwab"))
    st.session_state.stage = 2
    res = buy.trade_option()
    logging.info(f"Result of sell contract  {res} ")
    st.write(res)


if st.session_state.stage > 1:

    stike = st.session_state.created_order
    st.dataframe(stike)
    st.write("Selling one Option ")
    # logging.info(f"Before Submitting sell  {stike['symbol']} ")
    st.button("Submit sell ", on_click=set_stage, args=[stike])

if st.session_state.stage > 2:
    st.write("Selling one share")
