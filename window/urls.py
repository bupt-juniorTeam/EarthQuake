from django.contrib import admin
from django.urls import path
from window import views

urlpatterns = [
    path('', views.base),
    path('map/',views.return_location),
    path('lists/', views.lists),
    path('lists/sublists', views.sublists),
    path('report/', views.report),
    path('report/earthquake', views.report_earthquake),
    path('report/affection', views.report_affection),
    path('data', views.return_data_json),
    path('graph/',views.graph_vision),
]
