import aiohttp
import asyncio
import pandas as pd
import  json

async def fetch_data():
    url = "https://data.egov.uz/apiPartner/Partner/WebService"
    params = {
         
        "token": "66648637ae34ef33011decc3",
        "name": "1-003-0016",
        "offset": 0,
        "limit": 10000,
        "lang": "uz"
    }

    headers = {
        ":authority": "data.egov.uz",
        ":method": "GET",
        ":path": "/apiPartner/Partner/WebService?token=66648637ae34ef33011decc3&name=1-003-0016&offset=0&limit=5&lang=uz",
        ":scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,uz;q=0.7",
        "Cache-Control": "max-age=0",
        "Cookie": "i18n_redirected=uzb",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Failed to fetch data. Status code: {response.status}")


# Run the async function
re = asyncio.run(fetch_data())

df = pd.DataFrame(re)
df.to_csv('main.csv')

n_df = pd.read_json(json.dumps(re['result']['data']))

print(n_df.columns)

n_df.to_csv('new.csv')