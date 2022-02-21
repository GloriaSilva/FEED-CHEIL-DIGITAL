"""
Samsung feed provides urls for each product.
However, these urls are not definitive as they redirect to others.
Therefore, this script collects these urls and gather the final links for each product.
The file generated will be used as a dictionary for any platform feed
"""

import pandas as pd
import sys
import requests
from bs4 import BeautifulSoup
import datetime
from config import project_path, database_info
from Utils import generate_random_int


begin_time = datetime.datetime.now()
print(datetime.datetime.now())

#Every country has its own Samsun feed
country = sys.argv[1]

#We create a dataframe where only product ID and link are stored
df = pd.DataFrame(columns=['Id', 'Link'])
file_name = 'Feed_url.csv'
dict_path = '{}/src/dictionaries/url/'.format(project_path)

url = f'https://shop.samsung.com/{country}/googleShoppingFeed?{generate_random_int(1000000)}'

try:
    document = requests.get(url)
    if document.status_code == 200:
        x = BeautifulSoup(document.content,'xml').find_all('entry')
        for i, y in enumerate(x):
            df.loc[i, ['Id', 'Link']] = [y.find('g:id').text,y.find('g:link').text]
        df.fillna(value='', inplace=True)
    else:
        print("Código de estado %d" % document.status_code)
    print('CSV downloaded')

except:
    print('Not able to reach Samsung Feed')
    sys.exit()


dict_from_csv = {"https://www.samsung.com/pt/smartphones/galaxy-s20/galaxy-s20-fe/buy/":"https://www.samsung.com/pt/smartphones/galaxy-s20/buy/"}
df.drop(df.query('Id == "HAFIN2/EXP"| Id == "HAFEX/EXP"').index, inplace=True)

enlacefinal = []
for x in df['Link']:
    session = requests.Session()
    session.max_redirects = 1000
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        r = session.get(x, allow_redirects=True)
        if r.history:
            link = r.url
        else:
            link = x
        enlacefinal.append(link)
    except:
        enlacefinal.append('Error getting the final link')

df['Final_Link'] = enlacefinal
df.loc[df['Id'].str.startswith('SM-'), 'Final_Link'] = df['Final_Link']+'buy/'
df.loc[df['Id'].str.startswith('SM-R1'), 'Final_Link'] = df['Final_Link'].str.strip('/buy/')
df['Final_Link'] = df['Final_Link'].replace(dict_from_csv)
df['Final_Link'] = df['Final_Link'].replace({'buy/buy/': 'buy/'}, regex=True)
#df.query('Id.str.startswith("SM-") == True & Id.str.startswith("SM-R1") == False' & Final_Link.endswith("buy/") == False)Final_Link.apply(lambda x: x+'buy/')
df.loc[df['Final_Link'].str.contains('[0-9A-Z_]buy/$', regex=True), 'Final_Link'] = df['Final_Link'].str.strip('buy')

shit = df.loc[df['Id'].str.startswith('SM-'), 'Final_Link']
enlacefinal2 = []
for t  in shit:
    session = requests.Session()
    session.max_redirects = 1000
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        r = session.get(t, allow_redirects=True)
        if r.history:
            link = r.url
        else:
            link = t
        enlacefinal2.append(link)
    except:
        enlacefinal.append('Error getting the final link')

df.loc[df['Id'].str.startswith('SM-'), 'Final_Link'] = enlacefinal2

df['Final_Link'] = df['Final_Link'].replace(dict_from_csv)
reg = '^https://www\.samsung\.com/'+country+'/[a-zA-Z]+/.{1,30}/buy/$'
df.loc[df['Final_Link'].str.contains(reg, regex=True), 'Final_Link'] = df['Final_Link']+ '?modelCode='+df['Id']
df['Final_Link'] = df['Final_Link'].replace({'buy/buy/': 'buy/'}, regex=True)
df.loc[df['Final_Link'].str.contains('\?modelCode='), 'Final_Link'] = df['Final_Link'].str.strip('/buy/')

del df["Link"]
df.rename({'Final_Link': 'Link'}, axis=1, inplace=True)
df.to_csv(dict_path + f"url_dictionary_{country}.csv", mode='w')

print("CSV created")
print(datetime.datetime.now() - begin_time)