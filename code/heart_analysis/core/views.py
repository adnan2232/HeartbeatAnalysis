from urllib import response
from django.http import HttpResponse
from django.shortcuts import render

from keras.models import load_model
import librosa
import numpy as np

# Create your views here.


def homepage(req):
    return render(req,"index.html")


def temp(req):
    # button = req.POST["textArea"]
    # inputFile = req.POST["inputFile"]

    # print(req.FILES)
    file = req.FILES["inputFile"]
    y, sr = librosa.load(file, sr=16000)
    print(y.shape)
    mfccs = np.mean(librosa.feature.mfcc(y,sr,n_mfcc=40).T,axis=0)
    print(mfccs.shape)
    mfccs.reshape((-1,1))
    print(mfccs.shape)
    mfccs = np.reshape(mfccs, (1,40,1))
    result = LSTM(mfccs)
    return render(req, "temporary.html",context={"shape":mfccs.shape,"result":result,"y":y})



def LSTM(mfcc):
    model = load_model(r"C:\Users\adnan\OneDrive\Desktop\HeartAnalysis\Data\model_checkpoints.hdf5")
    predictions = model.predict(mfcc)
    print(mfcc.shape)
    return predictions