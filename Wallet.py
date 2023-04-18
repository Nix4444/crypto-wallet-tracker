import discord
import requests
import json
from discord.ext import commands, tasks

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
channel_id=1087340845700763712
wallet = 'bc1q96y38ev7uvhmrvapgnl9q95gfr99nnxyldeglg' #btc
token = 'MTA4NzMzNTMwODIxNzAyNDUzMw.G06GkU.-thUHr12PbYJMNUH2EDEdR2JkMV9Q8Z7M2pp8Q'
api=f"https://blockchain.info/rawaddr/{wallet}"
#addy_info_api=f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet}" not using blockcypher anymore
usd_api='https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key={321940b1c8bf5b47d9d121abebceac2f25f0d102c630d559c47e02fc455aed0f}'
api_token='d0c92a0487f24892a58054c8954d675e'#blockcypher token
addy_info_api = f"https://blockstream.info/api/address/{wallet}/txs"




def fetch_wallet_bal():
    response = requests.get(addy_info_api)
    data = json.loads(response.text)
    return data["balance"]



def update_usd():
    response = requests.get(usd_api)
    data = json.loads(response.text)
    usd_final =  data['USD']
    return usd_final
    

def update_oldhash(newh):
    global oldh
    oldh = newh
    
update_oldhash('11b1d12ab497327ce054232944b18531f73c1581487a238c4f1d9a358beae42b')

def get_received_btc(newh):
    response = requests.get(addy_info_api)
    data = json.loads(response.text)
    data = data['txrefs'][0]
    txhash = data.get('tx_hash')
    if txhash == newh:
        values = data.get('value')
        btcnum = 0.00000001 * values
        return btcnum

def sent_btc():
    response = requests.get(api)
    data = json.loads(response.text)
    data = data['txs'][0]
    out = data.get('out')
    value = out[1].get('value')
    return value



@tasks.loop(seconds=90)
async def check_trnscs():
    
    response = requests.get(addy_info_api)
    txs = response.json()
    
    latest_tx = txs[0]["txid"]
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
    usdt_emoji = discord.utils.get(client.emojis, name='USDT')
    usd_emoji = discord.utils.get(client.emojis, name='USD')
    
    channel_id=1087340845700763712
    
    
    
        
        
    if txs[0]["txid"] != oldh:
            latest_tx = txs[0]["txid"]
            inputs = txs[0]["vin"]
            outputs = txs[0]["vout"]
            address_input_value = 0
            address_output_value = 0
            for input in inputs:
                if input["prevout"]["scriptpubkey_address"] == wallet:
                    address_input_value += input["prevout"]["value"]
            for output in outputs:
                if output["scriptpubkey_address"] == wallet:
                    address_output_value += output["value"]
            if address_input_value > address_output_value:
                direction = "sent"
            else:
                direction = "received"
            
            if direction == "sent":
                value = address_input_value - address_output_value
                usd_rate = update_usd()
                finalp = usd_rate * value * 0.00000001
                finalp = round(finalp,2)
                embed = discord.Embed(title="Money Sent Successfully!", color=0xff0000)
                embed.set_author(name="BTC Sent!", url=f"https://blockchair.com/bitcoin/transaction/{latest_tx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1888/1888486.png")
                embed.add_field(name=f"{btc_emoji}BTC", value=value*0.00000001)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)
                update_oldhash(latest_tx)
                await client.get_channel(channel_id).send(embed=embed)
            else:
                value = address_output_value - address_input_value
                usd_rate = update_usd()
                finalp = usd_rate * value *0.00000001
                finalp = round(finalp,2)
                
                embed = discord.Embed(title="Money Received Successfully!", color=0x46D117)
                embed.set_author(name="BTC Received!", url=f"https://blockchair.com/bitcoin/transaction/{latest_tx}", icon_url='https://cdn-icons-png.flaticon.com/512/5610/5610944.png')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1888/1888486.png")
                embed.add_field(name=f"{btc_emoji}BTC", value=value*0.00000001)
                embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
                embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)
                update_oldhash(latest_tx)
                await client.get_channel(channel_id).send(embed=embed)
            
    


@tasks.loop(seconds = 30)
async def update_status():
    pr = update_usd()
    intpr = int(pr)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = f"BTC 💰: ${intpr}"))


    
    
async def send_notification(message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

@client.command()
async def bal(ctx):
            current_balance = fetch_wallet_bal()
            usd_rate = update_usd()
            finalp=current_balance * 0.00000001* usd_rate
            finalp = round(finalp,2)
            btc_emoji = discord.utils.get(client.emojis, name='BTC')
            usdt_emoji = discord.utils.get(client.emojis, name='USDT')
            usd_emoji = discord.utils.get(client.emojis, name='USD')
            embed = discord.Embed(title="Current Balance💸", color=0x5217D1)
            embed.set_author(name="Wallet Balance", url=f"https://blockchair.com/bitcoin/address/{wallet}", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/5341/5341431.png")
            embed.add_field(name=f"{btc_emoji}BTC", value=current_balance * 0.00000001)
            embed.add_field(name=f"{usd_emoji}Value", value=f"${finalp}", inline=True)
            embed.add_field(name=f"{usdt_emoji}BTC Price", value=f"${usd_rate}", inline=True)
    
            await ctx.send(embed=embed)


@client.command()
async def price(ctx):
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
   

    embed = discord.Embed(title="Current Price",description=f"{btc_emoji}BTC: ${update_usd()} ",color=0x5217D1)
    embed.set_author(name="BTC Market Price", url="https://blockchair.com/bitcoin", icon_url='https://cdn-icons-png.flaticon.com/512/3444/3444339.png')
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/9214/9214823.png")
    
    await ctx.send(embed=embed)





@client.event
async def on_ready():
    print("I'm Up.")
    check_trnscs.start()
    update_status.start()
    
    
    
    
    

client.run(token)
