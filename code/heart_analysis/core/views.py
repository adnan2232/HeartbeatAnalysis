import warnings
from django.shortcuts import render
import io
from keras.models import load_model
import librosa
import numpy as np
import os
from heart_analysis.settings import BASE_DIR
# Create your views here.


def LSTM(y,sr):
    input_length = sr*12
    if(round(librosa.get_duration(y,sr))<12):
        y = librosa.util.fix_length(y,input_length)
    mfccs = np.mean(librosa.feature.mfcc(y,sr=sr,n_mfcc=13).T,axis=0)
    mfccs = np.reshape(mfccs, (1,13,1))
    model = load_model(os.path.join(BASE_DIR,"model_checkpoints_2.hdf5"))
    #model = load_model(r"D:\Python Projects\HeartBeatAnalysis\LSTM\model_checkpoints.hdf5")
    predictions = model.predict(mfccs)
    category = {
        0: "EXTRAHLS",
        1: "MURMUR",
        2: "NORMAL/Extrasystolic"
    }
    idx, val = -1, 0
    for pred in range(len(predictions[0])):
        if predictions[0][pred]*100 > val*100:
            val, idx = predictions[0][pred], category[pred]

    return val*100, idx

def homepage(req):
    return render(req,"index.html")


def temp(req):
    # button = req.POST["textArea"]
    # inputFile = req.POST["inputFile"]

    # print(req.FILES)
    file = io.BytesIO(req.FILES["inputFile"].read())
    y, sr = librosa.load(file, sr=22050)
    
    # print(mfccs.shape)
    # print(mfccs.shape)
    
    val, idx = LSTM(y,sr)
    
    
    lstm = {
        "category":idx,
        "value":val
    }
    

    # print(type(result))
    return render(req, "temporary.html",context={"lstm": lstm})


