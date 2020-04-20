
from django.core.management.base import BaseCommand
import pandas as pd
from django.db.models import Func

from brian.models import Sales2_Sales_Measures_by_Period




class Command(BaseCommand):
    help = "visualize data"

    # define logic of command
    def handle(self, *args, **options):
        df = pd.read_csv("C:/Users/prime/Downloads/walmart_data - Sayfa2.csv")




        print(df.head())
        for a, b, e, f, i, j in zip (df['Prime Item Nbr'], df['Prime Item Desc'], df['WM Week'],
                            df['WM Month'], df['POS Qty'], df['POS Sales']):


            Sales2_Sales_Measures_by_Period.objects.get_or_create(prime_item_nbr=a, prime_item_dec= b, wm_week = e, wm_month = f, pos_qty = i, pos_sales = j)


        #burdan asagisi silinebilir

        self.stdout.write('post complete')