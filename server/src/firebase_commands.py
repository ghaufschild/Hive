import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import datetime

#cred = credentials.Certificate("../../hive-5914-firebase-adminsdk-w772z-3f52e39450.json")
app = firebase_admin.initialize_app()
store = firestore.client()

def write_to_firebase(collection, key, value):
    doc_ref = store.collection(collection)
    doc_ref.add({key:value})

def get_all_documents_within_time_frame(collection, time_range = 0):
    if time_range > 0:
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)
        yesterday = today - one_day
        time_now = datetime.datetime.now().time()
        compare_time = datetime.datetime.combine(yesterday, time_now)
        
        docs = store.collection(collection).where("time", ">", compare_time).stream()
        #for doc in docs:
        #    print('{} => {}'.format(doc.id, doc.to_dict()))
        return docs
    else:
        return store.collection(collection).stream()
        
#get_all_documents_within_time_frame("queries", 24)

#write_to_firebase('trending', 'name', 'coronavirus')
    
