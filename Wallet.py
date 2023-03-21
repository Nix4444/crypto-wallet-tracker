import os
import discord
import requests
import json
from discord.ext import commands, tasks

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
channel_id=1087340845700763712
wallet = 'bc1q96y38ev7uvhmrvapgnl9q95gfr99nnxyldeglg' #btc
api=f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet}"
usd_api='https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'


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
    
@tasks.loop(seconds=60)
async def check_trnscs():
    response = requests.get(api)
    data = json.loads(response.text)
    current_balance = fetch_wallet_bal()
    finalp= current_balance * 0.00000001* update_usd()
    finalpr = round(finalp,2)
    for tx in data["txrefs"]:
        if tx["tx_output_n"] is None:
            if tx["value"] > 0:
                await send_notification(f"Received {tx['value'] * 0.00000001} BTC = ${finalpr}")
        else:
            if tx["value"]<0:
                await send_notification(f"Sent {tx['value'] * 0.00000001} BTC = ${finalpr} ")
    
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

client.run(os.environ.get('DISCORD_TOKEN'))