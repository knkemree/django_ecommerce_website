from django.urls import path
from . import views
from .views import (
    SearchsProductView
)


app_name = 'shop'

urlpatterns = [
    #path('', views.index, name='index'),

    path('', views.product_list, name='product_list'),

    path('shop/', views.product_list, name='product_list'),
    path('addtocartform/', views.addtocartform, name='addtocartform'),
    path('search/', SearchsProductView.as_view(), name='query'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),


    ]