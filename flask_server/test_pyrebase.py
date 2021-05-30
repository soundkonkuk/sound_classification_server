import pyrebase

config ={
    "apiKey": "AIzaSyAC2dAIfDflF7Qft4tZbqfTl30Ln6B12nI",
    "authDomain": "test-e4585.firebaseapp.com",
    "databaseURL": "https://test-e4585-default-rtdb.firebaseio.com",
    "projectId": "test-e4585",
    "storageBucket": "test-e4585.appspot.com",
    "messagingSenderId": "832943825026",
    "appId": "1:832943825026:web:54f8b9385006d36d39949b",
    "measurementId": "G-VHKBSKG1C4"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

path_on_cloud = "images/babycry10.wav"
path_local = "babycry10.wav"
storage.child(path_on_cloud).put(path_local)