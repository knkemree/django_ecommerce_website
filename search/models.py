from django.db import models
from shop.models import Product

# Create your models here.
class City(models.Model):
    names = models.CharField(max_length=255)
    states = models.CharField(max_length=255)
    pros = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
      verbose_name_plural = "cities"

    def __str__(self):
        return self.names