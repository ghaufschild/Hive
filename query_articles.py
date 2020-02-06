import requests
from datetime import date, timedelta
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'

my_query = discovery.query(env_id, collection_id, natural_language_query='coronavirus', count=50).get_result()

days = [date.today() + timedelta(days=d) for d in range(-4,1)]

for doc in my_query['results']:
    if doc['result_metadata']['confidence'] > 0.01:
        print(doc['title'], doc['enriched_body']['sentiment']['document']['score'])

