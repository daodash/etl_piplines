import os
import json
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

# load env variables
load_dotenv()
discourse_url = os.getenv("DISCOURSE_URL")
discourse_api_key = os.getenv("DISCOURSE_API_KEY")
discourse_api_username = os.getenv("DISCOURSE_API_USERNAME")
db_string = os.getenv('DB_STRING')

api_query = '{}/categories.json'.format(discourse_url)

# retrieve json results and convert to dataframe
result = requests.get(api_query).json()
result_items = result.items()
result_list = list(result_items)
result_list_of_dict = result_list[0][1].get('categories')
df = pd.json_normalize(result_list_of_dict)

# include only necessary columns
list_of_col_names = ['id', 'name', 'slug']
df = df.filter(list_of_col_names)
df['created_at'] = datetime.today()

# check existing records for MAX(id)
db = create_engine(db_string)
with db.connect() as conn:
    result = conn.execute(statement='SELECT MAX(id) AS max_id FROM daodash_ny.categories')
    for row in result:
        max_id = row.max_id
        print('max_id: ', max_id)

# include only new records (id > max_id)
df_filtered = df[df['id'].gt(max_id)]

# insert into records to db table
df_filtered.to_sql(name='categories', schema='daodash_ny', con=db, if_exists='append', index=False)
