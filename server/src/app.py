from flask import Flask, render_template, make_response, request
import os
import time
from datetime import date, timedelta
import firebase_commands
from watson_query_utilities import Hive
from requests import get
from apscheduler.schedulers.background import BackgroundScheduler
import scrape_cnbc as scraper

hive = Hive(sources=['reddit', 'cnbc'])
app = Flask(__name__)

def update_watson_database():
    today = date.today()
    yesterday = today - timedelta(days=1)
    scraper.scrape_cnbc(yesterday)

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_watson_database, trigger="interval", hours=24)

scheduler.start()

def format_server_time():
    server_time = time.localtime()
    return time.strftime("%I:%M:%S %p", server_time)

@app.route('/')
def index():
    context = { 'server_time': format_server_time() }
    template = render_template('index.html', context=context)
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'

    return response

@app.route("/about")
def about():
    context = { 'server_time': format_server_time() }
    template = render_template('about.html', context=context)
    response = make_response(template)
    response.headers['Cache-Control'] = 'public, max-age=300, s-maxage=600'

    return response


#from scrape_cnbc import scrape_cnbc
#@app.route('/uploaddocuments/<day>'):
#def uploaddocuments(day):
#    scrape_cnbc(date.strptime(day, '%Y-%m-%d'))
@app.route('/testing')
def testing():
    queries = firebase_commands.get_trending()

    trending = []

    for q in queries:
        results = hive.get_results(q, date.today(), 7)
        trending.append(results)

    return {'results': trending}

@app.route('/search')
def search():
    query = request.args.get('query')
    firebase_commands.write_query_to_firebase(query)
    articles_per_day = int(request.args.get('articles'))
    return hive.get_results(query, date.today(), 7, articles_per_day)

@app.route('/trending')
def trending():

    results = firebase_commands.get_all_documents_within_time_frame('trending')
    trending = []

    for r in results:
        trending.append(r.to_dict())

    print(trending)

    return {'results': trending}

if __name__ == '__main__':
    #with app.test_client() as c:
    #    response = c.get('/search?query=coronavirus&articles=1')
    #    print(response)
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
