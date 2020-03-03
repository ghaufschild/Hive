import praw
import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import datetime

def remove_non_ascii(text):
    return ''.join(i for i in text if ord(i)<128)

authenticator = IAMAuthenticator("6j66m1ZJdM6KYMYj8J074qXjWE6FLqsLG4XpA8Bm5Wog")
discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/instances/e3a97512-2f2e-4ff6-88c3-2255a1e6f56d')

env_id = '6afed5c1-e09a-4407-bd3a-2659124616af'
collection_id = 'afc340a2-57dc-486c-b471-9b687e2505c4'

reddit = praw.Reddit(client_id='JwuaAJFEkxPH6A',
                     client_secret='I-OFNj8ZuWSWWnG2gBCk9cG9-2k',
                     password='thisisabotforahivewebsite',
                     user_agent='scraper by /u/hivebot5914',
                     username='hivebot5914')

reset = True

if reset:
    for i in range(int(1000/50)):
        my_query = discovery.query(env_id, collection_id, query='*.*', count=50).get_result()
        if len(my_query) == 0:
            break
        for doc in my_query['results']:
            print(doc['title'])
            discovery.delete_document(env_id, collection_id, doc['id'])

character_limit = 50000

subreddit_names = ['inthenews', 'UpliftingNews', 'news', 'worldnews']
for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)
    for post in subreddit.top('week', limit=int(100/len(subreddit_names))):
        post_title = remove_non_ascii(post.title)
        post_url = post.shortlink
        print(post_title, post_url)
        post_body = remove_non_ascii('\n'.join(comment.body for comment in post.comments if type(comment) == praw.models.reddit.comment.Comment))
        if len(post_body) >= character_limit:
            post_body = post_body[:character_limit]
        post_time = post.created
        post_date = datetime.fromtimestamp(post.created)
        post_score = post.score,
        post_upvote_ratio = post.upvote_ratio
        document = {
            'title': post_title,
            'body': post_body,
            'url': post_url,
            'year': post_date.year,
            'month': post_date.month,
            'day': post_date.day,
            'hour': post_date.hour,
            'minute': post_date.minute,
            'second': post_date.second,
            'time': post_time,
            'score': post_score,
            'upvote_ratio': post_upvote_ratio,
        }
        doc_id = post_url
        discovery.update_document(env_id, collection_id, doc_id, file=json.dumps(document), filename='-'.join(post_title.split(' ')), file_content_type='application/json')
