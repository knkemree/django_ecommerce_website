# from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Orderpmp


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts-chartjs.html')

    ####################################################


## if you don't want to user rest_framework

# def get_data(request, *args, **kwargs): 
# 
# data ={ 
#             "sales" : 100, 
#             "person": 10000, 
#     } 
# 
# return JsonResponse(data) # http response 


####################################################### 

## using rest_framework classes 

class ChartData(APIView):
    #authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):


        lcd_list = []
        cases_list = []
        other_list = []
        date_list = []
        total_sale = []



        qs = Orderpmp.objects.values('order_date').filter(parent_cat = 'LCD').annotate(Sum('total_sale')) #.order_by('-quantity')
        qs1 = Orderpmp.objects.values('order_date').filter(parent_cat = 'Cases').annotate(Sum('total_sale'))
        qs2 = Orderpmp.objects.values('order_date').filter(parent_cat='nan').annotate(Sum('total_sale'))
        qs3 = Orderpmp.objects.values('order_date').annotate(Sum('total_sale'))
        qs4 = Orderpmp.objects.values('order_date').annotate(Sum('total_sale'))
        for lcd, cases, other, date, totals in zip(qs, qs1, qs2, qs3, qs4):
            lcd_list.append(lcd['total_sale__sum'])
            cases_list.append(cases['total_sale__sum'])
            other_list.append(other['total_sale__sum'])
            date_list.append(date['order_date'])
            total_sale.append(totals['total_sale__sum'])

        print(qs)
        labels = date_list
        chartLabel = "Monthly Sale"
        chartdata = [round(x) for x in total_sale]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }
        return Response(data) 