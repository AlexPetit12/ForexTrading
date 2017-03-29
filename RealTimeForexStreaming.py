'''
Created on 27 mars 2017

@author: Alexandre
'''

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from queue import Queue, Empty
from time import time, sleep
import threading


symbols = ["AUDUSD", "EURUSD", "GBPUSD", "USDCAD", "USDCHF", "USDJPY", "GBPJPY", "EURJPY"]
q = [None] * len(symbols)

def writer_thread_func(symbol_index):
    global symbols, q
    symbol = symbols[symbol_index]

    while True:
        try:
            (time, price) = q[symbol_index].get(True, 15)
            print(symbol, time, price)
        except Empty:
            print("no data for 15 seconds")

def my_callback(msg):
    global symbols, q
    if isinstance(msg, message.tickPrice):
        q[msg.tickerId].put_nowait((time(), msg.price))


def make_contract(symbol, sectype, exchange, currency, expiry, strike, right):
    cont = Contract()
    cont.m_symbol = symbol
    cont.m_secType = sectype
    cont.m_exchange = exchange
    cont.m_currency = currency
    cont.m_expiry = expiry
    cont.m_strike = strike
    cont.m_right = right
    return cont

con = ibConnection('127.0.0.1', 7497, 100)
con.registerAll(my_callback)
con.connect()

req_id = 0
for symbol in symbols:

    q[req_id] = Queue(0)
    t = threading.Thread(target=writer_thread_func, args=(req_id, ))
    t.daemon = True
    t.start()
    symbol_contract = make_contract(symbol[0:3], 'CASH', 'IDEALPRO', symbol[3:6], '', 0.0, '')
    con.reqMktData(req_id, symbol_contract, '', False)
    req_id += 1

sleep(10)