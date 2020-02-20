# this file contains a single unit test for my_function located in server/src/example.py
from datetime import date
import json
import src.watson_query_utilities as watson_utils
from unittest.mock import MagicMock

sample_query_result = {}
with open('test_watson_query_utilities_sample_query_result') as json_file:
    sample_query_result = json.load(json_file)



def test_get_average_sentiment_score_has_results():
    average_sentiment_score = watson_utils.get_average_sentiment_score(sample_query_result)

    assert average_sentiment_score == -0.553604


def test_get_average_sentiment_score_does_not_have_results():
    old_results = sample_query_result['results']

    sample_query_result['results'] = []

    average_sentiment_score = watson_utils.get_average_sentiment_score(sample_query_result)

    sample_query_result['results'] = old_results

    assert average_sentiment_score == None


def test_get_closest_result_has_result():
    closest_result = watson_utils.get_closest_result(sample_query_result, 0.0)

    assert closest_result == sample_query_result['results'][0]


def test_get_closest_result_has_no_result():
    old_results = sample_query_result['results']

    sample_query_result['results'] = []

    closest_result = watson_utils.get_closest_result(sample_query_result, 0.0)

    sample_query_result['results'] = old_results

    assert closest_result == None


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
