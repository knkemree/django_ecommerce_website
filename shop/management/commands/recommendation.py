import rec as rec
from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import plotly.offline as py
import plotly.graph_objects as go
from django.db.models import Sum
import slug

import http.client
import json

from shop.models import Rec, Product, Category


class Command(BaseCommand):
    help = "collect ft articles"

    # define logic of command
    def handle(self, *args, **options):
        conn = http.client.HTTPSConnection("www.primemobileparts.com")


        payload = ""

        headers = {'authorization': "Bearer XgXLQTAvcOwn4Q4LycjR0W1hViX5ChenEepGTcyPo37C3TBCy6ubDxu1FiHt"}

        conn.request("GET", "/api/user-order-report",payload, headers)

        res = conn.getresponse()
        data = res.read()

        data.decode("utf-8")
        x = json.loads(data.decode("utf-8"))

        df = pd.DataFrame(x['reportData'])

        df = df.dropna(subset=['user_id', 'product_id', 'quantity'])
        customer_item_matrix = df.pivot_table(
            index='user_id',
            columns='product_id',
            values='quantity',
            aggfunc='sum'
        )
        print(df.head())


        customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0)
        user_user_sim_matrix = pd.DataFrame(
            cosine_similarity(customer_item_matrix)
        )
        user_user_sim_matrix.columns = customer_item_matrix.index
        user_user_sim_matrix['user_id'] = customer_item_matrix.index
        user_user_sim_matrix = user_user_sim_matrix.set_index('user_id')
        # user_user_sim_matrix.loc[737.0].sort_values(ascending=False)  # Angelaya benzer kullaniclar
        #items_bought_by_A = set(customer_item_matrix.loc[737.0].iloc[customer_item_matrix.loc[737.0].nonzero()].index)
        #items_bought_by_B = set(customer_item_matrix.loc[685.0].iloc[customer_item_matrix.loc[685.0].nonzero()].index)
        #items_to_recommend_to_B = items_bought_by_A - items_bought_by_B
        #items_to_recommend_to_B
        item_item_sim_matrix = pd.DataFrame(
            cosine_similarity(customer_item_matrix.T)
        )
        item_item_sim_matrix.columns = customer_item_matrix.T.index

        item_item_sim_matrix['product_id'] = customer_item_matrix.T.index
        item_item_sim_matrix = item_item_sim_matrix.set_index('product_id')




        for y in df['product_id']:
            #Category.objects.get_or_create(name=z, slug = z.lower().replace(' ', '-'))
            #f = Category.objects.get(name = z)

            #Product.objects.get_or_create(name=y, price = p, category_id = f.id, slug=y.lower().replace(' ', '-'))
            dict = {}
            dict["products"] = {}


            top_10_similar_items = list(
                    item_item_sim_matrix \
                        .loc[y] \
                        .sort_values(ascending=False) \
                        .iloc[1:13] \
                        .index
                )
            dict["products"][y] = [i for i in top_10_similar_items]
                #print(y)
                #print(top_10_similar_items)
            #print(dict)
            rec = json.dumps(dict)
            #recs = json.loads(rec)

            print(rec)
            conn = http.client.HTTPSConnection("www.primemobileparts.com")



            headers = {
                'content-type': "application/json",
                'authorization': "Bearer XgXLQTAvcOwn4Q4LycjR0W1hViX5ChenEepGTcyPo37C3TBCy6ubDxu1FiHt"
            }

            conn.request("POST", "/api/product-related", rec, headers)

            res = conn.getresponse()
            data = res.read()

            #print(data.decode("utf-8"))



                #Product.objects.get_or_create(name=y)





            #print('%s added' % (top_10_similar_items,))

                #Rec.product.add(d)

        self.stdout.write('post complete')