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

        super().__init__(country, self.rows, "Facebook")
        self.channel_type = 'social'
        self.templateFile = os.path.join(self.templatePath,'Facebook/ES_Facebook_Sheet_Template.xls') 
        

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
                print('Hybris file error')
                error = {'Error file'}
                df = pd.DataFrame(error, columns = ['Error file'])
                # df.to_csv(self.csvFile, sep = ",", index=False)
                # df.to_xml(self.xmlFile)
                self.sendError()
                sys.exit('Hybris file error')
            print('CSV downloaded')

    def setLink(self, df, tracking_plataforma):
        tracking_plataforma = self.tracking_plataforma
        df['Link'] = df['Id'].map(tracking_plataforma).fillna(df['Link']+'?cid=pt_pd_social_facebook_'+df['Title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none')
        df['Link'] = df['Link'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        return df


#     def avoidXMLbreak(self,df):
#         #Final replace of "&" character by "and" in title and description
#         df['ns1:description'] = df['ns1:description'].str.replace('&','and')
       
#         #"&"Character makes xml breaks so we add "CDATA block to make the xml ignore it
#         df['ns1:link'] = df['ns1:link'].apply(lambda x: '<![CDATA['+ x +']]>')
#         return df

    def setDF(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[['Id', 'Gtin', 'Title', 'Description', 'Item_Group_Id', 'Link', 'Image_Link', 'Brand', 'Condition', 'Availability', 'Price', 'Sale_Price', 'Product_Type' ]]
        df = df.rename({'Id' : 'ns1:id', 'Gtin' : 'ns1:gtin', 'Title' : 'ns1:title', 'Description' : 'ns1:description', 'Item_Group_Id' : 'ns1:item_group_id', 'Link': 'ns1:link', 'Image_Link' : 'ns1:image_link', 'Brand' : 'ns1:brand', 'Condition' : 'ns1:condition', 'Availability' : 'ns1:availability', 'Price' : 'ns1:price', 'Sale_Price' : 'ns1:sale_price', 'Product_Type' : 'ns1:google_product_category'}, axis=1)
        df['ns1:gtin'] = df['ns1:gtin'].astype('int64', errors='ignore')
        df['ns1:description'] = df['ns1:description'].str.replace('"', '', regex=True)
        df['ns1:title'] = df['ns1:title'].str.replace('"', '', regex=True)
        df['ns1:description'] = df['ns1:description'].str.replace(" õ", "õ", regex=False)
        df['ns1:title'] = df['ns1:title'].str.replace(" õ", "õ", regex=False)

        return df

if __name__ == "__main__":
        country = sys.argv[1]
        # Run process
        FacebookFeedCheil(country).run()