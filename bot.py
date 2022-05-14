import traceback
from datetime import datetime
import os
import json
import pandas as pd
import plotly.graph_objects as go
import requests
import time
from client import FtxClient
import data

# [welcome to the infinite money printer]
# this is a cryptocurrency trading bot developed
# and maintained by Nyria LLC at
# github.com/xozxro/cryptogobrr
#
# feel free to fork and edit as you please.
#
# [nyriabot.io]

class tradebot():

    def __init__(self):

        print('[TRADEBOT] initializing trading bot...')

        # API KEY
        self.apiKey = data.apiKey

        # API SECRET
        self.apiSecret = data.apiSecret

        try:

            self.ftx_client = FtxClient(
                api_key=self.apiKey,
                api_secret=self.apiSecret
            )
            print('[TRADEBOT] SUCCESSS building trading bot.')

        except Exception as exception:

            print('[TRADEBOT] ERROR building trading bot.')
            traceback.print_exc()


        # set up variables
        self.openTrades = {}
        self.buyOrders = {}
        self.sellOrders = {}
        self.triggerEvents = {}

        self.accountBalance = self.ftx_client.get_total_usd_balance()
        print('[TRADEBOT] account balance: $' + str(self.accountBalance))


    def getPrice(self, coin):

        return None

    def placeOrder(self, coin, type, price):

        return None

    def getAccountInfo(self, type=None):

        return None


