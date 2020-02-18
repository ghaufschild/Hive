from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import date, timedelta

authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'


def getQueryForSpecificDay(query, year, month, day):
    my_query = discovery.query(
        env_id,
        collection_id,
        natural_language_query=query,
        count=50,
        filter='year::' + str(year) + ',month::' + str(month) + ',day::' + str(day)
    ).get_result()

    return my_query


def get_average_sentiment_score(queryResults):
    sentimentSum = 0.00
    totalItems = 0

    for doc in queryResults['results']:
        if doc['result_metadata']['confidence'] > 0.01:
            sentimentSum = sentimentSum + doc['enriched_body']['sentiment']['document']['score']
            totalItems = totalItems + 1

    if totalItems == 0:
        averageSentiment = None
    else:
        averageSentiment = sentimentSum / totalItems

    return averageSentiment


def getClosestResult(results, targetSentiment):
    closestResult = None

    closestResultDistance = 5

    for currentResult in results['results']:
        if currentResult['result_metadata']['confidence'] > 0.01:
            sentimentScore = currentResult['enriched_body']['sentiment']['document']['score']

            distanceToTarget = abs(sentimentScore - targetSentiment)

            if (distanceToTarget < closestResultDistance):
                closestResultDistance = distanceToTarget
                closestResult = currentResult

    return closestResult


def get_results(query, end_date, days_prior):
    result_dictionary = {
        'query_string': query,
        'ending_date': str(end_date),
        'days_prior': days_prior,
    }

    day_list = []

    start_date = end_date - timedelta(days=(days_prior - 1))

    for daysAgo in range(days_prior):
        current_date = start_date + timedelta(days=daysAgo)

        days_results = getQueryForSpecificDay(query, current_date.year, current_date.month, current_date.day)

        sentiment_score = get_average_sentiment_score(days_results)

        if sentiment_score is not None:
            returnResult = getClosestResult(days_results, sentiment_score)

            currentDayInformationDict = {
                'month': str(current_date.month),
                'day': str(current_date.day),
                'year': str(current_date.year),
                'y': sentiment_score,
                'url': returnResult['url'],
                'title': returnResult['title']
            }
            day_list.append(currentDayInformationDict)

    result_dictionary['results'] = day_list

    return result_dictionary

if __name__ == '__main__':
    print(get_results("Tesla", date.today(), 7))