import firebase_admin
import google.cloud
import datetime
from collections import defaultdict, Counter
from firebase_admin import credentials, firestore
from operator import itemgetter

#cred = credentials.Certificate("../../hive-5914-firebase-adminsdk-w772z-3f52e39450.json")
app = firebase_admin.initialize_app()
store = firestore.client()

def write_to_firebase(collection, key, value):
    doc_ref = store.collection(collection)
    doc_ref.add({key:value})

def write_query_to_firebase(query):
    doc_ref = store.collection('queries')
    doc_ref.add({'query':query, 'time':datetime.datetime.now()})

def get_all_documents_within_time_frame(collection, days_ago = 0):
    if days_ago > 0:
        today = datetime.date.today()
        one_day = datetime.timedelta(days = days_ago)
        yesterday = today - one_day
        time_now = datetime.datetime.now().time()
        compare_time = datetime.datetime.combine(yesterday, time_now)
        
        docs = store.collection(collection).where("time", ">", compare_time).stream()
        #for doc in docs:
        #    print('{} => {}'.format(doc.id, doc.to_dict()))
        return docs
    else:
        return store.collection(collection).stream()
        
def get_trending(days = 1):
    
    queries = get_all_documents_within_time_frame('queries', days)
    
    counts = defaultdict(int)

    for q in queries:
        q = q.to_dict()

        counts[q['query']] += 1

    trending = sorted(counts, key=counts.get, reverse=True)

    return trending[:10]