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
usd_api='https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
api_token='d0c92a0487f24892a58054c8954d675e'#blockcypher


def fetch_wallet_bal():
    response = requests.get(api)
    data = json.loads(response.text)
    return data["balance"]
print(fetch_wallet_bal)



def update_usd():
    response = requests.get(usd_api)
    data = json.loads(response.text)
    usd_final =  data['bitcoin']['usd']
    return usd_final
    
@tasks.loop(seconds=90)
async def check_trnscs():
    response = requests.get(api)
    data = json.loads(response.text)
    transactions = data['txs']

    for transaction in transactions:
        tx_hash = transaction['hash']
        outgoing = False
        for output in transactions['out']:
            if output['addr'] == wallet:
                outgoing = True
                break
            if outgoing:
                message = f"📤 Outgoing transaction: https://www.blockchain.com/btc/tx/{tx_hash}"
            else:
                message = f"📤 Incoming transaction: https://www.blockchain.com/btc/tx/{tx_hash}"
    
    await send_notification(message)

    

    
    
        
            
        


    
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