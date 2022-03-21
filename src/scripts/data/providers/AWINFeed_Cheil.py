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

class AWINFeedCheil(FeedCheil):
    def __init__(self,country):
        
        self.rows = ['Id', 'Title', 'Description', 'Availability', 'Condition', 'Price', 'Sale_Price', 'Image_Link', 'Gtin', 'Product_Type', 'Brand', 'Link']
        self.platform = 'awin'

        super().__init__(country, self.rows,'AWIN')
        self.templateFile = os.path.join(self.templatePath,'AWIN/ES_AWIN_Sheet_Template.xls') 
        

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
                        archivo.writerow ([Id, Title, Description, Availability, Condition, Price, Sale_Price, Image_link, Gtin, Product_Type, Brand, Link])

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
        df['Link'] = df['Id'].map(tracking_plataforma).fillna(df['Link']+f'?cid={self.country}_pd_affiliate_{self.platform}_'+df['Title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none')
        df['Link'] = df['Link'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        return df

    def setDF(self, df):
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[['Id', 'Gtin', 'Title', 'Description', 'Link', 'Image_Link', 'Brand', 'Condition', 'Availability', 'Price', 'Sale_Price', 'Product_Type' ]]
        df = df.rename({'Id' : 'g:id', 'Gtin' : 'g:gtin', 'Title' : 'g:title', 'Description' : 'g:description', 'Link': 'g:link', 'Image_Link' : 'g:image_link', 'Brand' : 'g:brand', 'Condition' : 'g:condition', 'Availability' : 'g:availability', 'Price' : 'g:price', 'Sale_Price' : 'g:sale_price', 'Product_Type' : 'g:product_type'}, axis=1)
        df['g:gtin'] = df['g:gtin'].astype('int64', errors='ignore')
        df['g:description'] = df['g:description'].str.replace('"', '', regex=True)
        df['g:title'] = df['g:title'].str.replace('"', '', regex=True)
        df['g:description'] = df['g:description'].str.replace(" õ", "õ", regex=False)
        df['g:title'] = df['g:title'].str.replace(" õ", "õ", regex=False)

        return df

if __name__ == "__main__":
        country = sys.argv[1]
        # Run process
        AWINFeedCheil(country).run()