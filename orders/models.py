from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db import models
from localflavor.us.forms import USStateField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                    MaxValueValidator
from coupons.models import Coupon

from shop.models import Product
# Create your models here.

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True ,null=True)  # validators should be a list
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    note=models.TextField(null=True, default="")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])


    def __str__(self):
        return 'Order {}'.format(self.id)

    def cart_total(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())

        return total_cost - total_cost * \
               (self.discount / Decimal('100'))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def cart_total(self):
        return sum(item.get_cost() for item in self.items.all())

class CustomerAddress(models.Model):
    line_1 = models.CharField(max_length=300)
    line_2 = models.CharField(max_length=300)
    line_3 = models.CharField(max_length=300)
    city = models.CharField(max_length=150)
    postalcode = models.CharField(max_length=10)
    state = USStateField(blank=True)
    country = models.CharField(max_length=150)



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True)



