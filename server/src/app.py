from flask import Flask, render_template, make_response
import os
import time
import requests
from datetime import date, timedelta
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


app = Flask(__name__)

authenticator = IAMAuthenticator("EBkvmVslhKY36GZBRJ44attJ4zYkSfKIfmlUG2B0_8p6")
discovery = DiscoveryV1(version="2019-04-30", authenticator=authenticator)
discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/622978c2-cc19-4abd-bc99-ef72da6c53fd')

env_id = 'b098ddfa-f993-407c-bd74-b20a2c6fc54f'
collection_id = '02d700e6-69c2-4d51-9d2f-b09e8e15ce8d'

def format_server_time():
  server_time = time.localtime()
  return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    
    # 1
    template = render_template('index.html', context=context)
    # 2
    response = make_response(template)
    # 3
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'

    return response



def getQueryForSpecificDay(query, year, month, day):
    my_query = discovery.query(
        env_id,
        collection_id,
        natural_language_query=query,
        count=50,
        filter='year::' + str(year) + ',month::' + str(month) + ',day::' + str(day)
    ).get_result()

    return my_query

def getAverageSentimentScore(queryResults):
    sentimentSum = 0.00
    totalItems = 0

    for doc in queryResults['results']:
        if doc['result_metadata']['confidence'] > 0.01:
            sentimentSum = sentimentSum + doc['enriched_body']['sentiment']['document']['score']
            totalItems = totalItems + 1

    averageSentiment = sentimentSum / totalItems

    return averageSentiment

def getResults(query, endDate, daysPrior):

    resultDictionary = {
        'queryString' : query,
        'endingDate' : str(endDate),
        'daysPrior' : daysPrior,

    }

    dayQueryDict = {}

    for daysAgo in range(daysPrior):
        currentDate = endDate - timedelta(days=daysAgo)

        daysResults = getQueryForSpecificDay(query, currentDate.year, currentDate.month, currentDate.day)

        sentimentScore = getAverageSentimentScore(daysResults)

        currentDayInformationDict = {
            'date' : str(currentDate),
            'sentiment' : str(sentimentScore),
            'url' : 'https://www.cnbc.com/2020/02/04/coronavirus-latest-updates.html'
        }

        dayQueryDict[str(currentDate)] = currentDayInformationDict

        #print(str(dayQueryDict))

    resultDictionary['results'] = dayQueryDict


    #print(resultDictionary)


    return resultDictionary


if __name__ == '__main__':
  print(getResults('coronavirus', date.today(), 3))
  #app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
