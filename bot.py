import traceback
from datetime import datetime
import os
import json
import pandas as pd
import plotly.graph_objects as go
import requests
import time

from discord_webhook import DiscordWebhook, DiscordEmbed

from client import FtxClient
import data
import yfinance as yf

# [welcome to the infinite money printer]
# this is a cryptocurrency trading bot developed
# and maintained by Nyria LLC at
# github.com/xozxro/cryptogobrr
#
# feel free to fork and edit as you please.
#
# [nyriabot.io]\




def getMarketData(avgprices, volumes, interval='1m'):




    # download data from yh finance
    running = True
    while running:

        try:
            data = yf.download(tickers='ETH-USD', period='1d', interval=interval, threads=False, progress=False)
            running = False

        except:

            try:
                if interval == '1m':
                    data = yf.download(tickers='ETH-USD', period='5d', interval=interval, threads=False, progress=False)
                    running = False
                else:
                    time.sleep(5)
                    data = yf.download(tickers='ETH-USD', period='1d', interval=interval, threads=False, progress=False)
                    running = False

            except Exception as exception:
                traceback.print_exc()
                time.sleep(10)

    # handle with dataframe
    df = data.iloc[::-1]

    # sort data
    stockOpen, high, low, close, volume = df['Open'].iloc[0], df['High'].iloc[0], df['Low'].iloc[0], df['Close'].iloc[0], df['Volume'].iloc[1]




    ####################################
    ############## calculate VWAP
    open_last, high_last, low_last, close_last, volume_last = df['Open'].iloc[1], df['High'].iloc[1], df['Low'].iloc[1], df['Close'].iloc[1], df['Volume'].iloc[1]

    now = datetime.now()
    minute = now.strftime("%M")
    hour = now.strftime("%H")

    # sum all to calculate indicators <<<< --

    # here count how many volumes were not 0

    trueVol = 0
    if volumes == []:

        # if market just opened, only want todays data

        # deal with getting as many minutes as possible but not spilling into previous session for first 1 hour

        for x in range(0,len(data)):
            try:

                newDF = data

                open_last, high_last, low_last, close_last, volume_last = newDF['Open'].iloc[x], newDF['High'].iloc[x], \
                                                                          newDF['Low'].iloc[x], newDF['Close'].iloc[x], \
                                                                          newDF['Volume'].iloc[x]
                avgprice = (high_last + low_last + close_last) / 3

                if volume_last == 0:
                    volume_last = 1
                pv = avgprice * volume_last

                avgprices.append(pv)
                volumes.append(volume_last)

            except:
                pass
    else:
        avgprice = (high + low + close) / 3

        pv = avgprice * volume_last

    VWAPList = (data['Volume'] * (data['High'] + data['Low']) / 2).cumsum() / data['Volume'].cumsum()

    VWAP = VWAPList[-1]




    ####################################
    ############## calculate strength indexes

    # RSI

    window_length = 14

    close_delta = data['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    # Calculate the EWMA
    # Use exponential moving average
    ma_up = up.ewm(com=14 - 1, adjust=True, min_periods=14).mean()
    ma_down = down.ewm(com=14 - 1, adjust=True, min_periods=14).mean()

    # Calculate the RSI based on EWMA
    rsiA = ma_up / ma_down
    rsiList = 100 - (100 / (1 + rsiA))

    rsi = rsiList[-1]

    # STOCH
    STOCH = 0




    ####################################
    ############## calculate EMAs
    ema12 = data['Close'].ewm(span=9, adjust=False).mean()
    ema26 = data['Close'].ewm(span=21, adjust=False).mean()
    ema5 = data['Close'].ewm(span=8, adjust=False).mean()




    ####################################
    ############## calculate MACD

    k = data['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = data['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s




    currentema12 = ema12[-1]
    currentema26 = ema26[-1]
    currentema5 = ema5[-1]

    currentmacd = macd[-1]
    currenthisto = macd_h[-1]




    # RETURN ALL

    return {'stockOpen': stockOpen, 'high': high, 'low': low, 'close': close, 'volume': volume, 'RSI': rsi, 'MACD': currentmacd, 'VWAP': VWAP, 'STOCH': STOCH, 'histogram': currenthisto, 'ema12': currentema12, 'ema26': currentema26, 'avgprices': avgprices, 'avgprice': avgprice, 'volumes': volumes, 'macdlist': macd_s, 'ema12list': ema12, 'ema26list': ema26, 'ema5': currentema5}



class tradebot():


    def __init__(self):

        print('[TRADEBOT] initializing trading bot...')

        # API KEY
        self.apiKey = data.apiKey

        # API SECRET
        self.apiSecret = data.apiSecret

        try:

            self.client = FtxClient(
                api_key=self.apiKey,
                api_secret=self.apiSecret
            )
            print('[TRADEBOT] SUCCESS building trading bot.')

        except Exception as exception:

            print('[TRADEBOT] ERROR building trading bot.')
            traceback.print_exc()


        # set up variables
        self.openTrades = {}
        self.buyOrders = {}
        self.sellOrders = {}
        self.triggerEvents = {}
        self.url = data.discordwebhook
        self.watching = False

        if data.devMode:
            self.accountBalance = 10000
        else:
            self.accountBalance = self.client.get_total_usd_balance()

        self.startingBal = self.accountBalance

        print('[TRADEBOT] account balance: $' + str(self.accountBalance))


    def getPrice(self, avgprices, volumes, interval='1m', coin='ETH/USD'):

        self.price = getMarketData(avgprices, volumes, interval=interval)

        return self.price


    def placeOrder(self, coin, type):

        success = False
        # actual purchase code will be here
        price = self.price

        if success:
            if type == 'BUY':
                self.accountBalance -= price

            else:
                print('[TRADEBOT] placing SELL order at ' + str(price))
                self.accountBalance += price

        return success,price


    def getAccountInfo(self, type=None):

        # to do - will allow bot to handle positions and orders
        return None


    def pushDiscordNotif(self, url, type=''):

        try:

            if type == 'watching' or self.watching:
                color = '3464eb'
                title = '[Trading Bot] | [READY]'
                desc = '**Now watching $ETH for a scalp due to an oversold dip.**'

            if type == 'sell':
                color = 'eb3453'
                title = '[Trading Bot] | [SOLD]'
                desc = '**Placed a SELL order @ ' + str(self.price) + '**'

            if type == 'buy':
                color = '03fca9'
                title = '[Trading Bot] | [PURCHASED]'
                desc = '**Placed a LONG order @ ' + str(self.price) + '**'


            if type == 'start_msg':
                color = '53eb34'
                title = '[Trading Bot] | Enabled.'
                desc = ''


            webhook = DiscordWebhook(url=self.url, username='Nyria', content='')
            embed = DiscordEmbed(title=title, description=desc, color=color)
            embed.add_embed_field(name='Time', value=str(time.strftime("%H:%M")))


            if type != 'start_msg':
                embed.add_embed_field(name='Price', value='$' + str(self.price))

                if type == 'sell':
                    embed.add_embed_field(name='New Balance', value='**$' + str(self.accountBalance) + '**')

                    gain = self.accountBalance - self.startingBal

                    if gain < 0:
                        gain = '** -$' + str(gain) + '**'

                    if gain > 0:
                        gain = '** +$' + str(gain) + '**'

                    else:
                        gain = 0

                    embed.add_embed_field(name='Day Gain', value=gain)

            else:
                embed.add_embed_field(name='Balance', value='**$' + str(self.accountBalance) + '**')

            webhook.add_embed(embed)
            response = webhook.execute()

            return response

        except Exception as exception:

            traceback.print_exc()

            return traceback.format_exc()




