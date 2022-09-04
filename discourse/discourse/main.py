import os
import requests
import pandas as pd
import sqlalchemy as db
from dotenv import load_dotenv
from typing import Optional, Dict

# load env variables
load_dotenv()
discourse_url = os.getenv("DISCOURSE_URL")
discourse_api_key = os.getenv("DISCOURSE_API_KEY")
discourse_api_username = os.getenv("DISCOURSE_API_USERNAME")
db_string = os.getenv('DB_STRING')
db_schema = os.getenv('DB_SCHEMA') #daodash_ny

# create db engine
db_engine = db.create_engine(db_string)

def get_table_max_id(table_name: str) -> int:
    """
    Get MAX(id) for given table_name
    """
    sql = 'SELECT MAX(id) AS max_id FROM {}.{};'.format(db_schema, table_name)
    with db_engine.connect() as conn:
        result = conn.execute(statement=sql)
        for row in result:
            max_id = row.max_id
        if max_id is None:
            max_id = 0
        #print(table_name, 'max_id:', max_id)
    return max_id

# source: https://blog.alexparunov.com/upserting-update-and-insert-with-pandas
def create_upsert_method(meta: db.MetaData, extra_update_fields: Optional[Dict[str, str]]):
    """
    Create upsert method that satisfied the pandas's to_sql API.
    """
    def method(table, conn, keys, data_iter):
        # select table that data is being inserted to (from pandas's context)
        sql_table = db.Table(table.name, meta, autoload=True)
        
        # list of dictionaries {col_name: value} of data to insert
        values_to_insert = [dict(zip(keys, data)) for data in data_iter]
        
        # create insert statement using postgresql dialect
        insert_stmt = db.dialects.postgresql.insert(sql_table, values_to_insert)

        # create update statement for excluded fields on conflict
        update_stmt = {exc_k.key: exc_k for exc_k in insert_stmt.excluded if exc_k.key != 'created_at'}
        if extra_update_fields:
            update_stmt.update(extra_update_fields)
        
        # create upsert statement
        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=sql_table.primary_key.columns, # index elements are primary keys of a table
            set_=update_stmt # the SET part of an INSERT statement
        )
        
        # execute upsert statement
        conn.execute(upsert_stmt)

    return method


########################################################
# Categories
api_query = '{}/categories.json'.format(discourse_url)
table_name = 'discourse_categories'

# retrieve json results and convert to dataframe
result = requests.get(api_query).json()
df = pd.json_normalize(result['category_list']['categories'])

# include only necessary columns
list_of_col_names = ['id', 'name', 'slug']
df = df.filter(list_of_col_names)

# create DB metadata object that can access table names, primary keys, etc.
meta = db.MetaData(db_engine, schema=db_schema)

# dictionary which will add additional changes on update statement
# i.e. all the columns which are not present in DataFrame, but needed to be updated regardless
extra_update_fields = {"updated_at": "NOW()"}

# create upsert method that is accepted by pandas API
upsert_method = create_upsert_method(meta, extra_update_fields)

# perform upsert of df DataFrame values to a table `table_name` and Postgres connection defined at `db_engine`
df.to_sql(
    name=table_name,
    con=db_engine,
    schema=db_schema,
    index=False,
    if_exists='append',
    method=upsert_method
)


########################################################
# Users
for page_n in range(100):
    api_query = '{}/directory_items.json?period=all&order=topic_count&page={}'.format(discourse_url, page_n)
    table_name = 'discourse_users'

    # retrieve json results and convert to dataframe
    result = requests.get(api_query).json()
    df = pd.json_normalize(result['directory_items'])

    # check if current page contains any users, exit loop if it doesn't
    if df.empty is True:
        break

    # change json column names to match table column names
    df = df.rename(columns={
        'user.username': 'username',
        'user.name': 'name'
    }, inplace=False)

    # include only necessary columns
    list_of_col_names = [
        'id', 'username', 'name', 'days_visited', 'time_read', 'topics_entered', 
        'topic_count', 'posts_read', 'post_count', 'likes_received', 'likes_given'
    ]
    df = df.filter(list_of_col_names)

    # create DB metadata object that can access table names, primary keys, etc.
    meta = db.MetaData(db_engine, schema=db_schema)

    # dictionary which will add additional changes on update statement
    # i.e. all the columns which are not present in DataFrame, but needed to be updated regardless
    extra_update_fields = {"updated_at": "NOW()"}

    # create upsert method that is accepted by pandas API
    upsert_method = create_upsert_method(meta, extra_update_fields)

    # perform upsert of df DataFrame values to a table `table_name` and Postgres connection defined at `db_engine`
    df.to_sql(
        name=table_name,
        con=db_engine,
        schema=db_schema,
        index=False,
        if_exists='append',
        chunksize=200, # it's recommended to insert data in chunks
        method=upsert_method
    )


########################################################
# Topics
for page_n in range(50): # check for more_topics_url instead?
    api_query = '{}/latest.json?order=created&ascending=true&api_key={}&api_username={}&page={}'.format(
        discourse_url, discourse_api_key, discourse_api_username, page_n
    )
    table_name = 'discourse_topics'

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
        'id', 'title', 'slug', 'user_id', 'category_id', 'excerpt', 'created_at', 'last_post_user_id', 'last_posted_at', 
        'views_count', 'posts_count', 'reply_count', 'like_count', 'is_pinned', 'is_visible', 'is_closed', 'is_archived'
    ]
    df = df.filter(list_of_col_names)
    #print(df)

    # check existing records for MAX(id)
    max_id = get_table_max_id(table_name)

    # include only new records (id > max_id)
    df_filtered = df[df['id'].gt(max_id)]

    # insert into records to db_engine table
    df_filtered.to_sql(name=table_name, schema=db_schema, con=db_engine, if_exists='append', index=False)


########################################################
# Posts & Polls
sql = 'SELECT id AS topic_id FROM {}.{} ORDER BY 1;'.format(db_schema, 'discourse_topics')
with db_engine.connect() as conn:
    result = conn.execute(statement=sql)
    for row in result:
        topic_id = row.topic_id

        api_query = '{}/t/{}.json?api_key={}&api_username={}'.format(
            discourse_url, topic_id, discourse_api_key, discourse_api_username
        )
        table_name = 'discourse_posts'

        # retrieve json results for posts
        result = requests.get(api_query).json()
        print(topic_id, result['posts_count'])
        #df = pd.json_normalize(result['post_stream']['posts'])

        # check if current topic contains any data, if it doesn't - skip and continue
        if df.empty is True:
            continue


########################################################
# final clean up
db_engine.dispose()
