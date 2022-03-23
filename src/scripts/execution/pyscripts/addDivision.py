import pandas as pd
from config import result_path
from Trafficking_Cheil import StandarizedCategory

providers= ['AWIN','Facebook','KuantoKusta','Criteo']


if __name__ == '__main__':
    
    get_new_categories= StandarizedCategory()

    for provider in providers:
        df = pd.read_csv(f'{result_path}/{provider}Feed.csv')
        df.rename(columns={'g:id':'id','reference':'id','designation':'title','g:title':'title','g:description':'description','g:link':'link','product_url':'link'},inplace=True)
        df = get_new_categories.add_standarized_cats(df,'id')
        df.replace({r'https://www.samsung.com.*':'', '\<\!\[CDATA\[':'' },regex = True, inplace=True)
        df[['id','title','description','link','tk:division','tk:category','tk:subcategory']].to_excel(f'{result_path}/division/{provider}FeedDivision_Cheil.xlsx',index=False)

