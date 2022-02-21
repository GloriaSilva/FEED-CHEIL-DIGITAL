"""
GoogleFeed_Cheil class is a child class from Feed_Cheil class. This allows to use any function defined there in the Google feed process.
However, some functions and process are only valid for Google. So, this class is useful as applies the logics that are only valid for this platform.
"""
#Importing the parent class
from Feed_Cheil import FeedCheil
# dependenciess
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import sys

#GoogleFeedCheil class needs the feed's country and the Samsung Feed fields we want to extract
class GoogleFeedCheil(FeedCheil):
    def __init__(self,country):
        country = sys.argv[1]
        #These fields from Samsung feed are only valid for Google feed.
        self.rows = ['Id', 'Title', 'Description', 'Availability', 'Condition', 'Price', 'Sale_Price', 'Image_Link', 'Gtin', 'Product_Type', 'Brand', 'Link']
        self.platform = 'google'

        super().__init__(country, self.rows)

        self.csvFile = f'GoogleFeed_{country}.csv'
        self.xmlFile = f'GoogleFeed_{country}.xml'
        
        

    #Open file and fill it with the content scrapped from Samsung Feed.
    def openFileAndScrap(self):
        # Open file
        with open(self.Google_feed_maestroCSV, mode='w') as archivo:
            #We create a csv.writer object and then we write the first row. This row will be our column names (defined above en self.rows)
            archivo = csv.writer(archivo)
            archivo.writerow(self.rows)
            #Getting the web from the url
            url = self.url
            document = requests.get(url)
            status_code = document.status_code
            #If we receive a valid status code, we start the waterfall of actions for scrapping the html
            if status_code==200:
                #Extracting all entities called "entr" which contains product information
                    soup = BeautifulSoup(document.content,"xml")
                    #Any product is stored in an element called "entry" in Samsung Feed web page
                    x = soup.find_all('entry')
                    for i, y in enumerate(x):
                        #In each "entry" object we have all the fields we want to extract. So, we iterate over each "entry" element for gathering all the data
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
                        if not Id or not Gtin:
                            continue
                        archivo.writerow ([Id, Title, Description, Availability, Condition, Price, Sale_Price, Image_link, Gtin, Product_Type, Brand, Link])
            else:
                #In case we have a different status code, we generate a file "Error file" and triggers the sendError function
                print("Código de estado %d" % status_code)
                error = {'Error file'}
                df = pd.DataFrame(error, columns = ['Error file'])
                df.to_csv(self.resultPath + f'GoogleFeed_{self.country}.csv', sep = ",", index=False)
                df.to_xml(self.resultPath + f'GoogleFeed_{self.country}.xml')
                self.sendError()
                sys.exit('Hybris file error')
            print('CSV downloaded')

    # Clean CSV
    def cleanCSV(self, df):
        #First step, we drop objects with specific IDs as we do not want them in Google feed.
        index_to_drop = df.query('Id == "HAFEX/EXP" | Id == "HAFIN2/EXP"').index
        df.drop(index_to_drop, inplace=True)

        #We create the sheet template path variable
        df1_path = f"{self.templatePath}/Google/ES_Google_Sheet_Template.xls"
        #If the path drives to a file, we start the replacing process
        if os.path.isfile(df1_path):
            #We import the template as a dataframe
            df1 = pd.read_excel(df1_path)
            #We iterate our df, extracted from Samsung Feed, and we replace the Title and Description fields for the personalized ones in the other dataframe.
            if df1.empty == False:
                #We create one dict for Samsung feed Titles and other for Samsung feed descriptions
                descriptions = dict(zip(df1['Id'],df1['Description']))
                titles = dict(zip(df1['Id'],df1['Title']))
                #We replace the products in the template for the personalizd. If template has no Title or Description for a product, the gap is filled with the original Title and Description.
                df['Description'] = df['Id'].map(descriptions).fillna(df['Description'])
                df['Title'] = df['Id'].map(titles).fillna(df['Title'])
            else:
                pass
        else:
            pass
        print("CSV cleaned")
        return df

    def setLink(self, df, tracking):
        #We create the url with the attached cid (Tracking ID) for all products in the dataframe.
        df['Link'] = df['Link']+'?'+df['Id'].map(tracking).fillna('cid='+self.country+df['Title'].replace({' ':'-', '\/':'-', '\&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none')
        df['Link'] = df['Link'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        return df

    def setDF(self, df):
        #We apply the final changes within the feed (column names changes, data types, funny characters...)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df[['Id', 'Gtin', 'Title', 'Description','Link', 'Image_Link', 'Brand', 'Condition', 'Availability', 'Price', 'Sale_Price', 'Product_Type' ]]
        df = df.rename({'Id' : 'g:id', 'Gtin' : 'g:gtin', 'Title' : 'g:title', 'Description' : 'g:description', 'Link': 'g:link', 'Image_Link' : 'g:image_link', 'Brand' : 'g:brand', 'Condition' : 'g:condition', 'Availability' : 'g:availability', 'Price' : 'g:price', 'Sale_Price' : 'g:sale_price', 'Product_Type' : 'g:product_type'}, axis=1)
        df['g:gtin'] = df['g:gtin'].fillna(0).astype('int64')
        df['g:description'] = df['g:description'].str.replace('"', '', regex=True)
        df['g:title'] = df['g:title'].str.replace('"', '', regex=True)
        df['g:description'] = df['g:description'].str.replace(" õ", "õ", regex=False)
        df['g:title'] = df['g:title'].str.replace(" õ", "õ", regex=False)
        df.dropna(subset=['g:link'], inplace=True)
        return df

if __name__ == "__main__":
        country = sys.argv[1]
        # Run process
        GoogleFeedCheil(country).run()