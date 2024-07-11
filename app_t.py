from datetime import datetime, timedelta
import requests
import base64
import schwabdev
# from src.contract_class import Contract
from src.account import AccountInfo
# from src.orders import SubmitOrders
# from src.get_optionchains import Get_option_chain
import pandas as pd
from dotenv import load_dotenv
import os

client = None


def main():
    global client
    load_dotenv()
    app_key = os.getenv("APP_KEY")
    app_secret = os.getenv("APP_SECRET")

    client = schwabdev.Client(app_key, app_secret, show_linked=True)

    # print(client.accounts.accountNumbers().json())
    client.update_tokens_auto()  # update tokens automatically (except refresh token)

    account_info = AccountInfo(client=client)

    # account_info.get_positions()

    print("\n\nAccounts and Trading - Accounts (in Schwab API documentation)")
    print(account_info.account)
    print("|\n|client.account_details_all().json()", end="\n|")
    linked_accounts = client.account_linked().json()
    account_hash = linked_accounts[0].get("hashValue")
  


if __name__ == "__main__":
    main()
    pass
