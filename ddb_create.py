import rich
import dolphindb as ddb

s = ddb.session()
s.connect("localhost", 8848, "admin", "123456")


# Raw Data - Stock Tick
"""
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


create_stock_tick_table = """
schemaTSETicks = streamTable(
     array(SYMBOL,0) as Exchange
    ,array(INT,0) as SubSeq
    ,array(SYMBOL,0) as Code
    ,array(DATE,0) as Date
    ,array(NANOTIME,0) as Time
    ,array(DOUBLE,0) as Close
    ,array(LONG,0) as Volume
    ,array(LONG,0) as VolSum
    ,array(LONG,0) as AmountSum
    ,array(INT,0) as TickType
    ,array(INT,0) as Simtrade
    ,array(NANOTIMESTAMP,0) as ReceviceTime
)
enableTableShareAndPersistence(table=schemaTSETicks,asynWrite=true, compress=false,cacheSize=10000, tableName="StreamTSETicks");
db = database("dfs://TSETicks",VALUE, 2021.03.30..2021.03.30)
db.createPartitionedTable(select * from StreamTSETicks,`TSETicks,`Date)
"""
if s.existsDatabase("dfs://TSETicks"):
    rich.print("dfs://TSETicks 存在")
else:
    s.run(create_stock_tick_table)
