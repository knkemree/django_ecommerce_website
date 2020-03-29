from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from home.models import Comment
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.views.generic import ListView, TemplateView
import plotly.offline as py
import plotly.graph_objects as go
from django.db.models import Sum
import datetime
import numpy as np
# Create your views here.



def product_list(request, category_slug=None, ):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        categories = Category.objects.all()
        products = products.filter(category=category)

    return render(request,
        'products.html',
        {'category': category,
        'categories': categories,
        'products': products,
         'cart_product_form':cart_product_form,
         })

def product_detail(request, id, slug, ):
    comments = Comment.objects.filter(status=1).order_by('-id')
    product = get_object_or_404(Product,
            id=id,
            slug=slug,
            available=True)

    cart_product_form = CartAddProductForm()
    gallery = ProductImage.objects.filter(product_id=id)


    date = []
    data = []
    #x_data = Orderpmp.objects.values_list('order_date', flat=True)

    #qs = Orderpmp.objects.values('order_date').annotate(daily_sale=Sum('quantity')).order_by('-order_date')
    #for entry in qs:
     #   data.append(entry['daily_sale'])
    #    date.append(entry['order_date'])

    #fig = go.Figure()
    #fig.add_trace(go.Scatter(x=date, y=data,  name="daily sale",line_color='deepskyblue'))

    #fig.update_layout(title_text='Time Series with Rangeslider',xaxis_rangeslider_visible=True, yaxis=dict(range=[0, 400]))
    fig = go.Figure(
        data=[go.Bar(y=[2, 1, 3])],
        layout_title_text="A Figure Displayed with fig.show()"
    )
    plot_div = py.plot(fig, include_plotlyjs=False, output_type='div')


    context = {'commnets': comments,
               'product': product,
              'gallery': gallery,
              'cart_product_form': cart_product_form,
               'plot_div': plot_div
               }
    return render(request, 'product_detail.html', context)

class SearchsProductView(ListView):
    model = Product
    template_name = "search_result.html"

    def get_queryset(self): # new
        query = self.request.GET.get('q', None)

        object_list = Product.objects.filter(Q(name__icontains=query) |
                                             Q(description__icontains=query) |
                                             Q(barcode__icontains=query) |
                                             Q(sku__icontains=query)
                                             ).exclude(available=False)
        if query is not None:
            return object_list.distinct()
        return object_list.available()

def addtocartform(request):
    cart_product_form = CartAddProductForm()
    pros = Product.objects.filter(available=True)
    context = {
               'cart_product_form': cart_product_form,
                'pros': pros
               }
    return render(request, 'addtocartform.html', context)



