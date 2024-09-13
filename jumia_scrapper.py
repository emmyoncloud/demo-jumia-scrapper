import os
import re
import requests
import time
import pandas as pd
import pygsheets
import unicodedata
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone


def extract_jumia_price(url):
    request = requests.get(url)
    soup = bs(request.content,'html.parser')
    product_name = soup.find("h1",{"class":"-fs20 -pts -pbxs"}).get_text()
    new_str = unicodedata.normalize("NFKD", product_name)
    price = soup.find("span",{"class":"-b -ubpt -tal -fs24 -prxs"}).get_text()
    prince_int = int(''.join(re.findall(r'\d+', price)))
    time_now = datetime.now(timezone("Africa/Lagos")).strftime('%Y-%m-%d %H:%M')
    return [new_str, prince_int, time_now]


path = 'optimum-agent-429214-s3-6701d765e026.json'
sheet_id = '12dLBJw91FYhWUDVlXejgzslk1gW9q1qB36I8UEbIhhs'
URL = "https://www.jumia.com.ng/hikers-43-frameless-fhd-led-tv-black-250798217.html"
gc = pygsheets.authorize(service_account_file = path)
gsheet_1 = gc.open_by_key(sheet_id)


output = extract_jumia_price(URL)
df = pd.DataFrame([output], columns = ["Product", "Price", "Date Time"])


ws_1 = gsheet_1.worksheet()
sheet_df = ws_1.get_as_df()

if sheet_df.empty:
    ws_1.set_dataframe(df,
                     (1,1))
else:
    df = pd.concat([sheet_df, df], 
                   ignore_index=True)
    ws_1.set_dataframe(df,
                     (1,1))
