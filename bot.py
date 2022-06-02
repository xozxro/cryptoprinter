import time
import traceback
from datetime import datetime
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
# [nyriabot.io]




def getMarketData(avgprices, volumes, interval='1m'):


    # download data from yh finance
    running = True
    while running:

        try:
            data = yf.download(tickers='SOL-USD', period='1d', interval=interval, threads=False, progress=False)
            running = False

        except:

            try:
                if interval == '1m':
                    data = yf.download(tickers='SOL-USD', period='5d', interval=interval, threads=False, progress=False)
                    running = False
                else:
                    time.sleep(5)
                    data = yf.download(tickers='SOL-USD', period='1d', interval=interval, threads=False, progress=False)
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
        self.openQT = 0
        self.gains = []

        if data.devMode:
            self.accountBalance = 10646.83
        else:
            self.accountBalance = self.client.get_total_usd_balance()

        self.startingBal = self.accountBalance

        print('[TRADEBOT] account balance: $' + str(self.accountBalance))


    def getPrice(self, avgprices, volumes, interval='1m', coin='SOL/USD'):

        self.price = getMarketData(avgprices, volumes, interval=interval)
        self.priceNum = round(self.price['close'],2)
        if self.openQT != 0: self.openVal = self.priceNum * self.openQT
        else: self.openVal = 0

        return self.price


    def placeOrder(self, coin, type):

        success = True
        # actual purchase code will be here
        price = self.priceNum

        if success:
            if type == 'BUY':
                self.openQT = self.accountBalance / self.priceNum
                self.cash = self.accountBalance - (self.priceNum * self.openQT)
                self.buyPrice = self.priceNum
                self.buyQT = self.openQT
                self.buyVal = self.buyPrice * self.buyQT
                self.logData()

            else:
                print('[TRADEBOT] placing SELL order at ' + str(self.priceNum))
                self.accountBalance = self.cash + (self.priceNum*self.openQT)
                self.soldVal = self.cash + (self.priceNum*self.openQT)
                self.soldQT = self.openQT
                self.cash = self.accountBalance
                self.openQT = 0
                self.logData()

        return success,price


    def getAccountInfo(self, type=None):

        # to do - will allow bot to handle positions and orders
        return None


    def logData(self):

        self.accountBalance = round(self.cash + (self.priceNum * self.openQT),2)

        if self.accountBalance > self.startingBal:
            self.dayGain = self.accountBalance - self.startingBal
        elif self.accountBalance < self.startingBal:
            self.dayGain = -(self.startingBal - self.accountBalance)
        else:
            self.dayGain = 0

        if self.openQT != 0:
            self.openVal = self.openQT * self.priceNum
            if self.openVal > self.buyVal:
                self.openGain = self.openVal - self.buyVal
            elif self.openVal < self.buyVal:
                self.openGain = -(self.buyVal - self.openVal)
            else:
                self.openGain = 0

        else:
            self.openGain = 0
            self.openVal = 0


    def updateMessage(self):

        self.logData()

        self.webhook = DiscordWebhook(url=self.url, username='Nyria', content='')
        self.embed = DiscordEmbed(title='[STATUS UPDATE]', description='', color='4200FF')
        self.embed.add_embed_field(name='Time', value=str(time.strftime("%H:%M")))
        self.embed.add_embed_field(name='Account Balance', value='**$' + str(self.accountBalance) + '**')
        self.embed.add_embed_field(name='Current Price', value='$' + str(self.priceNum))
        self.embed.add_embed_field(name='Open QT', value='x **' + str(self.openQT) + '**')
        self.embed.add_embed_field(name='Market Value', value='$' + str(round(self.openVal,2)))

        if self.openGain < 0:
            self.gainPerc = '-' + str(round((abs(self.openGain) / self.buyVal) * 100, 2)) + '%'
            self.gainText = '**-$' + str(round(abs(self.openGain),2)) + '**' + ' (' + self.gainPerc + ')'

        if self.openGain > 0:
            self.gainPerc = '+' + str(round((self.openGain / self.buyVal) * 100, 2)) + '%'
            self.gainText = '**+$' + str(round(self.openGain)) + '**' + ' (' + self.gainPerc + ')'

        else:
            self.gainText = '**$0**'

        self.embed.add_embed_field(name='Open Gain', value=self.gainText)

        if self.dayGain < 0:
            gainPerc = '-' + str(round((abs(self.dayGain) / self.startingBal) * 100, 2)) + '%'
            self.gainText = '**-$' + str(round(abs(self.dayGain),2)) + '**' + ' (' + gainPerc + ')'

        if self.dayGain > 0:
            gainPerc = '+' + str(round((self.dayGain / self.startingBal) * 100, 2)) + '%'
            self.gainText = '**+$' + str(round(self.dayGain,2)) + '**' + ' (' + gainPerc + ')'

        else:
            self.gainText = '**$0**'

        self.embed.add_embed_field(name='Day Gain', value=self.gainText)

        self.webhook.add_embed(self.embed)
        response = self.webhook.execute()


    def pushDiscordNotif(self, url, type=''):

        try:

            if type == 'watching' or self.watching:
                self.color = '3464eb'
                self.title = '[READY]'
                self.desc = '**Now watching $SOL for a scalp due to an oversold dip.**'

            if type == 'sell':
                self.color = 'eb3453'
                self.title = '[SOLD]'
                self.desc = '**Placed a SELL order in $SOL @ ' + str(self.priceNum) + '**'

            if type == 'buy':
                self.color = '03fca9'
                self.title = '[PURCHASED]'
                self.desc = '**Placed a LONG order in $SOL @ ' + str(self.priceNum) + '**'

            if type == 'start_msg':
                self.color = '53eb34'
                self.title = '[ENABLED]'
                self.desc = ''


            try:
                self.webhook = DiscordWebhook(url=self.url, username='Nyria', content='')
                self.embed = DiscordEmbed(title=self.title, description=self.desc, color=self.color)
                self.embed.add_embed_field(name='Time', value=str(time.strftime("%H:%M")))

                if type != 'start_msg':

                    self.embed.add_embed_field(name='Price', value='**$' + str(round(self.priceNum,2)) + '**')

                    if type == 'buy':

                        self.embed.add_embed_field(name='QT', value='x ' + str(self.openQT))
                        self.embed.add_embed_field(name='Value', value='**$' + str(round(self.openVal, 2)) + '**')

                    if type == 'sell':

                        self.embed.add_embed_field(name='QT', value='x ' + str(self.soldQT))

                        self.openGain = self.soldVal - self.buyVal
                        if self.openGain < 0: self.gains.append(-(round((abs(self.openGain) / self.buyVal) * 100, 2)))
                        else: self.gains.append(round((abs(self.openGain) / self.buyVal) * 100, 2))
                        self.avgGain = round(sum(self.gains) / len(self.gains),2)
                        # for debug purposes o
                        print(self.openGain)
                        print(self.avgGain)
                        print(self.gains)

                        self.embed.add_embed_field(name='Bought Price', value='$' + str(round(self.buyPrice, 2)))
                        self.embed.add_embed_field(name='Bought Value', value='$' + str(round(self.buyVal,2)))

                        if self.soldVal > self.buyVal:
                            self.soldValText = '**$' + str(round(self.soldVal,2)) + '** +$' + str(round(self.soldVal-self.buyVal,2)) + ' (+' + str(round(((self.soldVal-self.buyVal)/self.buyVal)*100,2)) + '%)'
                        else:
                            self.soldValText = '**$' + str(round(self.soldVal,2)) + '** -$' + str(round(self.buyVal-self.soldVal,2)) + ' (-' + str(round(((self.buyVal-self.soldVal)/self.buyVal)*100,2)) + '%)'

                        self.embed.add_embed_field(name='Sold Value', value=self.soldValText)

                        self.embed.add_embed_field(name='New Balance', value='**$' + str(round(self.accountBalance,2)) + '**')

                        if self.openGain < 0:
                            self.gainPerc = '-' + str(round((abs(self.openGain) / self.buyVal) * 100,2)) + '%'
                            self.gainText = '**-$' + str(round(abs(self.openGain),2)) + '**' + ' (' + self.gainPerc + ')'

                        if self.openGain > 0:
                            self.gainPerc = '+' + str(round((self.openGain / self.buyVal) * 100,2)) + '%'
                            self.gainText = '**+$' + str(round(self.openGain,2)) + '**' + ' (' + self.gainPerc + ')'
                        else:
                            # debug purposes
                            print(self.openGain)
                            print(self.buyVal)
                            print(self.sellVal)
                            self.gainText = '**$0**'

                        self.embed.add_embed_field(name='Realized Gain', value=self.gainText)

                        if self.dayGain < 0:
                            self.gainPerc = '-' + str(round((abs(self.dayGain) / self.startingBal) * 100,2)) + '%'
                            self.gainText = '**-$' + str(round(abs(self.dayGain),2)) + '**' + ' (' + self.gainPerc + ')'

                        if self.dayGain > 0:
                            self.gainPerc = '+' + str(round((self.dayGain / self.startingBal) * 100, 2)) + '%'
                            self.gainText = '**+$' + str(round(self.dayGain,2)) + '**' + ' (' + self.gainPerc + ')'

                        else:
                            self.gainText = '**$0**'

                        self.embed.add_embed_field(name='Day Gain', value=self.gainText)

                        if self.avgGain < 0:
                            self.avgGainText = '-' + str(abs(self.avgGain)) + '%'
                        else:
                            self.avgGainText = '+' + str(abs(self.avgGain)) + '%'

                        self.embed.add_embed_field(name='Trades Taken', value=str(len(self.gains)))

                        self.embed.add_embed_field(name='Avg % Gain', value=self.avgGainText)

                else:

                    self.embed.add_embed_field(name='Traded Assets', value='**$SOL**')

                    self.embed.add_embed_field(name='Starting Balance', value='**$' + str(self.accountBalance) + '**')

            except Exception as exception:

                print(1)

                traceback.print_exc()

            self.webhook.add_embed(self.embed)
            response = self.webhook.execute()

            return True

        except Exception as exception:

            traceback.print_exc()

            return traceback.format_exc()