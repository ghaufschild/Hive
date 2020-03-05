# this file contains a single unit test for my_function located in server/src/example.py
from datetime import date, timedelta
import src.watson_query_utilities as watson_utils
from unittest.mock import MagicMock

#sample_query_result = {'matching_results': 1, 'session_token': '1_dJGtXtLdLM59Z1f5_aQq7dMCbL', 'results': [{'id': 'ce6af094-5a4e-4301-a839-af905208cea6', 'result_metadata': {'confidence': 0.2084252734491108, 'score': 2.050411}, 'body': 'Sample Body', 'enriched_body': {'sentiment': {'document': {'score': -0.553604, 'label': 'negative'}}, 'emotion': {'document': {'emotion': {'disgust': 0.177818, 'joy': 0.565515, 'anger': 0.163678, 'fear': 0.16522, 'sadness': 0.551874}}}, 'concepts': [{'text': 'China', 'relevance': 0.945563, 'dbpedia_resource': 'http://dbpedia.org/resource/China'}, {'text': 'Princess Cruises', 'relevance': 0.878117, 'dbpedia_resource': 'http://dbpedia.org/resource/Princess_Cruises'}, {'text': 'Pacific', 'relevance': 0.866934, 'dbpedia_resource': 'http://dbpedia.org/resource/Pacific_(ship)'}], 'categories': [{'score': 0.958654, 'label': '/health and fitness/disease/epidemic'}, {'score': 0.91211, 'label': '/health and fitness/disease/cold and flu'}], 'keywords': [{'text': 'high relevance', 'relevance': 0.640152, 'count': 2}, {'text': 'low relevance', 'relevance': 0.585948, 'count': 1}]}, 'enriched_title': {'sentiment': {'document': {'score': -0.985702, 'label': 'negative'}}, 'emotion': {'document': {'emotion': {'disgust': 0.211562, 'joy': 0.008572, 'anger': 0.533021, 'fear': 0.258056, 'sadness': 0.362595}}}, 'concepts': [{'text': "Plain White T's", 'relevance': 0.841454, 'dbpedia_resource': "http://dbpedia.org/resource/Plain_White_T's"}, {'text': 'Management', 'relevance': 0.763351, 'dbpedia_resource': 'http://dbpedia.org/resource/Management'}], 'categories': [{'score': 0.987497, 'label': '/health and fitness/disease/epidemic'}], 'keywords': [{'text': 'director calls', 'relevance': 0.998073, 'count': 1}, {'text': 'global leaders', 'relevance': 0.992061, 'count': 1}, {'text': 'stigma', 'relevance': 0.613711, 'count': 1}, {'text': 'coronavirus epidemic', 'relevance': 0.19001, 'count': 1}, {'text': 'hate', 'relevance': 0.042738, 'count': 1}]}, 'url': 'https://www.cnbc.com/2020/02/15/article.html', 'year': 2020, 'extracted_metadata': {'sha1': '68d1cee94fb4b9523f93c99ececa8da3bf081b3b', 'filename': 'extracted-metadat-filename', 'file_type': 'json'}, 'title': 'Sample Title', 'day': 15, 'month': 2}], 'retrieval_details': {'document_retrieval_strategy': 'untrained'}}
sample_query_result = [
 		{'id': 'ce6af094-5a4e-4301-a839-af905208cea6', 'result_metadata': {'confidence': 0.2084252734491108, 'score': 2.050411}, 'body': 'Sample Body', 'enriched_body': {'sentiment': {'document': {'score': -0.553604, 'label': 'negative'}}, 'emotion': {'document': {'emotion': {'disgust': 0.177818, 'joy': 0.565515, 'anger': 0.163678, 'fear': 0.16522, 'sadness': 0.551874}}}, 'concepts': [{'text': 'China', 'relevance': 0.945563, 'dbpedia_resource': 'http://dbpedia.org/resource/China'}, {'text': 'Princess Cruises', 'relevance': 0.878117, 'dbpedia_resource': 'http://dbpedia.org/resource/Princess_Cruises'}, {'text': 'Pacific', 'relevance': 0.866934, 'dbpedia_resource': 'http://dbpedia.org/resource/Pacific_(ship)'}], 'categories': [{'score': 0.958654, 'label': '/health and fitness/disease/epidemic'}, {'score': 0.91211, 'label': '/health and fitness/disease/cold and flu'}], 'keywords': [{'text': 'high relevance', 'relevance': 0.640152, 'count': 2}, {'text': 'low relevance', 'relevance': 0.585948, 'count': 1}]}, 'enriched_title': {'sentiment': {'document': {'score': -0.985702, 'label': 'negative'}}, 'emotion': {'document': {'emotion': {'disgust': 0.211562, 'joy': 0.008572, 'anger': 0.533021, 'fear': 0.258056, 'sadness': 0.362595}}}, 'concepts': [{'text': "Plain White T's", 'relevance': 0.841454, 'dbpedia_resource': "http://dbpedia.org/resource/Plain_White_T's"}, {'text': 'Management', 'relevance': 0.763351, 'dbpedia_resource': 'http://dbpedia.org/resource/Management'}], 'categories': [{'score': 0.987497, 'label': '/health and fitness/disease/epidemic'}], 'keywords': [{'text': 'director calls', 'relevance': 0.998073, 'count': 1}, {'text': 'global leaders', 'relevance': 0.992061, 'count': 1}, {'text': 'stigma', 'relevance': 0.613711, 'count': 1}, {'text': 'coronavirus epidemic', 'relevance': 0.19001, 'count': 1}, {'text': 'hate', 'relevance': 0.042738, 'count': 1}]}, 'url': 'https://www.cnbc.com/2020/02/15/article.html', 'year': 2020, 'extracted_metadata': {'sha1': '68d1cee94fb4b9523f93c99ececa8da3bf081b3b', 'filename': 'extracted-metadat-filename', 'file_type': 'json'}, 'title': 'Sample Title', 'day': 15, 'month': 2}]
TEST_SOURCES = ['reddit', 'cnbc']

def test_get_average_sentiment_score_has_results():
    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=sample_query_result)

    average_sentiment_score = watson_query_object.get_average_sentiment_score(sample_query_result)

    assert average_sentiment_score == -0.553604


def test_get_average_sentiment_score_does_not_have_results():
    #old_results = sample_query_result

    #sample_query_result = []

    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=[])

    average_sentiment_score = watson_query_object.get_average_sentiment_score([])

    #sample_query_result = old_results

    assert average_sentiment_score == None


def test_get_closest_result_has_result():
    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=sample_query_result)

    closest_result = watson_query_object.get_closest_result(sample_query_result, 0.0)

    assert closest_result == sample_query_result[0]


def test_get_closest_result_has_no_result():
    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=[])

    closest_result = watson_query_object.get_closest_result([], 0.0)

    assert closest_result == None


def test_get_results_one_day():
    test_query = "Query"
    today = date.today()
    test_days_prior = 1

    days_prior = 0
    test_date = today - timedelta(days=(days_prior - 1))

    while test_date.day != 20 or test_date.month != 2 or test_date.year != 2020:
        test_date = today - timedelta(days=(days_prior - 1))
        days_prior += 1

    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=sample_query_result)

    results = watson_query_object.get_results(test_query, test_date, test_days_prior)


    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': test_days_prior, 'results': [{'month': '2', 'day': '20', 'year': '2020', 'y': -0.553604, 'url': 'https://www.cnbc.com/2020/02/15/article.html', 'title': 'Sample Title'}]}


def test_get_results_zero_days():
    test_query = "Query"
    test_date = date.today()
    test_days_prior = 0

    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=sample_query_result)

    results = watson_query_object.get_results(test_query, test_date, test_days_prior)

    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': test_days_prior, 'results': []}


def test_get_results_negative_days():
    test_query = "Query"
    test_date = date.today()
    test_days_prior = -1

    watson_query_object = watson_utils.Hive(TEST_SOURCES)
    watson_query_object.datapool.get_query_for_specific_day = MagicMock(return_value=sample_query_result)

    results = watson_query_object.get_results(test_query, test_date, test_days_prior)

    assert results == {'query_string': test_query, 'ending_date': str(test_date), 'days_prior': test_days_prior, 'results': []}
