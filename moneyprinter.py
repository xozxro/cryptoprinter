import bot

import data
from datetime import datetime
import time
import csv
from alpha_vantage.timeseries import TimeSeries
from bot import tradebot
import traceback




def makeTrade(tradearray,trends,type):


    success = False
    if type == 'BUY':
        try:
            success, price = bot.placeOrder('ETHUSD', 'BUY')
        except Exception as exception:
            print('[!] critical error in order placement.')
            traceback.print_exc()
    else:
        try:
            success, price = bot.placeOrder('ETHUSD', 'SELL')
        except Exception as exception:
            print('[!] critical error in order placement.')
            traceback.print_exc()


    # log trade
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y")
    with open(dt_string + ' ETHtrades.csv', 'a') as outputcsv:
        writer_ = csv.writer(outputcsv)
        writer_.writerow(tradearray)
        writer_.writerow(trends)
        outputcsv.close()


    # determine buy strength
    trndcnt = 0
    for trend in trends:
        if trend == 'FALSE':
            trndcnt += 1
    if trndcnt > 5:
        strong = True
    else:
        strong = False


    if success:
        # push discord notif
        pushDiscordMessageSuccess = bot.pushDiscordNotif(data.discordwebhook,type='sell')
        if pushDiscordMessageSuccess != True:
            print('[TRADEBOT] CRITICAL ERROR IN DISCORD MESSAGE SYSTEM!')


    return success





def createCSV():

    fields = ['TIME', 'HIGH', 'LOW', 'CLOSE', 'RSI', 'VWAP', 'EMA12', 'EMA26', 'MACD', 'STOCH']
    now = datetime.now()

    dt_string = now.strftime("%d-%m-%Y")

    with open(dt_string + ' ETHtrades.csv', 'w') as outputcsv:
        writer_ = csv.writer(outputcsv)
        writer_.writerow(fields)
        outputcsv.close()





def compareForEntry(previous,dataDict):

    # compare
    if dataDict['stockOpen'] < previous['close'][-1] or dataDict['close'] < previous['close'][-1]:
        priceDowntrend = True
    else:
        priceDowntrend = False

    if dataDict['MACD'] < previous['MACD'][-1]:
        MACDdowntrend = True
    else:
        MACDdowntrend = False

    if dataDict['RSI'] < previous['RSI'][-1]:
        RSIdowntrend = True
    else:
        RSIdowntrend = False

    if dataDict['close'] < dataDict['VWAP']:
        if (dataDict['VWAP'] - dataDict['close']) > (previous['VWAP'][-1] - previous['close'][-1]):
            LowerFromVWAP = True
        else:
            LowerFromVWAP = False
    else:
        LowerFromVWAP = False

    if dataDict['STOCH'] < previous['STOCH'][-1]:
        STOCHdowntrend = True
    else:
        STOCHdowntrend = False

    if dataDict['close'] < previous['close'][-1]:
        closeDowntrend = True
    else:
        closeDowntrend = False

    if previous['stockOpen'][-1] < previous['ema12'][-1] or dataDict['stockOpen'] < dataDict['ema12']:
        if (dataDict['ema12'] - dataDict['stockOpen']) > (previous['ema12'][-1] - previous['stockOpen'][-1]):
            LowerFromEMA12 = True
        else:
            LowerFromEMA12 = False
    else:
        LowerFromEMA12 = False

    return priceDowntrend, MACDdowntrend, RSIdowntrend, LowerFromVWAP, STOCHdowntrend, closeDowntrend, LowerFromEMA12







ts = TimeSeries(key='MTRZCHDVXHJJTONU',output_format='pandas')


# set other variables
laststatus = 'NULL'
rsis = []
volumes = []
avgprices = []
first = True
histogram = 'NULL'
RSI = 'NULL'
opentime = False
exitNeeded = False


# set up previous data and trend memory
previous = {'VWAP': [], 'close': [], 'MACD': [], 'RSI': [], 'STOCH': [], 'ema12': [], 'stockOpen': []}
previousTrends = {'priceDowntrend': [], 'MACDdowntrend': [], 'RSIdowntrend': [], 'LowerFromVWAP': [],
                  'STOCHdowntrend': [], 'closeDowntrend': [], 'LowerFromEMA12': []}


# initialize trading bot object
bot = tradebot()
bot.pushDiscordNotif(data.discordwebhook, type='start_msg')


while True:



    # ADD TO PREVIOUS DATA COLLECTION
    if first:
        pass
    else:
        previous['VWAP'].append(VWAP)
        previous['close'].append(close)
        previous['MACD'].append(MACD)
        previous['RSI'].append(RSI)
        previous['STOCH'].append(STOCH)
        previous['ema12'].append(ema12)
        previous['stockOpen'].append(stockOpen)



    # GET MARKET DATA
    dataWorking = False
    while dataWorking == False:
        try:
            dataDict = bot.getPrice(avgprices, volumes)
            dataDict5m = bot.getPrice(avgprices, volumes, interval='5m')
            dataDict15m = bot.getPrice(avgprices, volumes, interval='15m')
            dataWorking = True
        except:
            time.sleep(10)
            pass



    # ASSIGN MARKET DATA
    high = dataDict['high']
    stockOpen = dataDict['stockOpen']
    low = dataDict['low']
    close = dataDict['close']
    volume = dataDict['volume']
    RSI = dataDict['RSI']
    MACD = dataDict['MACD']
    VWAP = dataDict['VWAP']
    STOCH = dataDict['STOCH']
    histogram = dataDict['histogram']
    ema12 = dataDict['ema12']
    ema26 = dataDict['ema26']
    ema5 = dataDict['ema5']
    avgprices = dataDict['avgprices']
    avgprice = dataDict['avgprice']
    volumes = dataDict['volumes']

    if first:
        previous['VWAP'].append(VWAP)
        previous['close'].append(close)
        previous['MACD'].append(MACD)
        previous['RSI'].append(RSI)
        previous['STOCH'].append(STOCH)
        previous['ema12'].append(ema12)
        previous['stockOpen'].append(stockOpen)
        previous['VWAP'].append(VWAP)
        previous['close'].append(close)
        previous['MACD'].append(MACD)
        previous['RSI'].append(RSI)
        previous['STOCH'].append(STOCH)
        previous['ema12'].append(ema12)
        previous['stockOpen'].append(stockOpen)
        previous['VWAP'].append(VWAP)
        previous['close'].append(close)
        previous['MACD'].append(MACD)
        previous['RSI'].append(RSI)
        previous['STOCH'].append(STOCH)
        previous['ema12'].append(ema12)
        previous['stockOpen'].append(stockOpen)

    high5m = dataDict5m['high']
    stockOpen5m = dataDict5m['stockOpen']
    low5m = dataDict5m['low']
    close5m = dataDict5m['close']
    volume5m = dataDict5m['volume']
    RSI5m = dataDict5m['RSI']
    MACD5m = dataDict5m['MACD']
    VWAP5m = dataDict5m['VWAP']
    STOCH5m = dataDict5m['STOCH']
    histogram5m = dataDict5m['histogram']
    ema125m = dataDict5m['ema12']
    ema265m = dataDict5m['ema26']
    ema55m = dataDict5m['ema5']
    avgprices5m = dataDict5m['avgprices']
    avgprice5m = dataDict5m['avgprice']
    volumes5m = dataDict5m['volumes']

    high15m = dataDict15m['high']
    stockOpen15m = dataDict15m['stockOpen']
    low15m = dataDict15m['low']
    close15m = dataDict15m['close']
    volume15m = dataDict15m['volume']
    RSI15m = dataDict15m['RSI']
    MACD15m = dataDict15m['MACD']
    VWAP15m = dataDict15m['VWAP']
    STOCH15m = dataDict15m['STOCH']
    histogram15m = dataDict15m['histogram']
    ema1215m = dataDict15m['ema12']
    ema2615m = dataDict15m['ema26']
    ema515m = dataDict15m['ema5']
    avgprices15m = dataDict15m['avgprices']
    avgprice15m = dataDict15m['avgprice']
    volumes15m = dataDict15m['volumes']

    if first == True:
        first = False
        RSIdowntrend = False
    else:
        priceDowntrend, MACDdowntrend, RSIdowntrend, LowerFromVWAP, STOCHdowntrend, closeDowntrend, LowerFromEMA12 = compareForEntry(
            previous, dataDict)
        previousTrends['priceDowntrend'].append(priceDowntrend)
        previousTrends['MACDdowntrend'].append(MACDdowntrend)
        previousTrends['RSIdowntrend'].append(RSIdowntrend)
        previousTrends['LowerFromVWAP'].append(LowerFromVWAP)
        previousTrends['STOCHdowntrend'].append(STOCHdowntrend)
        previousTrends['closeDowntrend'].append(closeDowntrend)
        previousTrends['LowerFromEMA12'].append(LowerFromEMA12)

        if len(previous['VWAP']) > 40:
            for key, value in previous.items():
                previous[key] = value[-30:]

        if len(previousTrends['priceDowntrend']) > 50:
            for key, value in previousTrends.items():
                previousTrends[key] = value[20:]


    # UPDATE TIME
    now = datetime.now()
    lastminute = now.strftime("%M")
    current_time = now.strftime("%H:%M:%S")


    # PRINT MESSAGE TO CONSOLE
    print()

    print('[TRADEBOT]         [' + str(current_time) + ']')
    print('[TRADEBOT]  PRICE | $' + str(round(avgprice,2)))
    print('[TRADEBOT] VOLUME | ' + str(volume))




    # TEST FOR OVERSOLD DIP IN ASSET PRICE
    try:
        testa = previous['close'][-1]
    except:
        testa = close

    if len(previous['close']) > 19:
        testBool = previous['close'][-20] > stockOpen
    else:
        testBool = RSIdowntrend

    lowestMACD = 100
    lowestRSI = 100

    if close < VWAP and close < ema12 and close < ema265m and close < ema5 and \
            (RSI5m < 35 or RSI < 32) and testBool:
        if (MACD < previous['MACD'][-1] or MACD < previous['MACD'][-2] or MACDdowntrend):
            if histogram < 0:


                print('[TRADEBOT] watching for a trade.')


                # UPDATE PREVIOUS TRADE DICT
                previous['VWAP'].append(VWAP)
                previous['close'].append(close)
                previous['MACD'].append(MACD)
                previous['RSI'].append(RSI)
                previous['STOCH'].append(STOCH)
                previous['ema12'].append(ema12)
                previous['stockOpen'].append(stockOpen)



                # PUSH DISCORD MESSAGE
                pushDiscordMessageSuccess = bot.pushDiscordNotif(data.discordwebhook, type='watching')
                if pushDiscordMessageSuccess != True:
                    print('[TRADEBOT] CRITICAL ERROR IN DISCORD MESSAGE SYSTEM!')



                # SET VARIABLES
                trade = True # MAIN TRADE VAR
                waitForUptrend = False # HELPS WEIGH DECISIONS
                possible = False #
                wait = False #
                newCsv = False #

                tradearray = []



                # OPEN LOOP TO PLACE TRADE
                while trade:


                    # REFRESH TIME
                    now = datetime.now()
                    minute = now.strftime("%M")
                    current_time = now.strftime("%H:%M:%S")
                    # wait for next minute
                    while minute == lastminute:
                        time.sleep(1)
                        now = datetime.now()
                        minute = now.strftime("%M")
                    time.sleep(1)


                    # KEEP TRACK OF CURRENT MINUTE
                    lastminute = minute


                    # GET NEW DATA
                    dataWorking = False
                    while dataWorking == False:

                        try:

                            dataDict = bot.getPrice(avgprices, volumes)
                            dataDict5m = bot.getPrice(avgprices, volumes, interval='5m')
                            dataDict15m = bot.getPrice(avgprices, volumes, interval='15m')
                            dataWorking = True

                        except:

                            time.sleep(2)
                            pass


                    # SAVE TREND CALCULATIONS FOR COMPARISON
                    priceDowntrend, MACDdowntrend, RSIdowntrend, LowerFromVWAP, STOCHdowntrend, closeDowntrend, LowerFromEMA12 = compareForEntry(
                        previous, dataDict)
                    previousTrends['priceDowntrend'].append(priceDowntrend)
                    previousTrends['MACDdowntrend'].append(MACDdowntrend)
                    previousTrends['RSIdowntrend'].append(RSIdowntrend)
                    previousTrends['LowerFromVWAP'].append(LowerFromVWAP)
                    previousTrends['STOCHdowntrend'].append(STOCHdowntrend)
                    previousTrends['closeDowntrend'].append(closeDowntrend)
                    previousTrends['LowerFromEMA12'].append(LowerFromEMA12)

                    avgprices = dataDict['avgprices']
                    volumes = dataDict['volumes']

                    # KEEP TRACK OF TIME
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")

                    # SAVE DATA IF TRADE PLACED
                    tradearray = [current_time, dataDict['high'], dataDict['low'], dataDict['close'], dataDict['RSI'],
                                  dataDict['VWAP'], dataDict['ema12'], dataDict['ema26'], dataDict['MACD'],
                                  dataDict['STOCH']]


                    # SORT DATA
                    high = dataDict['high']
                    stockOpen = dataDict['stockOpen']
                    low = dataDict['low']
                    close = dataDict['close']
                    volume = dataDict['volume']
                    RSI = dataDict['RSI']
                    MACD = dataDict['MACD']
                    VWAP = dataDict['VWAP']
                    STOCH = dataDict['STOCH']
                    histogram = dataDict['histogram']
                    ema12 = dataDict['ema12']
                    ema26 = dataDict['ema26']
                    ema5 = dataDict['ema5']
                    avgprices = dataDict['avgprices']
                    avgprice = dataDict['avgprice']
                    volumes = dataDict['volumes']

                    high5m = dataDict5m['high']
                    stockOpen5m = dataDict5m['stockOpen']
                    low5m = dataDict5m['low']
                    close5m = dataDict5m['close']
                    volume5m = dataDict5m['volume']
                    RSI5m = dataDict5m['RSI']
                    MACD5m = dataDict5m['MACD']
                    VWAP5m = dataDict5m['VWAP']
                    STOCH5m = dataDict5m['STOCH']
                    histogram5m = dataDict5m['histogram']
                    ema125m = dataDict5m['ema12']
                    ema265m = dataDict5m['ema26']
                    ema55m = dataDict5m['ema5']
                    avgprices5m = dataDict5m['avgprices']
                    avgprice5m = dataDict5m['avgprice']
                    volumes5m = dataDict5m['volumes']

                    high15m = dataDict15m['high']
                    stockOpen15m = dataDict15m['stockOpen']
                    low15m = dataDict15m['low']
                    close15m = dataDict15m['close']
                    volume15m = dataDict15m['volume']
                    RSI15m = dataDict15m['RSI']
                    MACD15m = dataDict15m['MACD']
                    VWAP15m = dataDict15m['VWAP']
                    STOCH15m = dataDict15m['STOCH']
                    histogram15m = dataDict15m['histogram']
                    ema1215m = dataDict15m['ema12']
                    ema2615m = dataDict15m['ema26']
                    ema515m = dataDict15m['ema5']
                    avgprices15m = dataDict15m['avgprices']
                    avgprice15m = dataDict15m['avgprice']
                    volumes15m = dataDict15m['volumes']

                    if float(RSI) < float(lowestRSI):
                        lowestRSI = float(RSI)
                    if float(MACD) < float(lowestMACD):
                        lowestMACD = float(MACD)


                    # COMPARE TO LAST MIN
                    currentTrends = [priceDowntrend, MACDdowntrend, RSIdowntrend, LowerFromVWAP, STOCHdowntrend,
                                     closeDowntrend, LowerFromEMA12]


                    # TALLY INDICATOR DOWNTRENDS IN CURRENT MINUTE
                    trueCntNow = 0
                    trueCnt = 0
                    trueCnt_ = 0
                    trueCnt__ = 0

                    for trend in currentTrends:
                        if trend is True:
                            trueCntNow = trueCntNow + 1


                    # TALLY DOWNTRENDS IN PREVIOUS MINUTE
                    # perfect score for downtrend is 7/7
                    try:

                        for trend, arr in previousTrends.items():

                            if arr[-2] is True:
                                trueCnt = trueCnt + 1

                        for trend, arr in previousTrends.items():
                            if arr[-3] is True:
                                trueCnt_ = trueCnt_ + 1

                        for trend, arr in previousTrends.items():
                            if arr[-4] is True:
                                trueCnt__ = trueCnt__ + 1
                    except:
                        # don't have 4 minutes of data yet

                        trueCnt_ = 0
                        trueCnt__ = 0



                    # ALGO TO TEST FOR TRADE PLACEMENT

                    lowestMACDtest = -.6
                    atrVal = abs(close - (previous['stockOpen'][-1])) * 1.5

                    if close > previous['stockOpen'][-4] \
                            and (stockOpen > ema12 or close > ema12) and \
                            (stockOpen > ema55m or close > ema55m) and \
                            MACDdowntrend is False and \
                            lowestMACD < lowestMACDtest and \
                            RSIdowntrend is False and (
                            lowestRSI < 30) and (
                            ema5 > ema12
                            # close > 3 closes ago by more than one atrVal (distance of this close from last x 1.5)
                    ):

                        # ESSENTIAL VARS
                        entryPrice = close
                        entryTrueCnt = trueCntNow

                        tradearray.append('TRADE a')  # KEEP TRACK OF ALGO PATH
                        # TAKE THE TRADE
                        makeTrade(tradearray, currentTrends, 'BUY')  # PASS TRADEARRAY FOR DATA AND CURRENTTRENDS
                        print('[TRADEBOT] placing LONG trade at ' + str(round(close, 2)))
                        # ESSENTIAL VARS
                        exitNeeded = True
                        trade = False



                    if lowestMACD < lowestMACDtest and lowestRSI < 30 and ema5 > ema12 and close < ema5 and \
                            RSIdowntrend is False and (stockOpen > ema55m or close > ema55m) and previous['close'][
                        -1] > ema55m and close > previous['close'][-3]:

                        # ESSENTIAL VARS
                        entryPrice = close
                        entryTrueCnt = trueCntNow

                        tradearray.append('TRADE B') # KEEP TRACK OF ALGO PATH
                        # TAKE THE TRADE
                        makeTrade(tradearray, currentTrends, 'BUY') # PASS TRADEARRAY FOR DATA AND CURRENTTRENDS
                        print('[TRADEBOT] placing LONG trade at ' + str(round(close,2)))
                        # ESSENTIAL VARS
                        exitNeeded = True
                        trade = False


                    # KEEP TRACK OF PREVIOUS DATA - THIS is skipped if trade is FALSE due to an exit.
                    previous['VWAP'].append(VWAP)
                    previous['close'].append(close)
                    previous['MACD'].append(MACD)
                    previous['RSI'].append(RSI)
                    previous['STOCH'].append(STOCH)
                    previous['ema12'].append(ema12)
                    previous['stockOpen'].append(stockOpen)



                consider = False

                # TRADE HAS BEEN PLACED. WE MUST EXIT TO PLACE NEXT TRADE.
                while exitNeeded:



                    # KEEP TRACK OF PREVIOUS DATA - THIS is used if trade is FALSE due to an exit.
                    previous['VWAP'].append(VWAP)
                    previous['close'].append(close)
                    previous['MACD'].append(MACD)
                    previous['RSI'].append(RSI)
                    previous['STOCH'].append(STOCH)
                    previous['ema12'].append(ema12)
                    previous['stockOpen'].append(stockOpen)



                    # KEEP TRACK OF TIME
                    now = datetime.now()
                    minute = now.strftime("%M")
                    current_time = now.strftime("%H:%M:%S")

                    while minute == lastminute:
                        time.sleep(1)
                        now = datetime.now()
                        minute = now.strftime("%M")

                    lastminute = minute



                    # GET NEW DATA
                    dataWorking = False
                    while dataWorking == False:
                        try:
                            dataDict = bot.getPrice(avgprices, volumes)
                            dataWorking = True
                        except:
                            time.sleep(2)
                            pass


                    # KEEP TRACK OF INDICATOR TRENDS
                    priceDowntrend, MACDdowntrend, RSIdowntrend, LowerFromVWAP, STOCHdowntrend, closeDowntrend, LowerFromEMA12 = compareForEntry(
                        previous, dataDict)
                    previousTrends['priceDowntrend'].append(priceDowntrend)
                    previousTrends['MACDdowntrend'].append(MACDdowntrend)
                    previousTrends['RSIdowntrend'].append(RSIdowntrend)
                    previousTrends['LowerFromVWAP'].append(LowerFromVWAP)
                    previousTrends['STOCHdowntrend'].append(STOCHdowntrend)
                    previousTrends['closeDowntrend'].append(closeDowntrend)
                    previousTrends['LowerFromEMA12'].append(LowerFromEMA12)

                    avgprices = dataDict['avgprices']
                    volumes = dataDict['volumes']


                    # KEEP TRACK OF TIME
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")


                    # SAVE TRADEARRAY WITH NEW DATA INCASE OF EXIT
                    tradearray = [current_time, dataDict['high'], dataDict['low'], dataDict['close'], dataDict['RSI'],
                                  dataDict['VWAP'], dataDict['ema12'], dataDict['ema26'], dataDict['MACD'],
                                  dataDict['STOCH']]


                    # SORT DATA
                    high = dataDict['high']
                    stockOpen = dataDict['stockOpen']
                    low = dataDict['low']
                    close = dataDict['close']
                    volume = dataDict['volume']
                    RSI = dataDict['RSI']
                    MACD = dataDict['MACD']
                    VWAP = dataDict['VWAP']
                    STOCH = dataDict['STOCH']
                    histogram = dataDict['histogram']
                    ema12 = dataDict['ema12']
                    ema26 = dataDict['ema26']
                    avgprices = dataDict['avgprices']
                    avgprice = dataDict['avgprice']
                    volumes = dataDict['volumes']



                    # KEEP TRACK OF AVG INDICATOR DIRECTIONS
                    trueCnt = 0
                    trueCnt_ = 0
                    trueCnt__ = 0

                    for trend, arr in previousTrends.items():
                        if arr[-1] is True:
                            trueCnt = trueCnt + 1

                    for trend, arr in previousTrends.items():
                        if arr[-2] is True:
                            trueCnt_ = trueCnt_ + 1

                    for trend, arr in previousTrends.items():
                        if arr[-3] is True:
                            trueCnt__ = trueCnt__ + 1




                    # PRICE DIFFERENCE
                    difference = close - entryPrice
                    lastdifference = previous['close'][-1] - entryPrice


                    # ALGO TO DETERMINE EXITS
                    if difference > 20:
                        tradearray.append('7302734')
                        makeTrade(tradearray, currentTrends, 'SELL')
                        exitNeeded = False

                    elif difference > 10 and difference < 20:
                        tradearray.append('9472')
                        makeTrade(tradearray, currentTrends, 'SELL')
                        exitNeeded = False

                    elif difference > lastdifference + 2:

                        if consider == True:
                            makeTrade(tradearray, currentTrends, 'SELL')
                            consider = False
                            exitNeeded = False

                        tradearray.append('a8932')
                        consider = True

                    elif difference <= 7:
                        tradearray.append('a893')

                        if consider == True or difference <= 8:
                            tradearray.append('894')
                            makeTrade(tradearray, currentTrends, 'SELL')
                            exitNeeded = False

                        elif trueCnt >= entryTrueCnt + 2 and trueCnt >= trueCnt_ + 1:
                            tradearray.append('895')
                            makeTrade(tradearray, currentTrends, 'SELL')
                            exitNeeded = False

                    if trueCnt > entryTrueCnt + 1:
                        tradearray.append('a32235423')
                        consider = True

                    if trueCnt > trueCnt_ + 1:
                        tradearray.append('a523563')
                        consider = True

                    if trueCnt >= trueCnt__ + 2:
                        tradearray.append('a12345423')
                        consider = True

                    if minute == lastminute:

                        while minute == lastminute:
                            time.sleep(1)
                            now = datetime.now()
                            minute = now.strftime("%M")

    now = datetime.now()
    minute = now.strftime("%M")

    while minute == lastminute:
        time.sleep(1)
        now = datetime.now()
        minute = now.strftime("%M")
