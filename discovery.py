import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)

discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

environments = discovery.list_environments().get_result()
print(json.dumps(environments, indent=2))

env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'

collections = discovery.list_collections(env_id).get_result()
wikinews_collections = [x for x in collections['collections']]
print(json.dumps(collections, indent=2))


#my_query = discovery.query('b098ddfa-f993-407c-bd74-b20a2c6fc54f',
#                           'c76cbe5e-0d22-49b9-a3db-ae9fc3606586',
#                           filter='enriched_text.emotion.document.emotion.disgust>=0.4').get_result()

#print(my_query['results'][0]['text'])
