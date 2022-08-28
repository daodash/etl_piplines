import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
discourse_url = os.getenv("discourse_url") #'http://localhost:4200/' | 'https://forum.bankless.community'
discourse_api_key = os.getenv("discourse_api_key")
discourse_api_username = os.getenv("discourse_api_username") #'All Users'

# generic info
#api_query = '{}/site.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/tag_groups.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/tags.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/tag/test_tag.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/groups.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#https://{defaultHost}/groups/{id}.json
#https://{defaultHost}/groups/{id}/members.json

# categories
#api_query = '{}/categories.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}//c/Uncategorized/1.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)

# users
#api_query = '{}/users/{}.json?api_key={}&api_username={}'.format(discourse_url, 'tomfutago', discourse_api_key, discourse_api_username)
#api_query = '{}/directory_items.json?period=all&order=topic_count&api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/u/{}/emails.json?api_key={}&api_username={}'.format(discourse_url, 'tomfutago', discourse_api_key, discourse_api_username)
#api_query = '{}/notifications.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)

# posts
#api_query = '{}/posts.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/posts/10.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/posts/1/replies.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)

# topics
#api_query = '{}/latest.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#https://{defaultHost}/t/{id}.json
#https://{defaultHost}/t/{id}/posts.json + {"post_ids[]": 0}

# search
#search = 'q=@tomfutago'
#api_query = '{}/search.json?{}'.format(discourse_url, search)

search = 'term=after:2021-01-01%20before:2022-01-01'
api_query = '{}/search/query.json?{}&page=10'.format(discourse_url, search) #doesn't require api key

result = requests.get(api_query).json()
with open('./tests/samples/search_results.json', 'w') as f:
    json.dump(result, f, indent=4)
#print(json.dumps(result, indent=4))
