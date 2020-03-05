from flask import Flask, render_template, make_response
import os
import time
from datetime import date
from watson_query_utilities import Hive

hive = Hive(sources=['reddit', 'cnbc'])
app = Flask(__name__)

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

@app.route('/search/<query>')
def search(query):
    return hive.get_results(query, date.today(), 7)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
