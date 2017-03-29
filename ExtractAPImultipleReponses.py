'''
Created on 25 mars 2017

@author: Alexandre
'''

from __future__ import print_function #I'm using 3.x style print
import pandas as pd

#better to read these from a file
contracts = pd.DataFrame([
        ['IBM','SMART','USD'],
        ['AAPL','SMART','USD'],
        ['GOOG','SMART','USD'],
        ['ES','GLOBEX','USD','201506','50'],
        ['CL','NYMEX','USD','201506','1000']
])

# make decent column names
contracts.columns = ['sym','exch','curr','expiry','mult']

#add these specific column names to match the name returned by TickType.getField()
contracts['bidPrice'] = 0
contracts['askPrice'] = 0
contracts['lastPrice'] = 0

from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType as tt
from time import sleep

def error_handler(msg):
    print (msg)

def my_callback_handler(msg):
    if msg.field in [tt.BID,tt.ASK,tt.LAST]:
        #now we can just store the response in the data frame
        contracts.loc[msg.tickerId,tt.getField(msg.field)] = msg.price
        if msg.field == tt.LAST:
            print(contracts.loc[msg.tickerId,'sym'],msg.price)

tws = ibConnection()
tws.register(my_callback_handler, message.tickPrice, message.tickSize)
# tws.register(error_handler, 'Error')
tws.connect()

for index, row in contracts.iterrows():
    c = Contract()
    c.m_symbol = row['sym']
    c.m_exchange = row['exch']
    c.m_currency = row['curr']
    c.m_secType = 'STK' if row['expiry'] is None else 'FUT'
    c.m_expiry = row['expiry']
    c.m_multiplier = row['mult']
    # the tickerId is just the index in but for some reason it needs str()
    tws.reqMktData(str(index),c,"",False)
sleep(10)
tws.disconnect()