from config import result_path, project_path
import os
import yaml
import pandas as pd

cats_yml = f'{project_path}/src/dictionaries/division/categories_pt.yml'

class StandarizedCategory(object):
    def __init__(self):
        self.transform_cats = self.get_transform_cats()
        
       

    def get_transform_cats(self):
        with open(cats_yml) as f:
            # use safe_load instead load
            tranform_cats_yaml = yaml.safe_load(f)
        
        
        return {el['IDENTIFICADOR']: (el['DIVISION'],el['CATEGORIA'],el['SUBCATEGORIA']) for el in tranform_cats_yaml}

    def add_standarized_cats(self,df, sku_tag):
        pat = '|'.join(r"^{}".format(x) for x in self.transform_cats.keys())
        df['tk:all']= df[sku_tag].str.extract('('+ pat + ')', expand=False).map(self.transform_cats)
        df[['tk:division','tk:category','tk:subcategory']] = pd.DataFrame(df['tk:all'].tolist(), index=df.index)
        df.drop('tk:all', axis=1, inplace=True)
        return df