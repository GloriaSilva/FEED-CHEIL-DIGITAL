import pandas as pd
from config import result_path
from Trafficking_Cheil import StandarizedCategory

providers= ['AWIN','Facebook','KuantoKusta','Criteo']

tags_dict= {'KuantoKusta': 'reference'}

if __name__ == '__main__':
    
    get_new_categories= StandarizedCategory()

    for provider in providers:
        df = pd.read_csv(f'{result_path}/{provider}Feed.csv')
        df = get_new_categories.add_standarized_cats(df,tags_dict[provider] if provider in tags_dict else 'g:id')
        df.to_csv(f'{result_path}/division/{provider}FeedDivision_Cheil.csv',index=False)

