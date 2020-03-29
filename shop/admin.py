from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from shop.models import Category, Product, ProductImage, Rec


# Register your models here.
class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'category', 'cost', 'price', 'stock', 'available', 'updated', ]
    list_filter = ['category', 'available', 'updated']
    list_editable = ['cost', 'price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'sku', 'barcode')
    list_display_links = ['image_tag','name',]
    inlines = [ImageInline]

class ModelClass:
    ## content = models.TextField()
    description = RichTextUploadingField()


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())



class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product','image','create_at')

admin.site.register(Rec)


