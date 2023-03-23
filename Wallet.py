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
usd_api='https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
api_token='d0c92a0487f24892a58054c8954d675e'#blockcypher
txlink = "https://www.blockchain.com/btc/tx/{new_hash}"
old_hash =''

def fetch_wallet_bal():
    response = requests.get(api)
    data = json.loads(response.text)
    return data["balance"]



def update_usd():
    response = requests.get(usd_api)
    data = json.loads(response.text)
    usd_final =  data['bitcoin']['usd']
    return usd_final
    

def update_oldhash(newh):
    global oldh
    oldh = newh
    
update_oldhash('994c7b79b4e3e207c197607e7c8caea37cb9a324d6471e484c033e32877e8828')

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
    
    if new_hash != oldh:
        if tx_addy == wallet:
            msg = f"Outgoing Transaction Detected!📤\n Check Confirmations here: https://www.blockchain.com/btc/tx/{n}"
            update_oldhash(new_hash)

        else:
            msg = f"Incoming Transaction Detected!📤\n Check Confirmations here: https://www.blockchain.com/btc/tx/{n}"
            update_oldhash(new_hash)
    await send_notification(msg)
        



    
    
async def send_notification(message):
    channel = client.get_channel(channel_id)
    await channel.send(message)

@client.command()
async def bal(ctx):
    current_balance = fetch_wallet_bal()
    finalp=current_balance * 0.00000001* update_usd()
    finalpr = round(finalp,2)
    await ctx.send(f"Current Balance: {current_balance * 0.00000001} BTC = ${finalpr}")


@client.command()
async def price(ctx):
    await ctx.send(update_usd())


@client.event
async def on_ready():
    print("I'm Up.")
    check_trnscs.start()

client.run(token)