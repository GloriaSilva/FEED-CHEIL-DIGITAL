import pandas as pd
from config import result_path
from Trafficking_Cheil import DivisionByCategory

providers= ['AWIN','Facebook','KuantoKusta','Criteo']

tags_dict= {'KuantoKusta': ('division','category'), 
            'Facebook': ('g:division','g:google_product_category'),
            'Criteo': ('g:division','g:google_product_category')}

if __name__ == '__main__':
    
    get_division= DivisionByCategory()

    for provider in providers:
        df = pd.read_csv(f'{result_path}/{provider}Feed.csv')
        tags = tags_dict[provider] if provider in tags_dict else ('g:division','g:product_type')
        df = get_division.add_division_to_df(df,*tags)
        df.to_csv(f'{result_path}/division/{provider}FeedDivision_Cheil.csv',index=False)

