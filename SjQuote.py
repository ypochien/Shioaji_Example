import sys
import os
from multiprocessing import Event
from dotenv import load_dotenv
import rich
import shioaji
from shioaji.constant import QuoteType

load_dotenv()
"""
QUT/idcdmzpcr01/TSE/2330
{
    'AskPrice': [594.0, 595.0, 596.0, 597.0, 598.0],
    'AskVolume': [1272, 1496, 776, 586, 761],
    'BidPrice': [593.0, 592.0, 591.0, 590.0, 589.0],
    'BidVolume': [901, 1251, 861, 1534, 317],
    'Date': '2021/03/30',
    'Time': '12:09:29.463610'
}
MKT/idcdmzpcr01/TSE/2330
{
    'AmountSum': [10811130000.0],
    'Close': [594.0],
    'Date': '2021/03/30',
    'TickType': [1],
    'Time': '12:09:28.074703',
    'VolSum': [18143],
    'Volume': [2]
}
"""


def cb_quote(topic, msg):
    rich.print(topic, msg)


def main():
    simulation = os.environ.get("SIMULATION").lower() in ["true", "1"]
    login_id = os.environ.get("ID")
    login_password = os.environ.get("PASSWORD")

    rich.print("登入模擬環境") if simulation else rich.print("登入正式環境")

    api = shioaji.Shioaji(simulation=simulation)
    api.login(login_id, login_password)
    api.quote.set_quote_callback(cb_quote)
    api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type=QuoteType.Tick)
    api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type=QuoteType.BidAsk)
    Event().wait()


if __name__ == "__main__":
    sys.exit(main())
