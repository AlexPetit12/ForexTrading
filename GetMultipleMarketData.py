'''
Created on 28 mars 2017

@author: Alexandre
'''

#! /usr/bin/env python
# -*- coding: utf-8 -*-

# get quotes for multiple contracts
# using a different tickerId for each one

from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep

# print all messages from TWS
def watcher(msg): print(msg)

# choose which price quotes to print
def printQuote(msg):
    qtype = "nada"
    if msg.field == 1: qtype = "bid"
    if msg.field == 2: qtype = "ask"
    if msg.field == 4: qtype = "last"
    if msg.field == 9: qtype = "close"

    if qtype != "nada":
        optstring = ""
        if float(contractDict[msg.tickerId][5]) > 0.001:
            optlist = []
            optlist.append(str(contractDict[msg.tickerId][4]))
            optlist.append(" ")
            optlist.append(str(contractDict[msg.tickerId][5]))
            optlist.append(" ")
            optlist.append(contractDict[msg.tickerId][6])
            optstring = ''.join([s for s in optlist])
        print( '%s: %s: %s: %s: %s' % (contractDict[msg.tickerId][1],
                contractDict[msg.tickerId][0], optstring, qtype, msg.price))

def makeContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    if len(contractTuple) > 7:
        if contractTuple[1] == "OPT":
            newContract.m_multiplier = contractTuple[7]
    return newContract

if __name__ == '__main__':

    contractDict = {}
    # a stock
    contractDict[0] = ('QQQ', 'STK', 'SMART', 'USD', '', 0.0, '')
    # another stock
    contractDict[1] = ('SPY', 'STK', 'SMART', 'USD', '', 0.0, '')
    # a stock option contract
    contractDict[2] = \
        ('QQQ', 'OPT', 'SMART', 'USD', '20121221', 65.0, 'CALL', 100)
    # a futures contract
    contractDict[3] = ('ES', 'FUT', 'GLOBEX', 'USD', '201212', 0.0, '')
    # a futures option contract
    contractDict[4] = \
        ('ES', 'FOP', 'GLOBEX', 'USD', '20121221', 1400.0, 'PUT')
    # a forex contract
    contractDict[5] = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')

    con = ibConnection()
    con.registerAll(watcher)
    showPrintQuotesOnly = True  # set False to see lots of tick messages
    if showPrintQuotesOnly:
        con.unregister(watcher, (message.tickSize,),
                        (message.tickPrice,),
                        (message.tickString,),
                        (message.tickOptionComputation,))
        con.register(printQuote, (message.tickPrice,))
    con.connect()
    sleep(.1)
    print('\n* * * * REQUESTING 10 SECONDS OF MARKET DATA * * * *\n')
    for tickId in range(len(contractDict)):
        stkContract = makeContract(contractDict[tickId])
        con.reqMktData(tickId, stkContract, '', False)
    sleep(10)
    print('\n* * * * CANCELING MARKET DATA * * * *')
    for tickId in range(len(contractDict)):
        con.cancelMktData(tickId)
        sleep(.1)
    con.disconnect()
    sleep(.1)
