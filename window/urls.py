from django.contrib import admin
from django.urls import path
from window import views

urlpatterns = [
    path('', views.base),
]