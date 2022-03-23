import pandas as pd
from config import templates_path
import sys
import os

if __name__ == '__main__':

    dir_excels_tracking = sys.argv[1]

    for filename in os.listdir(dir_excels_tracking):
        file_path = os.path.join(dir_excels_tracking,filename)
        if os.path.isfile(file_path) and 'FeedDivision_Cheil' in filename and not '~' in filename:
            print(file_path)
            df = pd.read_excel(file_path)
            df.rename(columns={'g:id':'id','reference':'id','designation':'title','g:title':'title','g:description':'description','Tracking':'tracking'},inplace=True)
            provider_name = os.path.splitext(filename)[0].replace('FeedDivision_Cheil','')
            
            if 'tracking' in df.columns:
                print(f'Generating {provider_name} template with new tracking')
                df[['id','title','description','tracking']].to_excel(os.path.join(templates_path,provider_name,f'ES_{provider_name}_Sheet_Template.xlsx'))
            else:
                print(f'Not found tracking for {provider_name}. Not generating new template')
