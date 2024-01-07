@echo off
echo Please enter your configuration details.

SET /P cryptocompare_apikey=Enter your CryptoCompare API key: 
SET /P btc_wallet=Enter your BTC wallet address: 
SET /P ltc_wallet=Enter your LTC wallet address: 
SET /P token=Enter your Discord bot token: 
SET /P channel_id=Enter your Discord channel ID: 

echo Writing configuration to settings.txt...
(
echo cryptocompare_apikey=%cryptocompare_apikey%
echo btc_wallet=%btc_wallet%
echo ltc_wallet=%ltc_wallet%
echo token=%token%
echo channel_id=%channel_id%
) > settings.txt

echo Configuration complete. You can now run your bot.
pause