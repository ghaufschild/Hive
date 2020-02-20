import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

#cred = credentials.Certificate("../../hive-5914-firebase-adminsdk-w772z-3f52e39450.json")
app = firebase_admin.initialize_app()

def write_to_firebase(collection, key, value):
    store = firestore.client()
    doc_ref = store.collection(collection)
    doc_ref.add({key:value})


#write_to_firebase('trending', 'name', 'coronavirus')
    
