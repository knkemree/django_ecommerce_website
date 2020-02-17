from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput

from shop.models import Product


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length = 50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    read = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-create_at',)

    class Meta:
        verbose_name = "Contact Form Message"
        verbose_name_plural = "Contact Form Messages"

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = {'name', 'email', 'subject', 'message'}
        widgets = {
            'name': TextInput(attrs={'class': 'input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'}),
            'message': TextInput(attrs={'class': 'input', 'placeholder': 'Your  Message'})}

class Comment(models.Model):
    STATUS = (
        (1, 'True'),
        (2, 'False')
    )
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=255)
    status = models.IntegerField(choices=STATUS, default=0)
    rating = models.IntegerField(choices=RATING, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = {'subject', 'message', 'rating'}
        widgets = {
            'subject': TextInput(attrs={'class': 'input', 'placeholder': 'Subject'}),
            'message': TextInput(attrs={'class': 'input', 'placeholder': 'Your Review'}),
            'rating': TextInput(attrs={'class': 'input',})
            }

