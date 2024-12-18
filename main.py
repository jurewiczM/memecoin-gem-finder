import requests
import pandas as py
import csv
import time
import json
from urllib.parse import urlparse

import twintpy

__price_max__ = 0.0005
__marketcap_max__ = 500000
__marketcap_min__ = 55000
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
                    if price_usd < __price_max__:
                        if __marketcap_min__ <= market_cap <= __marketcap_max__:
                            if volume_5m > __volume_min__:
                                if created_at / 1000 + 3600 <= time.time():
                                        print(pair.get('baseToken', {}).get('address'))
                                        pair_list.append(pair.get('baseToken', {}).get('address'))
            

                    
                    #if (price_usd < __price_max__ and __marketcap_min__ <= market_cap <= __marketcap_max__ and 
                    #    volume_5m > __volume_min__ and 
                     #   created_at/1000 + 3600 <= time.time()):


        except requests.RequestException as e:
            print(f"An error occurred while fetching data for token {token_Id}: {e}")
        except ValueError as ve:
            print(f"Error converting price to float: {ve}")
        time.sleep(0.5)  
    return pair_list

def collectSocialData(foundTokens,tokenIDs):
    social_data = []

    for token_Id in foundTokens:
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
        
#this entire segement is based on some guy on stack overflow
def extract_handle_from_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc in ["twitter.com", "x.com"]:
        path = parsed_url.path.strip("/")
        if path:  # Ensure there's something
            return path.split("/")[0]  # Return the segement as a handle
    return None


def fetch_twitter_data(handle):
    c = twint.Config()
    c.Username = handle
    c.Hide_output = True
    c.Store_object = True

    try:
        twint.run.Lookup(c)
        user = twint.output.users_list[0]
        return {
            "username": user.username,
            "tweets": user.tweets,
            "followers": user.followers,
        }
    except Exception as e:
        print(f"Error fetching data for {handle}: {e}")
        return None

def process_social_data(social_data):
    for entry in social_data:
        token = entry.get("token", "Unknown")
        print(f"Processing token: {token}")
            
        for social in entry.get("socials", []):
            if social["type"] == "twitter":
                twitter_url = social.get("url", "")
                handle = extract_handle_from_url(twitter_url)
                if handle:
                    print(f"Fetching data for handle: {handle}")
                    data = fetch_twitter_data(handle)
                    if data:
                        print(f"Username: {data['username']}, Tweets: {data['tweets']}, Followers: {data['followers']}")
                else:
                    print(f"Invalid or unsupported Twitter URL: {twitter_url}")
        print("-" * 40)



#start program - collect last 30 tokens deployed on dexscreener
      
url = "https://api.dexscreener.com/token-profiles/latest/v1"

result = requests.get(url)

result = result.json()

#filter out token CA addreses to later get info about them
tokenIDs = filterIDs(result)

#the main part - looking for tokens with hard typed attributes - the attributes might
#need some testing. Since the memecoin world is changing rapidly and there are a lot of 'strategies'
#user can change the hard written attributes. Might need to fix it with the nice gui.
foundTokens = tokenFinder(tokenIDs)


#Collecting social data - second most important thing  about memecoins. 
# Using twint to get basic data about followers, posts and engagement
# Need to find memecoins with organic  community and help with rugpools


socialData = collectSocialData(foundTokens,tokenIDs)

processed_socials = process_social_data(socialData)

#output data - the entire process takes too long - optimize!
output_data = []

for i in range(len(foundTokens)):
    
    social_info = process_social_data
    
    
    entry = {
        "token": foundTokens[i],  # Add the token
        "pair": social_info['pair'],  # Add the 'pair' key from socialData
        "socials": social_info[i]  # Add the 'socials' key from socialData
    }
    
    # Append the entry to the output data
    output_data.append(entry)

# Save to a JSON file
with open("gems.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)




