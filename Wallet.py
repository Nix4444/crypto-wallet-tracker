import os
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
addy_info_api=f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet}"
usd_api='https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&api_key={321940b1c8bf5b47d9d121abebceac2f25f0d102c630d559c47e02fc455aed0f}'
api_token='d0c92a0487f24892a58054c8954d675e'#blockcypher



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
    
update_oldhash('994c7b79b4e3e207c197607e7c8caea37cb9a324d6471e484c033e32877e8828')

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
    response = requests.get(api)
    data = json.loads(response.text)
    new_transaction = data['txs'][0]
    new_hash = new_transaction.get('hash')
    n = new_hash
    input1 = data['txs'][0]
    inputs_list = input1.get('inputs')
    prevout = inputs_list[0].get('prev_out')
    tx_addy = prevout.get('addr')
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
    
    if new_hash != oldh:
        if tx_addy == wallet:
            btcvalue = sent_btc() * 0.00000001
            usd_rate = update_usd()
            finalp = usd_rate * btcvalue
            finalp = round(finalp,2)
            msg = f"📤 Sent {btcvalue} {btc_emoji}: ${finalp}\n Check Confirmations here: https://blockchair.com/bitcoin/transaction/{n}"
            update_oldhash(new_hash)
            await send_notification(msg)

        else:
            btcvalue = get_received_btc(new_hash)
            usd_rate = update_usd()
            finalp = usd_rate * btcvalue
            finalp = round(finalp,2)
            msg = f"📥 Received {btcvalue} {btc_emoji}: ${finalp}\n Check Confirmations here: https://blockchair.com/bitcoin/transaction/{n}"
            update_oldhash(new_hash)
            await send_notification(msg)
    else:
        return None
        
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
    finalp=current_balance * 0.00000001* update_usd()
    finalp = round(finalp,2)
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
    await ctx.send(f"Current Balance: {current_balance * 0.00000001} {btc_emoji} = ${finalp}")


@client.command()
async def price(ctx):
    btc_emoji = discord.utils.get(client.emojis, name='BTC')
    msg = f"{btc_emoji}: ${update_usd()}"
    await send_notification(msg)





@client.event
async def on_ready():
    print("I'm Up.")
    check_trnscs.start()
    update_status.start()
    
    

client.run(token)
