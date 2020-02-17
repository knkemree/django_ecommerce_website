from django.urls import path
from . import views
app_name = 'EaganJones'
urlpatterns = [
    path('companies/',views.CompaniesListView.as_view(), name='com_list'),
    path('companies/<pk>/',views.CompaniesDetailView.as_view(),name='com_detail'),
]