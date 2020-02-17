from django.shortcuts import render
from django.views.generic import ListView
from shop.models import Product
from django.db.models import Q
from search.models import City

# Create your views here.
class SearchProductView(ListView):
    model = City
    template_name = "search_results.html"

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = City.objects.filter(
            Q(names__icontains=query) | Q(states__icontains=query)
        )
        return object_list