from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('postmessage', views.postmessage),
    path('postcomment', views.postcomment),
    path('deletecomment', views.deletecomment),
    path('deletemessage', views.deletemessage)
]