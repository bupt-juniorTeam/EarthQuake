from django.contrib import admin
from django.urls import path
from window import views

urlpatterns = [
    path('', views.base),
    path('lists/', views.lists),
    path('report/', views.report),
    path('report/earthquake', views.report_earthquake),
    path('report/affection', views.report_affection),
    path('data', views.return_data_json)
]
