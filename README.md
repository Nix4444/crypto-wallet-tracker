# Crypto Wallet Tracker 

![GitHub last commit](https://img.shields.io/github/last-commit/Nix4444/crypto-wallet-tracker) ![GitHub issues](https://img.shields.io/github/issues-raw/Nix4444/crypto-wallet-tracker) 
![GitHub views](https://img.shields.io/github/watchers/Nix4444/crypto-wallet-tracker?style=social) ![Python](https://img.shields.io/badge/python-3.x-green.svg)


The Crypto Wallet Transactions Tracker Bot is a Simple Discord bot designed to monitor and notify users of transaction activities across multiple cryptocurrency wallets. 
Leveraging real-time data from blockchain explorers, this bot provides immediate updates on Bitcoin and Litecoin transactions, ensuring that you stay informed of all activity within your crypto wallets. Whether you're tracking personal finances or managing a portfolio of crypto assets, this bot acts as your vigilant assistant, delivering crucial transaction information directly to your Discord server.

## Features

- Real-time transaction monitoring for Bitcoin and Litecoin wallets.
- Instant notifications for new transactions.
- Current price fetching for Bitcoin and Litecoin.

If you'd like to contribute for adding support for more crypto currencies, feel free to!


## Requirements
To run the bot, you'll need to have Python 3.6 or later installed on your system, along with the following Python libraries:
``discord.py``
``requests``
You'll also need to get an API key, get the free key from here: [Crypto Compare URL](https://min-api.cryptocompare.com/)

## Installation
1. Clone this repo: ``https://github.com/Nix4444/crypto-wallet-tracker``
2. Install the requirements: ``pip install -r requirements.txt``
3. Run ``setup.bat`` To setup API Key, Discord Bot token, Crypto Wallet Addresses
4. Start The Bot ``python Wallet.py``

-> Optional: Also add BTC, LTC, USDT symbols as emojis to your server, and name them BTC, LTC, USDT respectively. The Embed might display it as "None" if not done. They are uploaded in ``icons`` folder.






## Disclaimer
This bot does not have access to your wallet, and all data is stored on your local machine.





