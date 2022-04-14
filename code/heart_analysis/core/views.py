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
    mfcc = np.mean(librosa.feature.mfcc(y, sr, n_mfcc=40).T, axis=0)
    print(mfcc.shape)
    res = LSTM(mfcc)
    print(res)
    context = {
        "res" : res
    }
    return render(req, "temporary.html",context=context)

    # return render(req,"temporary.html",context = {"variable": 25})

def LSTM(mfcc):
    path = 'D:\Python Projects\HeartBeatAnalysis\LSTM\model_checkpoints.hdf5'
    model = load_model(path)
    predictions = model.predict(mfcc)
    return predictions