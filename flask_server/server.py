from flask import Flask
import numpy as np
import os 
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import glob
import librosa
from keras.models import load_model
import tensorflow as tf
import json
import pyrebase


def predict_sound():
    model = tf.keras.models.load_model('model2.h5')
    def sound_feature(file_name):
        X, sample_rate = librosa.load(file_name)
        stft = np.abs(librosa.stft(X))
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
        mel = np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T,axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T,axis=0)
        return mfccs,chroma,mel,contrast,tonnetz
    
    features = np.zeros((41668, 193))

    def parse_sound(files): 
        index=0
        try:
            mfccs, chroma, mel, contrast, tonnetz = sound_feature(files)
            exfeatures = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
        except:
            print("error " + filename)
        else:
            features[index] = exfeatures
            index+=1
        return features
    
    def get_ans(ans):
        answer = {}
        answer['answer'] = ans
        message = ''

        #기능 1
        if(ans==1):
            message = "siren"
        # 기능 2
        if(ans==0):
            message = "dog"
        if(ans==2):
            message = "baby"
        else:
            message = "doorbell"
        answer['message'] = message
        return json.dumps(answer, ensure_ascii=False)

    def predict(filename):
        X = parse_sound(filename)
        X = X[0]
        X = X.reshape(1,193,1)
        y_pred = model.predict(X)
        y_pred = np.argmax(y_pred, axis=1)[0]
        result = get_ans(int(y_pred))
        print(result)
        return result
            
    
    config ={
        "apiKey" : "AIzaSyDZPPM4rCMlPnTf0ZNgaaMYisdrO9FFNq8",
        "authDomain": "test-a9dcc.firebaseapp.com",
        "databaseURL": "https://test-a9dcc-default-rtdb.firebaseio.com",
        "projectId": "test-a9dcc",
        "storageBucket": "test-a9dcc.appspot.com",
        "messagingSenderId": "1066850164582",
        "appId": "1:1066850164582:web:c7efd9b188d5ecfc5ab2a7",
        "measurementId": "G-Q2RRZBDD3N"
    }

    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    path_on_cloud = "sounds/2021-05-09T06_46_58.655.wav"
    path_local = "sound.wav"
    storage.child(path_on_cloud).download(path_local)
    result = predict(path_local)

    return result
            

        

app = Flask(__name__)

@app.route("/predict")
def test():
    return predict_sound()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port = "5000")