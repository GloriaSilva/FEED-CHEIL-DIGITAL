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
import html

class KuantoKustaFeedCheil(FeedCheil):
    def __init__(self,country):
        
        self.rows = ['EAN', 'Id', 'Title', 'Description', 'Availability', 'Condition', 'Stock', 'Price', 'Sale_Price', 'Shipping_price', 'Size', 'Color', 'Image_Link', 'Product_Type', 'Brand', 'Link']
        self.platform = 'kuantokusta'

        super().__init__(country, self.rows,'KuantoKusta')
        self.templateFile = os.path.join(self.templatePath,'KuantoKusta/ES_KuantoKusta_Sheet_Template.xls') 

       
    # Open file and scrap
    def openFileAndScrap(self):
        # Open file and scrap
        with open(self.Google_feed_maestroCSV, mode='w') as archivo:
            archivo = csv.writer(archivo)
            archivo.writerow(self.rows)
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

                    if y.find('g:availability') is None:
                            Availability = ""
                    else:
                            Availability = y.find('g:availability').text
                    if y.find('g:condition') is None:
                            Condition = ""
                    else:
                            Condition = y.find('g:condition').text
                    if y.find('g:stock') is None:
                            Stock = ""
                    else:
                            Stock = y.find('g:stock').text
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
                    if y.find('g:gtin') is None:
                            Id = ""
                    else:
                            ean = y.find('g:gtin').text
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
                    if y.find('g:size') is None:
                            Size = ""
                    else:
                            Size = y.find('g:size').text

                    if y.find('g:color') is None:
                            Color = ""
                    else:
                            Color = y.find('g:color').text
                    if y.find('g:shipping') is None:
                            Shipping_price = ""
                    else:
                            shipping = soup.find('g:shipping')
                            Shipping_price = y.shipping.find('g:price').text
                   
                    if not Id or not ean:
                            continue
                    archivo.writerow ([ean, Id, Title, Description, Availability, Condition, Stock, Price, Sale_Price, Shipping_price, Size, Color, Image_link, Product_Type, Brand, Link])

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


    def setLink(self, df, tracking):
        df['Link'] = df['Link']+'?'+df['Id'].map(tracking).fillna(f'cid=pt_pd_affiliate_{self.platform}_'+df['Title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none')
        df['Link'] = df['Link'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')  
        return df

    def setDF(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[['Id', 'EAN', 'Title', 'Description', 'Link', 'Image_Link', 'Brand', 'Condition', 'Availability', 'Price', 'Sale_Price', 'Product_Type', 'Stock', 'Shipping_price' ]]
        df = df.rename({'Id' : 'reference', 'EAN' : 'upc_ean', 'Title' : 'designation', 'Description' : 'description', 'Link': 'product_url', 'Image_Link' : 'image_url', 'Brand' : 'brand', 'Condition' : 'condition', 'Availability' : 'availability', 'Price' : 'regular_price', 'Sale_Price' : 'current_price', 'Product_Type' : 'category', 'Stock' : 'stock', 'Shipping_price' : 'norma_shipping_cost'},axis=1)
        df['upc_ean'] = df['upc_ean'].astype('int64', errors='ignore')
        #df['g:stock'] = df['g:stock'].astype('int64', errors='ignore')
        df['stock'] = df['stock'].astype(str)
        df['stock'] = df['stock'].str.replace('.0', '', regex=True)
        df['stock'] = df['stock'].str.replace('nan', '', regex=True)
        df['description'] = df['description'].str.replace('"', '', regex=True)
        df['description'] = df['description'].str.replace(" õ", "õ", regex=False)
        df['designation'] = df['designation'].str.replace('"', '', regex=True)
        df['category'] = df['category'].astype(str)
        df['category'] = df['category'].str.replace('nan', 'N/A')
        df['product_url'] = html.unescape(df['product_url'])

        return df

    def avoidXMLbreak(self,df):
        #Final replace of "&" character by "and" in title and description
        df['designation'] = df['designation'].str.replace('&','and')
        df['description'] = df['description'].str.replace('&','and')
        #"&"Character makes xml breaks so we add "CDATA block to make the xml ignore it
        df['product_url'] = df['product_url'].apply(lambda x: '<![CDATA[ '+ x +']]>')
        return df


if __name__ == "__main__":
        country = sys.argv[1]
        # Run process
        KuantoKustaFeedCheil(country).run()