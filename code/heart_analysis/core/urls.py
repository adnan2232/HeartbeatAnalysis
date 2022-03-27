from django.urls import path
from .views import homepage, temp


urlpatterns = [
    path("",homepage, name ="homepage"),
    path("temporary",temp,name="temp")
]