import requests
import feedparser
import json
from bs4 import  BeautifulSoup
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import date, timedelta

def scrape_cnbc(day):
    authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
    discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
    discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

    env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
    collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'

    #feed = feedparser.parse('http://www.cnbc.com/id/100727362/device/rss/rss.html')
    content = requests.get(day.strftime("https://www.cnbc.com/site-map/%Y/%B/%d"), allow_redirects=True).content
    soup = BeautifulSoup(content, features="html.parser")
    articles_list = soup.find('div', {'class': 'SiteMapArticleList-articleData'})
    links = [article['href'] for article in articles_list.findChildren('a', recursive=True)]

    for link in links:
        print(link)
        try:
            content = requests.get(link, allow_redirects=True).content
            soup = BeautifulSoup(content, features="html.parser")
            article_title = soup.find('h1', {'class': lambda value: value and value.startswith("ArticleHeader")}).text
            article_body = ' '.join(x.text for x in soup.find_all('div',{'class':'group'}))
            article_date = date(*[int(x) for x in link.split('/')[-4:-1]])
            document = {
                'title': article_title,
                'body': article_body,
                'url': link,
                'year': article_date.year,
                'month': article_date.month,
                'day': article_date.day
            }
            discovery.add_document(env_id, collection_id, file=json.dumps(document), filename='-'.join(article_title.split(' ')), file_content_type='application/json')
        except Exception as e:
            print('Failed to parse or upload document')
            print(e)


    '''
    my_query = discovery.query(env_id, collection_id, query='*.*', count=50).get_result()
    for doc in my_query['results']:
        new_doc = {}
        print(doc['url'])
        article_date = date(*[int(x) for x in doc['url'].split('/')[-4:-1]])
        new_doc['title'] = doc['title']
        new_doc['body'] = doc['body']
        new_doc['url'] = doc['url']
        new_doc['year'] = article_date.year
        new_doc['month'] = article_date.month
        new_doc['day'] = article_date.day
        discovery.update_document(env_id, collection_id, doc['id'], file=json.dumps(new_doc), filename=doc['extracted_metadata']['filename'], file_content_type='application/json')
    '''
if __name__ == '__main__':

    reset = True
    if reset:
        authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
        discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
        discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

        env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
        collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'

        delete_docs = []
        for i in range(int(1000/50)):
            my_query = discovery.query(env_id, collection_id, query='*.*', count=50, offset=i*50).get_result()
            if len(my_query) == 0:
                break
            for doc in my_query['results']:
                if doc['month'] != 3 and (not (doc['month'] == 2 and doc['day'] >= 28)):
                    print(doc['title'], doc['month'], doc['day'])
                    delete_docs.append(doc['id'])
        for doc_id in delete_docs:
            discovery.delete_document(env_id, collection_id, doc_id)
    scrape_cnbc(date.today())
