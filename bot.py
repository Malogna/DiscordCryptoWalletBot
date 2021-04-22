import discord
from bscscan import BscScan
from pycoingecko import CoinGeckoAPI
import json
import decimal
import re

def priceget(currencyfromdiscord):
    cg = CoinGeckoAPI()
    currencyvs = currencyfromdiscord
    global curpriceformat
    example4 = cg.get_price(ids="safemoon", vs_currencies=currencyvs)
    curprice = (example4["safemoon"][currencyvs])
    curpriceformat = format(curprice, 'f')

def pricegrab(addressfromdiscord, currencyfromdiscord):
    cg = CoinGeckoAPI()

    bsc = BscScan("ABZ3YV2I961GK1HJDPXN7GUQB6WIPEWUWU") # key in quotation marks
    
    global example2
    global sfmwalletbalanceincurfinal
    global curpriceformat
    
    address = addressfromdiscord
    currencyvs = currencyfromdiscord.lower()
    example = int(bsc.get_acc_balance_by_token_contract_address(contract_address="0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3", address=address))
    example2 = example * 0.000000001

    example4 = cg.get_price(ids="safemoon", vs_currencies=currencyvs)
    curprice = (example4["safemoon"][currencyvs])
    curpriceformat = format(curprice, 'f')
    sfmwalletbalanceincurfinal = int(float(curprice) * example2) - (float(curprice) * example2 / 10)

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('??wallet'):
            if '0x' in message.content:
                try:
                    addressyes = message.content.split()
                    addressbruh = addressyes[addressyes.index('??wallet') + 1]
                    currencythingy = addressyes[addressyes.index(addressbruh) + 1]
                    pricegrab(addressbruh, currencythingy)
                    embedVar = discord.Embed(title="**SFM Wallet Address:**", description=str(addressbruh), color=0x0000FF)
                    embedVar.add_field(name="**SFM Wallet Balance:**", value=("{} {}".format(int(example2), "SAFEMOON")), inline=False)
                    embedVar.add_field(name="**SFM Wallet Balance in {}:**".format(str(currencythingy.upper())), value=("{} {}".format(int(sfmwalletbalanceincurfinal), str(currencythingy.upper()))), inline=False)
                    msgsent = await message.channel.send(embed=embedVar)
                    await msgsent.add_reaction("\N{ROCKET}")
                except IndexError:
                    await message.channel.send("**You forgot to specify a currency to convert the SFM into!**")
                except KeyError:
                    await message.channel.send("**The Currency you specified was invalid! Check your spelling and try again. You're dumber than Fabian bro**")
                except AssertionError:
                    await message.channel.send("**That wallet address is invalid**")
        if message.content.startswith('??price'):
            try:
                addressyes = message.content.split()
                currencythingy = addressyes[addressyes.index("??price") + 1]
                priceget(currencythingy)
                msgsent = await message.channel.send("{} {}".format(curpriceformat, currencythingy.upper()))
                await msgsent.add_reaction("\N{ROCKET}")
            except IndexError:
                priceget("usd")
                msgsent = await message.channel.send("{}{}".format(curpriceformat, " USD"))
                await msgsent.add_reaction("\N{ROCKET}")
            except KeyError:
                await message.channel.send("**The Currency you specified was invalid! Check your spelling and try again. You're dumber than Fabian bro**")
print("Ready!")
client = MyClient()
client.run(TOKENGOESHERE)