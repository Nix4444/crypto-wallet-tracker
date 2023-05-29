import discord
import requests
import json
from discord.ext import commands, tasks

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
channel_id=1087340845700763712
btc_wallet = 'bc1q96y38ev7uvhmrvapgnl9q95gfr99nnxyldeglg'
token = 'MTA4NzMzNTMwODIxNzAyNDUzMw.G06GkU.-thUHr12PbYJMNUH2EDEdR2JkMV9Q8Z7M2pp8Q'
api=f"https://blockchain.info/rawaddr/{btc_wallet}"
btcaddy_info_api=f"https://api.blockcypher.com/v1/btc/main/addrs/{btc_wallet}"
btc_price_api='https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key={addc799de5b1c06c6adb4381396de5d8711002a807a5521c1f85ffabe5ce146b}'
api_token='d0c92a0487f24892a58054c8954d675e'
test = f"https://blockstream.info/api/address/{btc_wallet}/txs"

#LTC APIs---
ltc_wallet='LM9PY3LdkE8Mmmu4SJL5t75yxp89z4qt9u'
ltc_txhistory_api = f"https://chainz.cryptoid.info/ltc/api.dws?key=1cb5722c643e&q=multiaddr&active={ltc_wallet}"
ltchashinfo_api = "https://chainz.cryptoid.info/ltc/api.dws?q=txinfo&t="
ltc_price_api ="https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD&api_key={addc799de5b1c06c6adb4381396de5d8711002a807a5521c1f85ffabe5ce146b}"


def fetch_btc_bal():
    response = requests.get(btcaddy_info_api)
    data = json.loads(response.text)
    return data["balance"]
def fetch_ltc_bal():
    response = requests.get(ltc_txhistory_api)
    data = json.loads(response.text)
    bal = data["addresses"][0]["final_balance"]
    return bal
def btcprice():
    response = requests.get(btc_price_api)
    data = json.loads(response.text)
    btcpr =  data['USD']
    return btcpr
def ltcprice():
    response = requests.get(ltc_price_api)
    data = json.loads(response.text)
    ltcpr =  data['USD']
    return ltcpr
def get_received_btc(newh):
    response = requests.get(btcaddy_info_api)
    data = json.loads(response.text)
    data = data['txrefs'][0]
    txhash = data.get('tx_hash')
    if txhash == newh:
        values = data.get('value')
        btcnum = 0.00000001 * values
        return btcnum

@tasks.loop(seconds=90)
async def check_btc_trnscs():
    
    response = requests.get(test)
    txs = response.json()
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
    usdt_emoji = discord.utils.get(client.emojis, name='USDT')        
    usd_emoji = discord.utils.get(client.emojis, name='USD')
    
    channel_id=1087340845700763712
    latest_tx = txs[0]["txid"]
    f = open("latestBTCtx.txt", "r")
    oldh = f.readline()
    f.close()

    if latest_tx != oldh:
            
            inputs = txs[0]["vin"]
            outputs = txs[0]["vout"]
            address_input_value = 0
            address_output_value = 0
            for input in inputs:
                if input["prevout"]["scriptpubkey_address"] == btc_wallet:
                    address_input_value += input["prevout"]["value"]
            for output in outputs:
                if output["scriptpubkey_address"] == btc_wallet:
                    address_output_value += output["value"]
            if address_input_value > address_output_value:
                direction = "sent"
            else:
                direction = "received"
            
            if direction == "sent":
                value = (address_input_value - address_output_value) * 0.00000001
                value = round(value,10)
                usd_rate = btcprice()
                finalp = usd_rate * value
                finalp = round(finalp,2)
                embed = discord.Embed(title="Money Sent Successfully!", color=0xff0000)
                embed.set_author(name="BTC Sent!", url=f"https://blockchair.com/bitcoin/transaction/{latest_tx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1888/1888486.png")
                embed.add_field(name=f"{btc_emoji}BTC", value=value)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)
                f = open("latestBTCtx.txt", "w")
                f.write(latest_tx)
                f.close()
                
                await client.get_channel(channel_id).send(embed=embed)
            else:
                value = (address_output_value - address_input_value) * 0.00000001
                value = round(value,10)
                usd_rate = btcprice()
                finalp = usd_rate * value 
                finalp = round(finalp,2)
                embed = discord.Embed(title="Money Received Successfully!", color=0x46D117)
                embed.set_author(name="BTC Received!", url=f"https://blockchair.com/bitcoin/transaction/{latest_tx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1888/1888486.png")
                embed.add_field(name=f"{btc_emoji}BTC", value=value)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)
                f = open("latestBTCtx.txt", "w")
                f.write(latest_tx)
                f.close()
                
                await client.get_channel(channel_id).send(embed=embed)
@tasks.loop(seconds=90)
async def check_ltc_trnscs():
    channel_id = 1087340845700763712
    response = requests.get(ltc_txhistory_api)
    data = json.loads(response.text)
    newtx = data['txs'][0]['hash']
    f = open("latestLTCtx.txt", "r")
    tx = f.readline()
    f.close()
    if newtx != tx:
        response = requests.get(ltchashinfo_api + newtx)
        data = json.loads(response.text)
        input = data["inputs"]
        for i in input:
            addy = i["addr"]
            if addy == ltc_wallet:
                direction = "sent"
                output = data["outputs"]
                ltcvalue = output[-1]["amount"]
                ltcvalue = round(ltcvalue,6)
                usd_rate = ltcprice()
                finalp =  ltcvalue * usd_rate
                finalp = round(finalp,2)
                ltc_emoji = discord.utils.get(client.emojis, name='LTC')
                usdt_emoji = discord.utils.get(client.emojis, name='USDT')
                usd_emoji = discord.utils.get(client.emojis, name='USD')
                embed = discord.Embed(title="Money Sent Successfully!", color=0xff0000)
                embed.set_author(name="LTC Sent!", url=f"https://blockchair.com/litecoin/transaction/{newtx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3938/3938179.png")
                embed.add_field(name=f"{ltc_emoji}LTC", value=ltcvalue)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}LTC Price", value=f"${usd_rate}", inline=True)
                f = open("latestLTCtx.txt", "w")
                f.write(newtx)
                f.close()
                await client.get_channel(channel_id).send(embed=embed)

            else:
                direction = "received"
                output = data["outputs"]
                for i in output:
                    if i['addr'] == ltc_wallet:
                        ltcvalue = i["amount"]
                ltcvalue = round(ltcvalue,6)
                usd_rate = ltcprice()
                finalp =  ltcvalue * usd_rate
                finalp = round(finalp,2)
                ltc_emoji = discord.utils.get(client.emojis, name='LTC')
                usdt_emoji = discord.utils.get(client.emojis, name='USDT')
                usd_emoji = discord.utils.get(client.emojis, name='USD')
                embed = discord.Embed(title="Money Received Successfully!", color=0x46D117)
                embed.set_author(name="LTC Received!", url=f"https://blockchair.com/litecoin/transaction/{newtx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3938/3938179.png")
                embed.add_field(name=f"{ltc_emoji}LTC", value=ltcvalue)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}LTC Price", value=f"${usd_rate}", inline=True)
                f = open("latestLTCtx.txt", "w")
                f.write(newtx)
                f.close()
                await client.get_channel(channel_id).send(embed=embed)

    


@client.command()
async def bal(ctx,coin):
    if coin == 'ltc' or coin == 'LTC' or coin == "Ltc":
        current_balance = fetch_ltc_bal()
        ltcvalue = current_balance *0.00000001
        ltcvalue = round(ltcvalue,6)
        usd_rate = ltcprice()
        finalp = current_balance  * usd_rate * 0.00000001
        finalp = round(finalp,2)
        ltc_emoji = discord.utils.get(client.emojis, name='LTC')
        usdt_emoji = discord.utils.get(client.emojis, name='USDT')
        usd_emoji = discord.utils.get(client.emojis, name='USD')
        embed = discord.Embed(title="Current Balance💸", color=0x5217D1)
        embed.set_author(name="LTC Wallet Balance", url=f"https://blockchair.com/litecoin/address/{ltc_wallet}", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3938/3938179.png")
        embed.add_field(name=f"{ltc_emoji}LTC", value=ltcvalue)
        embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
        embed.add_field(name=f"{usdt_emoji}LTC Price", value=f"${usd_rate}", inline=True)
 
    elif coin == 'btc' or coin =='BTC' or coin == 'Btc':

        current_balance = fetch_btc_bal()
        usd_rate = btcprice()
        btcvalue = current_balance * 0.00000001
        btcvalue = round(btcvalue,10)
        finalp=current_balance * 0.00000001* usd_rate
        finalp = round(finalp,2)
        btc_emoji = discord.utils.get(client.emojis, name='BTC')
        usdt_emoji = discord.utils.get(client.emojis, name='USDT')
        usd_emoji = discord.utils.get(client.emojis, name='USD')
        embed = discord.Embed(title="Current Balance💸", color=0x5217D1)
        embed.set_author(name="BTC Wallet Balance", url=f"https://blockchair.com/bitcoin/address/{btc_wallet}", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5341/5341431.png")
        embed.add_field(name=f"{btc_emoji}BTC", value=btcvalue)
        embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
        embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)

    elif coin == "all" or coin == "All" or coin == "ALL":
        ltcbal = fetch_ltc_bal()
        btcbal = fetch_btc_bal()
        usd_ltc_rate = ltcprice()
        usd_btc_rate = btcprice()
        finalltc = ltcbal * usd_ltc_rate * 0.00000001
        finalbtc= btcbal * 0.00000001* usd_btc_rate
        finalltc = round(finalltc,2)
        finalbtc = round(finalbtc,2)
        btcvalue = btcbal * 0.00000001
        btcvalue = round(btcvalue,10)
        ltcvalue = ltcbal * 0.00000001
        ltcvalue = round(ltcvalue,6)
        walletbal = round(finalltc + finalbtc,2)
        btc_emoji = discord.utils.get(client.emojis, name='BTC')
        ltc_emoji = discord.utils.get(client.emojis, name='LTC')
        usdt_emoji = discord.utils.get(client.emojis, name='USDT')
        usd_emoji = discord.utils.get(client.emojis, name='USD')
        embed = discord.Embed(title="Current Balance💸", color=0x5217D1)
        embed.set_author(name="Wallet Balance", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/4825/4825188.png")
        embed.add_field(name=f"{btc_emoji}BTC", value=btcvalue )
        embed.add_field(name= f"{ltc_emoji}LTC", value = ltcvalue  , inline=True )
        embed.add_field(name=f"{usd_emoji}Value", value=f"${walletbal}", inline=True)
        embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_btc_rate}", inline=True)
        embed.add_field(name=f"{usdt_emoji}LTC Price", value=f"${usd_ltc_rate}", inline=True)

    await ctx.send(embed=embed)
@client.command()
async def price(ctx):
        btc_emoji = discord.utils.get(client.emojis, name='BTC')
        ltc_emoji = discord.utils.get(client.emojis, name='LTC')
        embed = discord.Embed(title="Market Price💸", color=0x5217D1)
        embed.set_author(name="Major Coins", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9214/9214823.png")
        embed.add_field(name=f"{btc_emoji}BTC", value=f"${btcprice()}" )
        embed.add_field(name= f"{ltc_emoji}LTC", value = f"${ltcprice()}"  , inline=True )
        await ctx.send(embed=embed)


async def send_notification(message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

@tasks.loop(seconds = 30)
async def update_status():
    pr = btcprice()
    intpr = int(pr)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f"BTC 💰: ${intpr}"))

@client.event
async def on_ready():
    print("I'm Up.")
    check_btc_trnscs.start()
    check_ltc_trnscs.start()
    update_status.start()
 
client.run(token)