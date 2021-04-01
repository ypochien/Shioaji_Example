import sys
import os
from multiprocessing import Event
from dotenv import load_dotenv
import rich
import pandas as pd
import dolphindb
import datetime as dt
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
ddb = dolphindb.session()
ddb.connect("localhost", 8848, "admin", "123456")

api = None


def cb_quote(topic, quote):
    # print(topic, quote)
    if topic.startswith("QUT"):
        _, _, _, code = topic.split("/")
        # one = {
        #     "AskPrice1": quote["AskPrice"][0],
        #     "AskPrice2": quote["AskPrice"][1],
        #     "AskPrice3": quote["AskPrice"][2],
        #     "AskPrice4": quote["AskPrice"][3],
        #     "AskPrice5": quote["AskPrice"][4],
        #     "AskVolume1": quote["AskVolume"][0],
        #     "AskVolume2": quote["AskVolume"][1],
        #     "AskVolume3": quote["AskVolume"][2],
        #     "AskVolume4": quote["AskVolume"][3],
        #     "AskVolume5": quote["AskVolume"][4],
        #     "BidPrice1": quote["BidPrice"][0],
        #     "BidPrice2": quote["BidPrice"][1],
        #     "BidPrice3": quote["BidPrice"][2],
        #     "BidPrice4": quote["BidPrice"][3],
        #     "BidPrice5": quote["BidPrice"][4],
        #     "BidVolume1": quote["BidVolume"][0],
        #     "BidVolume2": quote["BidVolume"][1],
        #     "BidVolume3": quote["BidVolume"][2],
        #     "BidVolume4": quote["BidVolume"][3],
        #     "BidVolume5": quote["BidVolume"][4],
        #     "Date": quote["Date"],
        #     "Time": quote["Time"],
        #     "Code": code,
        #     "SimTrade": quote.get("Simtrade", 0),
        # }

        script = f"""
insert into StreamTSEQuotes values('{code}', temporalParse('{quote["Date"]}','yyyy/MM/dd'),nanotime('{quote['Time']}'),{ quote.get('Simtrade', 0)},\
{quote['AskPrice'][0]},{quote['AskPrice'][1]},{quote['AskPrice'][2]},{quote['AskPrice'][3]},{quote['AskPrice'][4]},\
{quote['AskVolume'][0]},{quote['AskVolume'][1]},{quote['AskVolume'][2]},{quote['AskVolume'][3]},{quote['AskVolume'][4]},\
{quote['BidPrice'][0]},{quote['BidPrice'][1]},{quote['BidPrice'][2]},{quote['BidPrice'][3]},{quote['BidPrice'][4]},\
{quote['BidVolume'][0]},{quote['BidVolume'][1]},{quote['BidVolume'][2]},{quote['BidVolume'][3]},{quote['BidVolume'][4]})"""
        ddb.run(script)

        # lst = [one]
        # df = pd.DataFrame.from_dict(lst, orient="columns")
        # ddb.upload({"tQuote": df})
        # ddb.run(
        #     """
        #     objByName("StreamTSEQuotes").append!(select Code,temporalParse(Date,"yyyy/MM/dd"),nanotime(Time),SimTrade,AskPrice1,AskPrice2,AskPrice3,AskPrice4,AskPrice5,AskVolume1,AskVolume2,AskVolume3,AskVolume4,AskVolume5,BidPrice1,BidPrice2,BidPrice3,BidPrice4,BidPrice5,BidVolume1,BidVolume2,BidVolume3,BidVolume4,BidVolume5 from tQuote)
        #     """
        # )
    elif topic.startswith("MKT"):
        _, _, exchange, code = topic.split("/")

        ticks = []
        now = dt.datetime.now()
        for i in range(len(quote["Close"])):
            dictMKT = {
                "Exchange": exchange,
                "SubSeq": i,
                "Date": quote.get("Date", dt.datetime.today().strftime("%Y/%m/%d")),
                "Time": quote["Time"],
                "Code": code,
                "Close": quote["Close"][i],
                "TickType": quote["TickType"][i] if quote.get("TickType", None) else 0,
                "AmountSum": quote["AmountSum"][i]
                if quote.get("AmountSum", None)
                else 0,
                "Volume": quote["Volume"][i],
                "VolSum": quote["VolSum"][i],
                "Simtrade": quote.get("Simtrade", 0),
            }
            dictMKT["ReceviceTime"] = now
            ticks.append(dictMKT)
        df = pd.DataFrame.from_dict(ticks, orient="columns")
        ddb.upload({"tTSETicks": df})
        ddb.run(
            """objByName("StreamTSETicks").append!(
                select Exchange,SubSeq,Code,temporalParse(Date,"yyyy/MM/dd"),nanotime(Time),Close,Volume,VolSum,AmountSum,TickType,int(Simtrade),ReceviceTime from tTSETicks)"""
        )


def cb_login(msg):
    rich.print(msg)
    if msg == "STK":
        sub_code = [
            "3481",
            "6116",
            "2303",
            "2409",
            "2603",
            "2324",
            "6237",
            "3707",
            "3006",
            "3037",
            "4919",
            "2338",
            "5243",
            "2317",
            "2337",
            "2323",
            "2330",
            "3576",
            "6443",
            "2344",
            "3305",
            "2401",
            "3552",
            "3189",
            "2610",
            "3149",
            "2002",
            "5299",
            "2328",
            "6138",
            "8046",
            "2352",
            "4960",
            "2615",
            "5471",
            "2891",
            "2883",
            "2618",
            "3711",
            "3169",
            "6770",
            "4968",
            "3141",
            "2436",
            "3059",
            "8358",
            "1440",
            "8936",
            "2888",
            "2356",
            "1517",
            "2454",
            "2881",
            "2882",
            "4938",
            "00881",
            "6251",
            "2006",
            "1409",
            "4952",
            "6531",
            "2108",
            "1101",
            "3322",
            "00637L",
            "3588",
            "2353",
            "2486",
            "8150",
            "2481",
            "2884",
            "3178",
            "6209",
            "3034",
            "3504",
            "2382",
            "6548",
            "6223",
            "6547",
            "2412",
            "4123",
            "6120",
            "2027",
            "2313",
            "2885",
            "2331",
            "1612",
            "1303",
            "2449",
            "3673",
            "5272",
            "6202",
            "6586",
            "6147",
            "2340",
            "8261",
            "3078",
            "6244",
            "9945",
            "2308",
        ]
        rich.print("開始訂閱")
        # sub_code = ["2330", "3406"]
        for code in sub_code:
            # api.quote.subscribe(api.Contracts.Stocks[code], quote_type=QuoteType.Tick)
            api.quote.subscribe(api.Contracts.Stocks[code], quote_type=QuoteType.BidAsk)
        rich.print("訂閱完成")


def main():
    global api
    simulation = os.environ.get("SIMULATION").lower() in ["true", "1"]
    login_id = os.environ.get("ID")
    login_password = os.environ.get("PASSWORD")

    rich.print("登入模擬環境") if simulation else rich.print("登入正式環境")

    api = shioaji.Shioaji(simulation=simulation)
    api.login(login_id, login_password, contracts_cb=cb_login)
    api.quote.set_quote_callback(cb_quote)
    Event().wait()


if __name__ == "__main__":
    sys.exit(main())
