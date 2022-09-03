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

# create db engine
db = create_engine(db_string)


########################################################
# Categories
api_query = '{}/categories.json'.format(discourse_url)

# retrieve json results and convert to dataframe
result = requests.get(api_query).json()
df = pd.json_normalize(result['category_list']['categories'])

# include only necessary columns
list_of_col_names = ['id', 'name', 'slug']
df = df.filter(list_of_col_names)
df['created_at'] = datetime.today()

# check existing records for MAX(id)
with db.connect() as conn:
    result = conn.execute(statement='SELECT MAX(id) AS max_id FROM daodash_ny.discourse_categories')
    for row in result:
        max_id = row.max_id
    if max_id is None:
        max_id = 0
    #print('discourse_categories max_id: ', max_id)

# include only new records (id > max_id)
df_filtered = df[df['id'].gt(max_id)]

# insert into records to db table
df_filtered.to_sql(name='discourse_categories', schema='daodash_ny', con=db, if_exists='append', index=False)


########################################################
# Topics
for page_n in range(50): # check for more_topics_url instead?
    api_query = '{}/latest.json?order=created&ascending=true&api_key={}&api_username={}&page={}'.format(
        discourse_url, discourse_api_key, discourse_api_username, page_n
    )

    # retrieve json results
    result = requests.get(api_query).json()
    #print(result['topic_list']['topics'])
    df = pd.json_normalize(result['topic_list']['topics'])

    # check if current page contains any topics, exit loop if it doesn't
    if df.empty is True:
        break

    # change json column names to match table column names
    df = df.rename(columns={
        'views': 'views_count',
        'pinned_globally': 'is_pinned',
        'visible': 'is_visible',
        'closed': 'is_closed',
        'archived': 'is_archived'
    }, inplace=False)

    # extract original and most recent poster using list comprehansion
    #[print(n, x['description'], x['user_id']) for n in range(0, len(df)) for x in df['posters'][n] if 'Original Poster' in x['description']]
    df['user_id'] = [
        x['user_id'] 
            for n in range(0, len(df)) 
                for x in df['posters'][n] 
                    if 'Original Poster' in x['description']
    ]
    df['last_post_user_id'] = [
        x['user_id'] 
            for n in range(0, len(df)) 
                for x in df['posters'][n] 
                    if 'Most Recent Poster' in x['description']
    ]

    # include only necessary columns
    list_of_col_names = [
        'id', 'title', 'slug', 'user_id', 'category_id', 'created_at', 'last_post_user_id', 'last_posted_at', 
        'views_count', 'posts_count', 'reply_count', 'like_count', 'is_pinned', 'is_visible', 'is_closed', 'is_archived'
    ]
    df = df.filter(list_of_col_names)
    #print(df)

    # check existing records for MAX(id)
    with db.connect() as conn:
        result = conn.execute(statement='SELECT MAX(id) AS max_id FROM daodash_ny.discourse_topics')
        for row in result:
            max_id = row.max_id
        if max_id is None:
            max_id = 0
        #print('discourse_categories max_id: ', max_id)

    # include only new records (id > max_id)
    df_filtered = df[df['id'].gt(max_id)]

    # insert into records to db table
    df_filtered.to_sql(name='discourse_topics', schema='daodash_ny', con=db, if_exists='append', index=False)
