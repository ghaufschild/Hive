# this file contains a single unit test for my_function located in server/src/example.py
from datetime import date
import json
import src.watson_query_utilities as watson_utils
from unittest.mock import MagicMock

sample_query_result = {}
with open('test_watson_query_utilities_sample_query_result') as json_file:
    sample_query_result = json.load(json_file)

def test_get_results_one_day():
    test_query = "Query"
    test_date = date.today()
    test_days_prior = 1

    watson_utils.get_query_for_specific_day = MagicMock(return_value=sample_query_result)
    results = watson_utils.get_results(test_query, test_date, test_days_prior)


    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': test_days_prior, 'results': [{'month': '2', 'day': '20', 'year': '2020', 'y': -0.553604, 'url': 'https://www.cnbc.com/2020/02/15/article.html', 'title': 'Sample Title'}]}

def test_get_results_zero_days():
    test_query = "Query"
    test_date = date.today()
    test_days_prior = 0

    watson_utils.get_query_for_specific_day = MagicMock(return_value=sample_query_result)
    results = watson_utils.get_results(test_query, test_date, test_days_prior)

    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': test_days_prior, 'results': []}

def test_get_results_negative_days():
    test_query = "Query"
    test_date = date.today()
    test_days_prior = -1

    watson_utils.get_query_for_specific_day = MagicMock(return_value=sample_query_result)
    results = watson_utils.get_results(test_query, test_date, test_days_prior)

    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': 0, 'results': []}
