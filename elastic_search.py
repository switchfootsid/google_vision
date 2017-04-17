# http://charlesleifer.com/blog/setting-up-elasticsearch-with-basic-auth-and-ssl-for-use-with-python/

import elasticsearch
from fuzzywuzzy import fuzz
import pandas as pd

class search_class:
    
    def __init__(self):
        self.new_db = elasticsearch.Elasticsearch()  
        
    def index_brand(self, brand_path):
        brand_repo = pd.read_csv(brand_path)
        for i in brand_repo.index:
            try:
                brand = brand_repo.loc[i, 'brand']
                self.new_db.index(index='brands', id=i, doc_type='message', body={'brand': brand})

                if i % 100 == 0:
                    print ('Brands: Done with ...', i)
            except KeyError: 
                #add logging
                pass
        print ('Brand indexing done')
        return None
    
    def index_tagline(self, tag_path):
        tag_repo = pd.read_excel(tag_path)
        for i in tag_repo.index:
            try:
                line = tag_repo.loc[i, 'TagLine']
                brand = tag_repo.loc[i, 'brand']
                self.new_db.index(index='tags', id=i, doc_type='message', body={'tagline': line, 'brand': brand}, request_timeout=10)

                if i % 100 == 0:
                    print ('Taglines: Done with ...', i)
            except KeyError: 
                pass
        print ('Tagline - Brand indexing done')
        return None
    
    def get_es(self):
    	return self.new_db