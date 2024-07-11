import json
import logging
import schwabdev


class SubmitOrders:

    client = None
    account_hash = None
    order_id = None

    def __init__(self, client: schwabdev.Client):
        self.client = client

    def get_order(self, order_id, account_hash):
        # get specific order details
        print("|\n|client.order_details(account_hash, order_id).json()", end="\n|")
        res = self.client.order_details(account_hash, order_id).json()
        return res

    def place_order(
        self,
        symbol,
        account_hash,
        price,
        instruction,
        quantity=1,
    ):

        # place order
        order = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "price": price,
            "orderLegCollection": [
                {
                    "instruction": instruction,
                    "quantity": quantity,
                    "instrument": {
                        "symbol": "{symbol}".format(symbol=symbol),
                        "assetType": "OPTION",
                    },
                }
            ],
        }
        # print(order)
        # exit()
        resp = self.client.order_place(account_hash, order)
        print(resp)
        print("|\n|client.order_place(self.account_hash, order).json()", end="\n|")
        print(f"Response code: {resp}")
        # get the order ID - if order is immediately filled then the id might not be returned
        order_id = resp.headers.get("location", "/").split("/")[-1]
        self.order_id = order_id
        print(f"Order id: {order_id}")
        return order_id

    def cancel_order(self, order_id, account_hash):
        # cancel specific order
        print("|\n|client.order_cancel(self.account_hash, order_id).json()", end="\n|")
        respone = self.client.order_cancel(account_hash, order_id)
        if respone.status_code == 200:
            logging.info(f"Cancel order successful. {order_id} ")
            return True
        else:
            logging.info(f"Cancel order unsuccessful. {order_id} ")
            return False
