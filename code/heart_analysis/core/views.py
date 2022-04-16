
from django.shortcuts import render
import io
from keras.models import load_model
import librosa
import numpy as np
import os
from heart_analysis.settings import BASE_DIR
# Create your views here.


def homepage(req):
    return render(req,"index.html")


def temp(req):
    # button = req.POST["textArea"]
    # inputFile = req.POST["inputFile"]

    # print(req.FILES)
    file = io.BytesIO(req.FILES["inputFile"].read())
    print(file)
    y, sr = librosa.load(file, sr=16000)
    mfccs = np.mean(librosa.feature.mfcc(y,sr=sr,n_mfcc=40).T,axis=0)
    # print(mfccs.shape)
    # print(mfccs.shape)
    mfccs = np.reshape(mfccs, (1,40,1))
    val, idx = LSTM(mfccs)
    # print(type(result))
    return render(req, "temporary.html",context={"category": idx, "value": val})



def LSTM(mfcc):
    model = load_model(os.path.join(BASE_DIR,"model_checkpoints.hdf5"))
    #model = load_model(r"D:\Python Projects\HeartBeatAnalysis\LSTM\model_checkpoints.hdf5")
    predictions = model.predict(mfcc)
    category = {
        0: "EXTRASTOLE/EXTRAHLS",
        1: "MURMUR",
        2: "NORMAL"
    }
    print(predictions)
    idx, val = -1, 0
    for pred in range(len(predictions[0])):
        if predictions[0][pred]*100 > val*100:
            val, idx = predictions[0][pred], category[pred]

    return val*100, idx