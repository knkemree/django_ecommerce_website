import rec as rec
from django.core.management.base import BaseCommand
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
import slug
from django.db.models import Sum, IntegerField
import http.client
import json
import plotly.graph_objects as go
from faker import Faker
import plotly.express as px
import datetime
from django.db.models import Func
from orders.models import Orderpmp

import random
import time


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'


class Command(BaseCommand):
    help = "visualize data"

    # define logic of command
    def handle(self, *args, **options):
        conn = http.client.HTTPSConnection("www.primemobileparts.com")

        payload = {
            "beginRange": "2019-09-01 00:00:00",
            "endRange": "2020-03-29 00:00:00" #str(datetime.datetime.now())
        }
        veri = json.dumps(payload)

        headers = {
            'content-type': "application/json",
            'authorization': "Bearer XgXLQTAvcOwn4Q4LycjR0W1hViX5ChenEepGTcyPo37C3TBCy6ubDxu1FiHt"
        }

        conn.request("GET", "/api/user-order-report", veri, headers)

        res = conn.getresponse()
        data = res.read()

        data.decode("utf-8")
        x = json.loads(data.decode("utf-8"))

        df = pd.DataFrame(x['reportData'])
        df['order_date'] = pd.to_datetime(df['order_date']).dt.date

        list3 = []
        for i in df['order_date']:
            list3.append(i.strftime("%Y-%m"))
        df['order_date_y_m'] = list3


        df = df.dropna()
        list2 = []
        for index, row in df.iterrows():
            prod_amount = float(df['price_wholesale'][index]) * float(df['quantity'][index])
            # prod_amount += prod_amount
            list2.append(prod_amount)
        df['total'] = list2

        df.loc[df['product_name'].str.contains('Case') |
               df['product_name'].str.contains('Band') |
               df['category_names'].str.contains('Cover')
        , 'parent_cat'] = 'Cases'

        df.loc[df['product_name'].str.contains('Assembly') |
               df['product_name'].str.contains('Digitizer') |
               df['product_name'].str.contains('Housing') |
               df['product_name'].str.contains('Glass') |
               df['category_names'].str.contains('Batteries')
        , 'parent_cat'] = 'LCD'


        print(df.head())
        for a, b, c, d, e, f, g, h, i, j, k in zip (df['user_id'], df['order_id'], df['product_id'], df['product_name'], df['quantity'], df['price_wholesale'],
                            df['category_ids'], df['category_names'], df['order_date'], df['total'], df['parent_cat']):


            Orderpmp.objects.get_or_create(useri=a, orderi= b, producti = c, product_name = d, quantity = e, price_wholesale = f, categotyi = g,
                                           category_name = h, order_date = i, total_sale = j,parent_cat=k  )


        #burdan asagisi silinebilir
        lcd_list = []
        cases_list = []
        other_list = []
        date_list = []
        totals = []



        qs = Orderpmp.objects.values('order_date').filter(parent_cat = 'LCD').annotate(Sum('total_sale')) #.order_by('-quantity')
        qs1 = Orderpmp.objects.values('order_date').filter(parent_cat = 'Cases').annotate(Sum('total_sale'))
        qs2 = Orderpmp.objects.values('order_date').filter(parent_cat='nan').annotate(Sum('total_sale'))
        qs3 = Orderpmp.objects.values('order_date').annotate(Sum('total_sale'))
        #qs4 = Orderpmp.objects.values('order_date').annotate(Sum('total_sale'))
        for lcd, cases, other, date in zip(qs, qs1, qs2, qs3):
            lcd_list.append(lcd['total_sale__sum'])
            cases_list.append(cases['total_sale__sum'])
            other_list.append(other['total_sale__sum'])
            date_list.append(date['order_date'])
            totals.append(date['total_sale__sum'])
        print(qs)

        #fig = go.Figure(data=[
            #go.Bar(name='LCD', x=date_list, y=[round(x) for x in lcd_list], text=[round(x) for x in lcd_list], textposition='auto',),
            #go.Bar(name='Case', x=date_list, y=[round(x) for x in cases_list], text=[round(x) for x in cases_list], textposition='auto'),
            #go.Bar(name='Other', x=date_list, y=[round(x) for x in other_list], text=[round(x) for x in other_list], textposition='auto'),
        #])

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=totals,x=date_list, mode = 'lines+markers',name="sales_by_category",line_color='deepskyblue',connectgaps=True))


        fig.update_layout(barmode='stack',
                          title_text='Time Series with Rangeslider',
                          xaxis_rangeslider_visible=True,
                          yaxis=dict(range=[0, 3000]),

                          xaxis=dict(
                              rangeselector=dict(
                                  buttons=list([
                                      dict(count=1,
                                           label="1m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=6,
                                           label="6m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=1,
                                           label="YTD",
                                           step="year",
                                           stepmode="todate"),
                                      dict(count=1,
                                           label="1y",
                                           step="year",
                                           stepmode="backward"),
                                      dict(step="all")
                                  ])
                              )
                          ))

        fig.show()
        #print(Orderpmp.objects.aggregate(Sum('quantity')))
        #print(Orderpmp.objects.values('useri').annotate(Sum('quantity')))
        #print(Orderpmp.objects.values('product_name').annotate(per_pro_sale=Sum('quantity')).order_by('-per_pro_sale'))
        #print(Orderpmp.objects.values('order_date').annotate(daily_sale=Sum('quantity')).order_by('-daily_sale'))
        self.stdout.write('post complete')