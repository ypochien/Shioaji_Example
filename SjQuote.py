import sys
import os
from multiprocessing import Event
from dotenv import load_dotenv
import rich
import shioaji
from shioaji.constant import QuoteType

load_dotenv()


def cb_quote(topic, msg):
    rich.print(topic)
    rich.print(msg)


def main():
    api = shioaji.Shioaji()
    api.login(os.environ.get("ID"), os.environ.get("PASSWORD"))
    api.quote.set_quote_callback(cb_quote)
    api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type=QuoteType.Tick)
    api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type=QuoteType.BidAsk)
    Event().wait()


if __name__ == "__main__":
    sys.exit(main())
