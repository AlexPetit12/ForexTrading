'''
Created on 30 mars 2017

@author: Alexandre
'''

from datetime import datetime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from queue import Queue, Empty
from time import ctime, time, sleep
import threading

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

class Stream:
    def __init__(self, IP, port, clientID, symbols):
        self.IP = IP
        self.port = port
        self.clientID = clientID
        self.symbols = symbols
        self.q = [None] * len(symbols)
                
        self.con = ibConnection(IP, port, clientID)
        self.con.registerAll(self.my_callback)
        self.con.connect()
        
    def my_callback(self, msg):
        if isinstance(msg, message.tickPrice):
            self.q[msg.tickerId].put_nowait((datetime.now().strftime('%Y-%d-%m %H:%M:%S'), msg.price))
            
            
    def writer_thread_func(self, symbol_index):
        symbol = self.symbols[symbol_index]
        while True:
            try:
                (time, price) = self.q[symbol_index].get(True, 15)
                print(symbol, time, price)
            except Empty:
                print("no data for 15 seconds")

    def start(self):
        req_id = 0
        for symbol in self.symbols:
        
            self.q[req_id] = Queue(0)
            t = threading.Thread(target=self.writer_thread_func, args=(req_id, ))
            t.daemon = True
            t.start()
            symbol_contract = make_contract(symbol[0:3], 'CASH', 'IDEALPRO', symbol[3:6], '', 0.0, '')
            self.con.reqMktData(req_id, symbol_contract, '', False)
            req_id += 1  
        
IP = '127.0.0.1'
port= 7497
clientId = 100
symbols = ["AUDUSD", "EURUSD", "GBPUSD", "USDCAD", "USDCHF", "USDJPY", "GBPJPY", "EURJPY"]

S = Stream(IP, port, clientId, symbols)
S.start()

sleep(20)