from datetime import date, timedelta
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class DataPool(object):
    def __init__(self, sources):
        possible_sources = ['cnbc', 'reddit']
        self.discoverers = []
        for source in sources:
            assert source in possible_sources, 'invalid source specified for data pool'
            if source == 'cnbc':
                authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
                discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
                discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')
                env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
                collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'
            elif source == 'reddit':
                authenticator = IAMAuthenticator("6j66m1ZJdM6KYMYj8J074qXjWE6FLqsLG4XpA8Bm5Wog")
                discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
                discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/instances/e3a97512-2f2e-4ff6-88c3-2255a1e6f56d')
                env_id = '6afed5c1-e09a-4407-bd3a-2659124616af'
                collection_id = 'afc340a2-57dc-486c-b471-9b687e2505c4'
            self.discoverers.append({'discovery': discovery, 'env_id': env_id, 'collection_id': collection_id})

    def get_query_for_specific_day(self, query, year, month, day):
        results = []
        for discoverer in self.discoverers:
            discovery = discoverer['discovery']
            env_id = discoverer['env_id']
            collection_id = discoverer['collection_id']
            my_query = discovery.query(
                env_id,
                collection_id,
                natural_language_query=query,
                count=50,
                filter='year::' + str(year) + ',month::' + str(month) + ',day::' + str(day)
            ).get_result()
            results.extend(my_query['results'])
        return results

class Hive(object):
    def __init__(self, sources):
        self.datapool = DataPool(sources=sources)

    def get_average_sentiment_score(self, results, confidence_threshold=0.03):
        results = list(filter(lambda doc: doc['result_metadata']['confidence'] > confidence_threshold, results))
        total_items = len(results)
        if total_items == 0:
            return None

        for doc in results:
            if not 'enriched_body' in doc:
                print(doc)

        confidence_sum = sum(doc['result_metadata']['confidence'] for doc in results)
        sentiment_sum = sum(doc['enriched_body']['sentiment']['document']['score']*doc['result_metadata']['confidence'] for doc in results)
        
        return sentiment_sum/confidence_sum

    def get_closest_result(self, results, target_sentiment, confidence_threshold=0.03):
        closest_result = None

        closest_distance = float('inf')

        for current_result in results:
            if current_result['result_metadata']['confidence'] > confidence_threshold:
                sentiment_score = current_result['enriched_body']['sentiment']['document']['score']

                distance_to_target = abs(sentiment_score - target_sentiment)/current_result['result_metadata']['confidence']

                if (distance_to_target < closest_distance):
                    closest_distance = distance_to_target
                    closest_result = current_result
                    
        return closest_result

    def get_results(self, query, end_date, days_prior):
        result_dictionary = {
            'query_string': query,
            'ending_date': str(end_date),
            'days_prior': days_prior,
        }
        
        day_list = []
        
        start_date = end_date - timedelta(days=(days_prior - 1))
        
        for daysAgo in range(days_prior):
            current_date = start_date + timedelta(days=daysAgo)
            
            days_results = self.datapool.get_query_for_specific_day(query, current_date.year, current_date.month, current_date.day)
            print(len(days_results))
            
            sentiment_score = self.get_average_sentiment_score(days_results)
            
            if sentiment_score is not None:
                return_result = self.get_closest_result(days_results, sentiment_score)
            
                current_day_information_dict = {
                    'month': str(current_date.month),
                    'day': str(current_date.day),
                    'year': str(current_date.year),
                    'y': sentiment_score,
                    'url': return_result['url'],
                    'title': return_result['title']
                }
                day_list.append(current_day_information_dict)
            
        result_dictionary['results'] = day_list

        return result_dictionary

if __name__ == '__main__':
    hive = Hive(sources=['reddit', 'cnbc'])
    print(hive.get_results('coronavirus', date.today(), 7))
