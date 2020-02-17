from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'EaganJones'
urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('<int:id>/<str:primarysymbol>/', views.company_detail, name='company_detail'),

    ]