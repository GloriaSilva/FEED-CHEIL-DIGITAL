"""
FeedCheil class is the parent class for any platform feed that could come later.
This way, this class is the common frame where every repeated task is stored.
Every child class will apply their specific differences and creates their own functions to generate the specific platform feed
"""

# dependencies
import json
import pandas as pd
import numpy as np
import datetime
from sqlalchemy import create_engine
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html
from config import project_path, templates_path, result_path, database_info
import os
from Utils import generate_random_int

sendErrorActive = False

# Class
class FeedCheil:
    # Constructor
    def __init__(self, country, rows):
        # Connect to the database
        self.mydb = create_engine('mysql+pymysql://' + database_info['user'] + ':' + database_info['passw'] + '@' + database_info['host'] + ':' + str(database_info['port']) + '/' + database_info['database'] , echo=False)

        # paths to files
        self.dictionariesPath = f'{project_path}/src/dictionaries'
        self.resultPath = result_path
        self.templatePath = templates_path

        #Init dataFrame
        pd.DataFrame.to_xml = FeedCheil.to_xml
        # define rows
        self.rows = rows;
        #define country variable
        self.country = country
        #Samsung feed URL
        self.url = f'https://shop.samsung.com/{country}/googleShoppingFeed?{generate_random_int(100000)}'
        self.Google_feed_maestroCSV = f'{self.dictionariesPath}/maestro/GoogleFeed_maestro_{self.platform}_{self.country}.csv'

    #Cheil personal "To XML" function
    def to_xml(df, country='pt', filename=None, mode='w'):
        header=f"""<?xml version="1.0"?>
    <rss xmlns="http://base.google.com/ns/1.0" xmlns:g="http://base.google.com/ns/1.0" version="2.0">
    <channel>
    <title>Samsung Shop {country.upper()}</title>
    <link>http://www.samsung.com/{country}</link>
    <description>Feed developed by Cheil Spain (Ramón Mariño Solís via Python) for Google Merchant provider.</description>
    """
        footer = """</channel>
    </rss>"""
        def row_to_xml(row):
            xml = ['<item>']
            for i, col_name in enumerate(row.index):
                xml.append('  <{0}>{1}</{0}>'.format(col_name, row.iloc[i]))
            xml.append('</item>')
            return '\n'.join(xml)
        res = '\n'.join(df.apply(row_to_xml, axis=1))

        if filename is None:
            return header+res+footer
        with open(filename, mode) as f:
            f.write(header+res+footer)


    # Send Error fucntion. When there is a problem collecting Samsung Feed, an emails is sent.
    def sendError(self):
        if not self.sendErrorActive:
            return
            
        query = 'SELECT email FROM `accounts`'
        mails = pd.read_sql(query, con = self.mydb)
        mailslist = mails['email'].tolist()

        # create message object instance
        msg = MIMEMultipart()

        message = '<img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Cheil_Worldwide_logo.svg" alt="Cheil logo" style="display: block; margin-left: auto;   margin-right: auto; margin-top:5px;">\
                <p style="font-size:16px; margin-top:35px; margin-bottom:35px; margin-right:15px; margin-left:15px; padding:20px; background-color: #F8F8F8; line-height: 30px">Hi team,<br/>Just inform that there is an issue with Hybris Feed so automatic feed could not be updated.</br>\
                <br>Regards,</p><div style="font-size:smaller; color:grey;text-align:center">***This is an automatically generated email, please do not reply to this message.***<br>Automated and developed by <a href="mailto:raul.fernandez@cheil.com?subject="INFO-AUTOMATION" style="color:black"> Raúl Fernández</a></div></p>'

        # setup the parameters of the message
        password = config['email']['passw']
        msg['From'] = config['email']['from']
        msg['To'] = ", " .join(mailslist)
        msg['Subject'] = config['email']['subject']

        # add in the message body
        msg.attach(MIMEText(message, 'html'))

        #create server
        server = smtplib.SMTP(config['email']['host'])
        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

        print ("successfully sent email to %s:" % (msg['To']))


    def filterXMLid(self,xml_id_tag):
        return xml_id_tag is None or xml_id_tag.text == "" or any([ prefix in xml_id_tag.text for prefix in ['ET-','EF-','HAF-']])
    #The following functions are all developed in the child classes
    def openFileAndScrap(self):
        #This function gets the specific Samsung Feed that any platform needs
        pass

    def cleanCSV(self):
        #After getting the feed, the file is cleaned based on business rules.
        pass

    def setLink(self, df):
        #Links from url_dictionary (each country has its own) are linked to the product ID. Also, the cid is added at the end of the url
        pass

    def run(self):
        # Init process
        self.begin_time = datetime.datetime.now()
        print(datetime.datetime.now())
        # Open file and Scrap
        self.openFileAndScrap()
        #In case the url_dictionary file specific for any country is not available, the program will get the previous version. it should only work the first time
        #Think about erase it after the solution is in production
    
        dic = pd.read_csv(f'{self.dictionariesPath}/url/url_dictionary_{self.country}.csv', index_col=0).squeeze("columns")

        #Creating the dictionary object which connects the product ID with the final URL obtained after all the redirections
        dictionary = dict(zip(dic['Id'],dic['Link']))

        #Importing the file with the feed obtained from the function openFileAndScrap
        df = pd.read_csv(self.Google_feed_maestroCSV, encoding='latin')
        #The following rows clear the dataframe from any row which has no ImageLink or Price
        index_to_drop = df.query('Image_Link == "" | Price == "" ').index
        df.drop(index_to_drop, inplace=True)
        #Associating the final URL with the product ID
        df['Link'] = df['Id'].map(dictionary).fillna(df['Link'])

        #The following logic aims to generate the field "categories" which classifies each product. This field is used for creating the "cid".
        col  = 'Id'
        conditions  = [ df[col].str.match('SM-A') | df[col].str.match('SM-G') | df[col].str.match('SM-N') | df[col].str.match('SM-F') | df[col].str.match('SM-M') | df[col].str.match('SM-S'),
        df[col].str.match('SM-P') | df[col].str.match('SM-T') | df[col].str.match('SM-X'),
        df[col].str.match('SM-R'),
        df[col].str.match('EF-') | df[col].str.match('EP-') | df[col].str.match('EB-') | df[col].str.match('ET-') | df[col].str.match('GP-'),
        df[col].str.match('DV') | df[col].str.match('WW'),
        df[col].str.match('DW'),
        df[col].str.match('HAF-'),
        df[col].str.match('MC') | df[col].str.match('MG') | df[col].str.match('MS'),
        df[col].str.match('NK') | df[col].str.match('NV') | df[col].str.match('NZ'),
        df[col].str.match('RB') | df[col].str.match('RL') | df[col].str.match('RR') | df[col].str.match('RS') | df[col].str.match('RT') | df[col].str.match('RZ'),
        df[col].str.match('VC') | df[col].str.match('VS'),
        df[col].str.match('QE') | df[col].str.match('UE'),
        df[col].str.match('SP-'),
        df[col].str.match('HW-'),
        df[col].str.match('VG-'),
        df[col].str.match('LC') | df[col].str.match('LS') | df[col].str.match('LF') | df[col].str.match('LU'),
        df[col].str.match('MU-') | df[col].str.match('MZ-'),
        ]
        choices = [ "im-smartphone", 'im-tablet', 'im-wearables', 'im-accessories', 'da-washing', 'da-dishwasher', 'da-accessories',  'da-microwave', 'da-kitchen', 'da-refrigerator', 'da-vacuum', 'vd-television', 'vd-projector', 'vd-audio', 'vd-accessories', 'it-monitor', 'it-memory'  ]

        
        df['category'] = np.select(conditions, choices, default='none-none')
        #Creating the cid (tracking Id) based on specific rules
        df['TrackingId'] = 'cid='+ self.country +'_pd_ppc_'+self.platform+'_'+df['Title'].replace({' ':'-', '\/':'-', '\&':'and', '&':'and'}, regex=True).str.lower()+'-'+df['Id'].replace({'/':'-'}, regex=True).str.lower()+'_ongoing_'+df['category']+'-automatic-feed_pla_none_none'
        df['TrackingId'] = df['TrackingId'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        #Finaly, we create a dictionary associating the product ID with the tracking ID we have just assembled
        tracking = dict(zip(df['Id'],df['TrackingId']))

        #We import the dictionary which allows us to handle HTML entities
        dictlan_from_csv = pd.read_csv(self.dictionariesPath + '/language/dict_language.csv', header=None, index_col=0).squeeze("columns").to_dict()
        #We apply the dictionary to all Titles and Descriptions in our feed
        df['Title'] = df['Title'].replace(dictlan_from_csv, regex=True)
        df['Description'] = df['Description'].replace(dictlan_from_csv, regex=True).fillna(df['Description'])
        df['Image_Link'] = df['Image_Link'].replace({'ORIGIN_PNG': '320_320_PNG'}, regex=True).fillna(df['Image_Link'])

        #We apply cleanCSV and setLink fucntions to the df we are working with
        df = self.cleanCSV(df)
        df = self.setLink(df,tracking)
        
        #We handle any NA on Link field
        df['Link'].fillna('', inplace=True)
        
        #We correct those URLs whic contains the "modelCode" as the cid is another parameter and not the first one
        df.loc[df['Link'].str.contains('\?modelCode='), 'Link'] = df['Link'].replace({'\?cid': '&cid'}, regex=True).fillna(df['Link'])

        #We import another dictionary to replace any symbol with funny characters which could break an URL.
        inverse_dictlan_from_csv = pd.read_csv(self.dictionariesPath + '/language/inverse_dict_language.csv', header=None, index_col=0, squeeze=True).to_dict()
        #We use that dictionary to handle those characters
        df['Link'] = df['Link'].replace(inverse_dictlan_from_csv, regex=True)
        #The function unescape from html module cleans the URLs where some HTML entities could create problems and make the URL break
        df['Link'] = html.unescape(df['Link'])

        #Finally, any valye within the following variables are replaced by nothing (""). This would help us to later remove those rows.
        values_to_replace=['NA','NaN', 'nan']
        values_to_replace_regex = ['\(','\)','TM','polegadas',"''"]
        df['Link'] = df['Link'].replace(values_to_replace, regex=False)
        df['Link'] = df['Link'].replace(values_to_replace_regex, '',regex=True)
        #Also, we replace the "+" symbol for the description
        df['Link'] = df['Link'].replace('\+','plus', regex=True)
        #Cleaning any product which has no link
        df = df.dropna(subset=['Link'])


        #We apply certain rules in terms of column names, data types and final characther cleaning.
        df = self.setDF(df)
        
        print(df.columns)
        print('Finished')
        
       

        #Before exporting the XML version we apply new considerations avoiding the XML break
        df['g:title'] = df['g:title'].str.replace('&','and')
        df['g:description'] = df['g:description'].str.replace('&','and')
        #We use the CDATA label for allowing literal strings wihtin the XML witout breaking.
        df['g:link'] = df['g:link'].apply(lambda x: '<![CDATA['+ x +']]>')

        #Exporting the final result, the platform Feed, as a csv file
        print(self.csvFile)
        df.to_csv(os.path.join(self.resultPath,self.csvFile), sep = ",", index=False)

        print(self.xmlFile)
        df.to_xml(filename = os.path.join(self.resultPath,self.xmlFile), country=self.country)

        #Process finish
        print("CSV and XML created")
        #Process duration
        print(datetime.datetime.now() - self.begin_time)
