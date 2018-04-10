from django.conf.urls import url
from django.urls import path, include
from .models import Cloud
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result$', views.result, name='result')
]
