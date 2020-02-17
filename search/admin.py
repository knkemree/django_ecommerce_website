from django.contrib import admin
from .models import City

# Register your models here.
class CityAdmin(admin.ModelAdmin):
    list_display = ("names", "states", "pros")

admin.site.register(City, CityAdmin)