from Feed_Cheil import FeedCheil
# dependencies
import os
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import csv
import sys
from config import project_path

class FacebookFeedCheil(FeedCheil):
    def __init__(self,country):
        
        self.rows = ['Id', 'Title', 'Description', 'Item_Group_Id', 'Availability', 'Condition', 'Price', 'Sale_Price', 'Image_Link', 'Gtin', 'Product_Type', 'Brand', 'Link']
        self.platform = 'facebook'

        super().__init__(country, self.rows)
        
        self.csvFile = f"FacebookFeed_{self.country}.csv"
        self.xmlFile = f"FacebookFeed_{self.country}.xml"
        

    # Open file and scrap
    def openFileAndScrap(self):
        # Open file and scrap
        with open(self.Google_feed_maestroCSV, mode='w') as archivo:
            archivo = csv.writer(archivo)
            archivo.writerow(['Id', 'Title', 'Description', 'Item_Group_Id', 'Availability', 'Condition', 'Price', 'Sale_Price', 'Image_Link', 'Gtin', 'Product_Type', 'Brand', 'Link'])
            url = self.url
            document = requests.get(url)
            status_code = document.status_code
            if status_code==200:
                soup = BeautifulSoup(document.content,"xml")
                x = soup.find_all('entry')

                for i, y in enumerate(x):
                    if self.filterXMLid(y.find('g:id')):
                            Id = ""
                    else:
                            Id = y.find('g:id').text

                    if y.find('g:title') is None:
                            Title = ""
                    else:
                            Title = y.find('g:title').text

                    if y.find('g:description') is None:
                            Description = ""
                    else:
                            Description = y.find('g:description').text

                    if y.find('g:item_group_id') is None:
                            Item_Group_Id = ""
                    else:
                            Item_Group_Id = y.find('g:item_group_id').text

                    if y.find('g:availability') is None:
                            Availability = ""
                    else:
                            Availability = y.find('g:availability').text

                    if y.find('g:condition') is None:
                            Condition = ""
                    else:
                            Condition = y.find('g:condition').text

                    if y.find('g:price') is None:
                            Price = ""
                    else:
                            Price = y.find('g:price').text

                    if y.find('g:sale_price') is None:
                            Sale_Price = ""
                    else:
                            Sale_Price = y.find('g:sale_price').text

                    if y.find('g:image_link') is None:
                            Image_link = ""
                    else:
                            Image_link = y.find('g:image_link').text

                    if y.find('g:gtin') is None or y.find('g:gtin').text=="":
                            Gtin = ""
                    else:
                            Gtin = y.find('g:gtin').text

                    if y.find('g:product_type') is None:
                            Product_Type = ""
                    else:
                            Product_Type = y.find('g:product_type').text

                    if y.find('g:brand') is None:
                            Brand = ""
                    else:
                            Brand = y.find('g:brand').text

                    if y.find('g:link') is None:
                            Link = ""
                    else:
                            Link = y.find('g:link').text
                    #print(titulo, modelo, modificacion, imagen, disponibilidad, precio, special_price)
                    if not Id or not Gtin:
                            continue
                    archivo.writerow ([Id, Title, Description, Item_Group_Id, Availability, Condition, Price, Sale_Price, Image_link, Gtin, Product_Type, Brand, Link])

            else:
                print("Código de estado %d" % status_code)
                error = {'Error file'}
                df = pd.DataFrame(error, columns = ['Error file'])
                df.to_csv(f'FacebookFeed_{self.country}.csv', sep = ",", index=False)
                df.to_xml(f"FacebookFeed_{self.country}.xml")
                self.sendError()
                sys.exit('Hybris file error')
            print('CSV downloaded')

    # Clean CSV
    def cleanCSV(self, df):
        df1 = f"{self.templatePath}/Facebook/ES_Facebook_Sheet_Template.xls"
        if os.path.isfile(df1):
            df1 = pd.read_excel(df1)
            if df1.empty == False:
                col  = 'id'
                descriptions = dict(zip(df1['id'],df1['description']))
                titles = dict(zip(df1['id'],df1['title']))
                self.tracking_plataforma = dict(zip(df1['id'],df1['tracking']))

                conditions  = [ df1[col].str.match('SM-A') | df1[col].str.match('SM-G') | df1[col].str.match('SM-N') | df1[col].str.match('SM-F') | df1[col].str.match('SM-M') | df1[col].str.match('SM-S'),
                    df1[col].str.match('SM-P') | df1[col].str.match('SM-T') | df1[col].str.match('SM-X'),
                    df1[col].str.match('SM-R'),
                    df1[col].str.match('EF-') | df1[col].str.match('EP-') | df1[col].str.match('EB-') | df1[col].str.match('ET-') | df1[col].str.match('GP-'),
                    df1[col].str.match('DV') | df1[col].str.match('WW'),
                    df1[col].str.match('DW'),
                    df1[col].str.match('HAF-'),
                    df1[col].str.match('MC') | df1[col].str.match('MG') | df1[col].str.match('MS'),
                    df1[col].str.match('NK') | df1[col].str.match('NV') | df1[col].str.match('NZ'),
                    df1[col].str.match('RB') | df1[col].str.match('RL') | df1[col].str.match('RR') | df1[col].str.match('RS') | df1[col].str.match('RT') | df1[col].str.match('RZ'),
                    df1[col].str.match('VC') | df1[col].str.match('VS'),
                    df1[col].str.match('QE') | df1[col].str.match('UE'),
                    df1[col].str.match('SP-'),
                    df1[col].str.match('HW-'),
                    df1[col].str.match('VG-'),
                    df1[col].str.match('LC') | df1[col].str.match('LS') | df1[col].str.match('LF') | df1[col].str.match('LU'),
                    df1[col].str.match('MU-') | df1[col].str.match('MZ-'),
                    ]
                choices = [ "im-smartphone", 'im-tablet', 'im-wearables', 'im-accessories', 'da-washing', 'da-dishwasher', 'da-accessories',  'da-microwave', 'da-kitchen', 'da-refrigerator', 'da-vacuum', 'vd-television', 'vd-projector', 'vd-audio', 'vd-accessories', 'it-monitor', 'it-memory'  ]

                df1['category'] = np.select(conditions, choices, default='none-none')
                df1['tracking'] = df1['tracking'].fillna('cid='+self.country+'_pd_social_facebook_'+df1['title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df1['id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df1['category']+'-automatic-feed_pla_none_none')
                df['Description'] = df['Id'].map(descriptions).fillna(df['Description'])
                df['Title'] = df['Id'].map(titles).fillna(df['Title'])
                df['Link'] = df['Id'].map(self.tracking_plataforma).fillna(df['Link'])

            else:
                pass
        else:
            pass
        print("CSV cleaned")
        return df

    def setLink(self, df, tracking_plataforma):
        tracking_plataforma = self.tracking_plataforma
        df['Link'] = df['Id'].map(tracking_plataforma).fillna(df['Link']+'?cid=pt_pd_social_facebook_'+df['Title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none')
        df['Link'] = df['Link'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        return df

    def setDF(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[['Id', 'Gtin', 'Title', 'Description', 'Item_Group_Id', 'Link', 'Image_Link', 'Brand', 'Condition', 'Availability', 'Price', 'Sale_Price', 'Product_Type' ]]
        df = df.rename({'Id' : 'g:id', 'Gtin' : 'g:gtin', 'Title' : 'g:title', 'Description' : 'g:description', 'Item_Group_Id' : 'g:item_group_id', 'Link': 'g:link', 'Image_Link' : 'g:image_link', 'Brand' : 'g:brand', 'Condition' : 'g:condition', 'Availability' : 'g:availability', 'Price' : 'g:price', 'Sale_Price' : 'g:sale_price', 'Product_Type' : 'g:google_product_category'}, axis=1)
        df['g:gtin'] = df['g:gtin'].astype('int64', errors='ignore')
        df['g:description'] = df['g:description'].str.replace('"', '', regex=True)
        df['g:title'] = df['g:title'].str.replace('"', '', regex=True)
        df['g:description'] = df['g:description'].str.replace(" õ", "õ", regex=False)
        df['g:title'] = df['g:title'].str.replace(" õ", "õ", regex=False)

        return df

if __name__ == "__main__":
        country = sys.argv[1]
        # Run process
        FacebookFeedCheil(country).run()