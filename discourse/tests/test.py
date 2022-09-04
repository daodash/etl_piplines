import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
discourse_url = os.getenv("DISCOURSE_URL") #'http://localhost:4200/' | 'https://forum.bankless.community'
discourse_api_key = os.getenv("DISCOURSE_API_KEY")
discourse_api_username = os.getenv("DISCOURSE_API_USERNAME") #'All Users'

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
#api_query = '{}/users/{}.json?api_key={}&api_username={}'.format(discourse_url, 'RunTheJewelz', discourse_api_key, discourse_api_username)
#api_query = '{}/directory_items.json?period=all&order=topic_count&api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/u/{}/emails.json?api_key={}&api_username={}'.format(discourse_url, 'tomfutago', discourse_api_key, discourse_api_username)
#api_query = '{}/notifications.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)

# admin (n/a)
#api_query = '{}/admin/users/{}.json?api_key={}&api_username={}'.format(discourse_url, 823, discourse_api_key, discourse_api_username)
#params = 'order=created%20show_emails=true'
#api_query = '{}/admin/users/list/{}.json?{}&api_key={}&api_username={}'.format(discourse_url, 'active', params, discourse_api_key, discourse_api_username)

# topics
#api_query = '{}/latest.json?order=created&ascending=true&api_key={}&api_username={}&page=18'.format(discourse_url, discourse_api_key, discourse_api_username)
#api_query = '{}/t/{}.json?api_key={}&api_username={}'.format(discourse_url, 3661, discourse_api_key, discourse_api_username)
#https://{defaultHost}/t/{id}/posts.json + {"post_ids[]": 0}

# posts
#api_query = '{}/posts.json?api_key={}&api_username={}'.format(discourse_url, discourse_api_key, discourse_api_username)
api_query = '{}/posts/{}.json?api_key={}&api_username={}'.format(discourse_url, 14065, discourse_api_key, discourse_api_username)
#api_query = '{}/posts/{}/replies.json?api_key={}&api_username={}'.format(discourse_url, 4171, discourse_api_key, discourse_api_username)

# search
#search = 'q=@tomfutago'
#api_query = '{}/search.json?{}'.format(discourse_url, search)

#search = 'term=after:2021-01-01%20before:2022-01-01'
#api_query = '{}/search/query.json?{}&page=2'.format(discourse_url, search) #doesn't require api key

result = requests.get(api_query).json()
with open('./tests/samples/posts_single.json', 'w') as f:
    json.dump(result, f, indent=4)
#print(json.dumps(result, indent=4))
