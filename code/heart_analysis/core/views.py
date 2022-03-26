from urllib import response
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def homepage(req):
    return render(req,"index.html")