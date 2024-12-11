import requests
import pandas as py
import matplotlib as mpl
import time

def filterIDs(result):
    IDs_list = []

    for token in result:
            IDs_list.append(token['tokenAddress'])

    return IDs_list
def pairFinder(tokenIDs):
   for token_Id in tokenIDs:
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_Id}"
            result = requests.get(url).json()
            pairs = result.get('pairs', [])
            for pair in pairs:
                if pair.get('quoteToken', {}).get('symbol') == 'SOL':
                    price_usd = float(pair.get('priceUsd', 0))
                    market_cap = pair.get('marketCap', 0)
                    created_at = pair.get('pairCreatedAt', 0)
                    volume_5m = pair.get('volume', {}).get('m5', 0)
                    
                    if (price_usd < 0.000001 and market_cap <= 500000 and 
                        volume_5m > 200 and 
                        created_at/1000 + 3600 <= time.time()):
                        print(pair.get('baseToken', {}).get('address'))
        except requests.RequestException as e:
            print(f"An error occurred while fetching data for token {token_Id}: {e}")
        except ValueError as ve:
            print(f"Error converting price to float: {ve}")
        time.sleep(0.5)  # Small delay to respect API rate limits

                
        

      
url = "https://api.dexscreener.com/token-profiles/latest/v1"

result = requests.get(url)

result = result.json()

tokenIDs = filterIDs(result)

pairFinder(tokenIDs)

