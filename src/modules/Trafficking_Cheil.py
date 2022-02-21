from config import result_path, project_path
import os
import yaml

division_yml = f'{project_path}/src/dictionaries/division/division_pt.yml'

class DivisionByCategory(object):
    def __init__(self):
        self.dict_cat_div = self.get_dict_cat_div()
        print(self.dict_cat_div)
       

    def get_dict_cat_div(self):
        with open(division_yml) as f:
            # use safe_load instead load
            dict_div_cat = yaml.safe_load(f)
        
        print(dict_div_cat)
        return { category: division for division in dict_div_cat for category in dict_div_cat[division]  }

    def add_division_to_df(self,df, division_tag, category_tag):
        pat = '|'.join(r"\b{}\b".format(x) for x in self.dict_cat_div.keys())
        df[division_tag] = df[category_tag].str.extract('('+ pat + ')', expand=False).map(self.dict_cat_div)
        return df