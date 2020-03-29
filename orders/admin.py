import csv
import datetime

from django.contrib import admin
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem, CustomerAddress, Orderpmp


# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_display = ['product', 'price', 'quantity', 'cart_total']
    raw_id_fields = ['product']

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;'\
        'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many\
              and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email','address', 'postal_code', 'city', 'paid','created', 'cart_total']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]



class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ['line_1', 'line_2', 'line_3', 'city', 'postalcode', 'state']
    list_filter = ['city', 'postalcode']
    search_fields = ['line1']

admin.site.register(CustomerAddress, CustomerAddressAdmin)

class OrderpmpAdmin(admin.ModelAdmin):
    list_display = ('useri','orderi','product_name', 'quantity', 'price_wholesale', 'category_name', 'order_date')
admin.site.register(Orderpmp, OrderpmpAdmin)