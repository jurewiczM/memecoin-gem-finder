import requests
import pandas as py
import csv
import time

__price_max__ = 0.000001
__marketcap_max__ = 500000
__marketcap_min__ = 75000
__volume_min__ = 200

def filterIDs(result):
    IDs_list = []

    for token in result:
            IDs_list.append(token['tokenAddress'])

    return IDs_list
def tokenFinder(tokenIDs):

    pair_list = []
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
                    
                    if (price_usd < __price_max__ and __marketcap_min__ <= market_cap <= __marketcap_max__ and 
                        volume_5m > __volume_min__ and 
                        created_at/1000 + 3600 <= time.time()):
                        print(pair.get('baseToken', {}).get('address'))
                        pair_list.append(air.get('baseToken', {}).get('address'))

            return pair_list
        except requests.RequestException as e:
            print(f"An error occurred while fetching data for token {token_Id}: {e}")
        except ValueError as ve:
            print(f"Error converting price to float: {ve}")
        time.sleep(0.5)  

def collectSocialData(foundTokens,tokenIDs):
    social_data = []

    for token_Id in tokenIDs:
        try:
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_Id}"
            result = requests.get(url).json()
            pairs = result.get('pairs', [])
            
            for pair in pairs:
                if pair.get('baseToken', {}).get('address') in foundTokens:
                    socials = pair.get('info', {}).get('socials', [])
                    social_data.append({
                        "pair": pair.get('baseToken', {}).get('address'),
                        "socials": socials
                    })
        except requests.RequestException as e:
            print(f"An error occurred while fetching data for token {token_Id}: {e}")
        time.sleep(0.5)

    return social_data
        
        

      
url = "https://api.dexscreener.com/token-profiles/latest/v1"

result = requests.get(url)

result = result.json()

tokenIDs = filterIDs(result)

foundTokens = tokenFinder(tokenIDs)

#dexData = collectDexData()
socialData = collectSocialData(foundTokens,tokenIDs)

writeFile = open('./gems.csv','w')
writer = csv.writer(writeFile)

for i in range(len(foundTokens)):
    row = foundTokens[i]+';'+socialData[i]
    writer.writerow(foundTokens[i])

