from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from home.models import Comment
from .models import Category, Product, ProductImage
from cart.forms import CartAddProductForm
from django.views.generic import ListView
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
    context = {'commnets': comments,
               'product': product,
              'gallery': gallery,
              'cart_product_form': cart_product_form,
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


