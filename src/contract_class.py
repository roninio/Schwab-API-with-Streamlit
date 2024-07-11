from enum import Enum


class ContractType(Enum):
    CALL = "CALL"
    PUT = "PUT"


class Contract:
    putCall: ContractType = None
    bid: float = 0
    ask: float = 0
    symbol = ""
    strikePrice: float = 0
    experationDate = ""
    daysToExiration = 0
    putCall = ""

    def __init__(
        self,
        **kwargs,
    ):
        for key, value in kwargs.items():
            # print(key, value)
            setattr(self, key, value)


    def get_symbol(self):
        split = self.symbol.split(" ")
        return split[0]

    def __str__(self) -> str:
        return f"Contract {self.symbol} {self.strikePrice} (putCall={self.putCall}, bid={self.bid},ask={self.ask} )"

    def compare_to(self, other_contract):
        diff_attrs = []
        for attr in [
            "strikePrice",
            "symbol",
            "ask",
            "bid",
            "daysToExiration",
            "putCall",
        ]:
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                if getattr(self, attr) != getattr(other_contract, attr):
                    diff_attrs.append(attr)
        return diff_attrs

    @staticmethod
    def dataframe_row_to_dict(input_contract):
        """
        input is expected to be a DataFrame with a single row, and the function returns a dictionary containing the same information.
        """
        values = input_contract.values.tolist()
        keys = input_contract.columns.values.tolist()
        dictionary = dict(zip(keys, values[0]))
        return dictionary
