'''
Created on 28 mars 2017

@author: Alexandre
'''

#! /usr/bin/env python
# -*- coding: utf-8 -*-

# this example shows how to get quotes for multiple contracts at the
# same time and how to tell which is which by using a different
# tickerId for each one

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep

# print all messages from TWS
def watcher(msg):
    print(msg)

# show Bid and Ask quotes
def my_BidAsk(msg):
    if msg.field == 1:
        print('%s:%s:bid: %s' % (contractDict[msg.tickerId][0],
                       contractDict[msg.tickerId][6], msg.price))
    elif msg.field == 2:
        print('%s:%s:ask: %s' % (contractDict[msg.tickerId][0],
                       contractDict[msg.tickerId][6], msg.price))

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    #print 'Contract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple
    return newContract

contractDict = {}
# Note: Option quotes will give an error if they aren't shown in TWS
 # a stock
contractDict[1] = ('QQQQ', 'STK', 'SMART', 'USD', '', 0.0, '')
# another stock
contractDict[2] = ('SPY', 'STK', 'SMART', 'USD', '', 0.0, '')
# a stock option contract
contractDict[3] = ('QQQQ', 'OPT', 'SMART', 'USD', '20091218', 45.0, 'CALL')
# a futures contract
contractDict[4] = ('ES', 'FUT', 'GLOBEX', 'USD', '200912', 0.0, '')
# a futures option contract
contractDict[5] = ('ES', 'FOP', 'GLOBEX', 'USD', '20091218', 1100.0, 'CALL')
# a forex contract
contractDict[6] = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')

if __name__ == '__main__':
    con = ibConnection()
    con.registerAll(watcher)
    showBidAskOnly = True  # set False to see the raw messages
    if showBidAskOnly:
        con.unregister(watcher, message.TickSize, message.TickPrice,
                       message.TickString, message.TickOptionComputation)
        con.register(my_BidAsk, message.TickPrice)
    con.connect()
    sleep(1)
    print('* * * * REQUESTING MARKET DATA * * * *')
    for tickId in range(1,7):
        stkContract = makeStkContract(contractDict[tickId])
        con.reqMktData(tickId, stkContract, '', False)
    sleep(30)
    print('* * * * CANCELING MARKET DATA * * * *')
    for tickId in range(1,7):
        con.cancelMktData(tickId)
    sleep(1)
    con.disconnect()
    sleep(1)
