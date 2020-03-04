from datetime import date, timedelta
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class Hive(object):
    def __init__(self, source='reddit'):
        self.source = source
        if source == 'cnbc':
            authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
            self.discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
            self.discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')
            self.env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
            self.collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'
        elif source == 'reddit':
            authenticator = IAMAuthenticator("6j66m1ZJdM6KYMYj8J074qXjWE6FLqsLG4XpA8Bm5Wog")
            self.discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
            self.discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/instances/e3a97512-2f2e-4ff6-88c3-2255a1e6f56d')
            self.env_id = '6afed5c1-e09a-4407-bd3a-2659124616af'
            self.collection_id = 'afc340a2-57dc-486c-b471-9b687e2505c4'
        else:
            raise SystemError

    def get_query_for_specific_day(self, query, year, month, day):
        my_query = self.discovery.query(
            self.env_id,
            self.collection_id,
            natural_language_query=query,
            count=50,
            filter='year::' + str(year) + ',month::' + str(month) + ',day::' + str(day)
        ).get_result()

        return my_query

    def get_average_sentiment_score(self, query_results, confidence_threshold=0.2):
        query_results['results'] = list(filter(lambda doc: doc['result_metadata']['confidence'] > confidence_threshold, query_results['results']))
        total_items = len(query_results['results'])
        if total_items == 0:
            return None

        for doc in query_results['results']:
            if not 'enriched_body' in doc:
                print(doc)

        confidence_sum = sum(doc['result_metadata']['confidence'] for doc in query_results['results'])
        sentiment_sum = sum(doc['enriched_body']['sentiment']['document']['score']*doc['result_metadata']['confidence'] for doc in query_results['results'])
        
        return sentiment_sum/confidence_sum/total_items

    def get_closest_result(self, results, target_sentiment, confidence_threshold=0.2):
        closest_result = None

        closest_distance = float('inf')

        for current_result in results['results']:
            if current_result['result_metadata']['confidence'] > confidence_threshold:
                sentiment_score = current_result['enriched_body']['sentiment']['document']['score']

                distance_to_target = abs(sentiment_score - target_sentiment)

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
            
            days_results = self.get_query_for_specific_day(query, current_date.year, current_date.month, current_date.day)
            
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
    hive = Hive(source='reddit')
    print(hive.get_results('coronavirus', date.today(), 7))
