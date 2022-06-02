![ezcv logo](https://raw.githubusercontent.com/xozxro/cryptoprinter/main/Crypto_Printer.png)

## _The Last Project You'll Ever Need._

----------------

![Twitter Follow](https://img.shields.io/twitter/follow/NyriaStocks?style=for-the-badge)(https://twitter.com/xozxro)
![Discord](https://img.shields.io/discord/836723167690883103?style=for-the-badge)(https://discord.gg/QJQqRUHk)


#### **Nyria's cryptocurrency trading bot is an open source, fully customizable day trading bot.**
**Written in Python by [zxro](https://twitter.com/xozxro) under [Nyria LLC](https://nyriabot.io).**




## *Planned Features*

- Trailing stops, dynamic stop losses
- Support for multiple currencies under one bot
- Varying position sizing based on a variety of factors which signal strength of uptrend
- Easy crypto platform connection
- Settings dashboard *(stops, position sizing, etc)*

## *Current Features*
- Complete entry / exit autonomy in the $SOL cryptocurrency
- Consistent trades being made targeting .2% - .7% per trade
- Alerts and updates on all trades sent to Discord channel

![example](https://raw.githubusercontent.com/xozxro/cryptoprinter/main/example.png)

The bot is derived from the algorithms which empower Nyria's dip - buying alert bots.
It's been made open source to strive for transparent and effecient community development,
so Nyria can build a trust - driven ecosystem and environment around the creation,
improvement, and public release of the bot as a product.

> If you are interested in developing
> this project under Nyria, or have
> contributions you would like
> published in the public version,
> plase email me at 
[michael@alwaysascending.io](mailto:michael@alwaysascending.io).



## Dependencies

The bot is built using some pretty simple libraries and tools. *Currently, we're focused 
on finding the perfect source of crypto price data, which can provide a dataframe of data 
for any high - volume cryptocurrency.* Yahoo finance prices work for testing and 
development, however are not accurate enough for real life use cases. **If you have any
suggestions, please provide them!**

- [yfinance](https://pypi.org/project/yfinance/) - Python Wrapper for the Yahoo Finance API
- [discord_webhook](https://pypi.org/project/discord-webhook/) - For sending bot messages to discord

For a default crypto trading platform, the bot will be written around FTX US due to 
their low fees and extensive API documentation. To make the bot work out of the box,
you must make an account there, [*get an API key*](https://ftx.us/settings/api), and provide it in the data.py file.
 - [FTX US](https://ftx.us/home/) API key and secret




## Installation / Use

The Crypto Printer requies at least Python 3.9x to run.

Please make an FTX.US account as mentioned above. You will need to make an API key
under the 'API' section in the drop down under your account.

Install the above dependencies through pip, drag the files into one folder, add your
API key, API secret, and optionally, your Discord webhook URL to get update 
messages to a Discord channel of your own.
```
apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
apiSecret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
discordwebhook = 'https://discord.com/api/webhooks/xxxxxxxxxxxxxx/xxxxxx'
```

**IMPORTANT: If you do not want the bot place trades for you, set devMode to True**.



**From here, you should be able to run the bot by executing the 'moneyprinter.py' script.**



## Development

Want to contribute? Great! 

Submit any pull requests you feel are critical to the general function of the bot.
Otherwise, feel free to shoot me an email to discuss this project more!

[michael@alwaysascending.io](emailto:michael@alwaysascending.io)


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
