import os

import pandas as pd
from get_optionchains import Get_option_chain
from dotenv import load_dotenv
import streamlit as st
import schwabdev

load_dotenv()
client: schwabdev.Client = None

left_column, right_column = st.columns(2)

if "stage" not in st.session_state:
    st.session_state.stage = 0

if "chain_list" not in st.session_state:
    st.session_state.chain_list = pd.DataFrame()

    
def sell_option(stike):
    # just print the stike you need to implemnt to buy flow.
    print(stike)
    

def start_flow():

    form = left_column.form(key="get_symbol")
    symbol = form.text_input("Enter symbol")
    submit = form.form_submit_button("Submit")

    if submit:
        symbol = symbol.upper()
        symbol = symbol.strip()
        process_symbol(symbol)

def process_symbol(symbol):
    display_quote(symbol)
    data = fetch_option_chain(symbol)
    st.session_state.chain_list = data

def display_quote(symbol):
    response = get_client().quote(symbol, "regular").json()
    right_column.markdown(f"Symbol: {symbol}")
    
    
    # right_column.table(response[symbol]["regular"])
    last_price = response[symbol]["regular"]["regularMarketLastPrice"]
    market_change = response[symbol]["regular"]["regularMarketNetChange"]
    right_column.markdown(f"Last Price: {last_price}")
    right_column.markdown(f"Market Change: {market_change}")


def display_and_select_options(init_value: bool = False) -> pd.DataFrame:
    """
    This function takes the option chain data for a given symbol and displays it in a dataframe. The dataframe includes a checkbox column that allows the user to select one or more options. When the user selects an option, the function stores the selected option in the session state and updates the stage of the application to 2. If the user does not select an option, the function updates the stage of the application to 1.
    """
    data = st.session_state.chain_list
    if len(data) == 0:
        print("No option chain found for symbol")
        return ""
    df_with_selections = data.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    if len(selected_rows) >= 1:

        row = selected_rows.drop("Select", axis=1)
        st.write("Create order for selection:")
        st.write(row)
        st.session_state.created_order = row
        st.session_state.stage = 2
        
    else:
        st.session_state.stage = 1
    print("order selection")

def fetch_option_chain(symbol):
    get_option_chain = Get_option_chain(get_client())
    get_option_chain.filter_options = True
    data = get_option_chain.get_options(symbol)
    return data




@st.cache_resource
def get_client():
    load_dotenv()
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")
    client = schwabdev.Client(app_key, app_secret, show_linked=False)
    # print(client.accounts.accountNumbers().json())
    client.update_tokens_auto()  # update tokens automatically (except refresh token)
    st.session_state.client = client
    return client



start_flow()
selection = display_and_select_options()

if st.session_state.stage > 1:
    stike = st.session_state.created_order
    # st.dataframe(stike)
    st.write("Selling one Option ")
    st.button("Submit sell ", on_click=sell_option, args=[stike])
    
