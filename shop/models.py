from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,
        db_index=True)
    slug = models.SlugField(max_length=200,
        unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super(CategoryManager,
            self).get_queryset()\
                .all()

class Product(models.Model):
    category = models.ForeignKey(Category,
        related_name='products',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='images',blank=True)
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width:60px; height:60px;" />' % self.image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    description = RichTextUploadingField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    stock = models.IntegerField(null=True, blank=True, default=0)
    available = models.BooleanField(default=True)
    stock_managed = models.BooleanField(default=True)
    stock_alert = models.IntegerField(null=True, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=200, db_index=True, blank=True, null=True,)
    barcode = models.PositiveIntegerField(blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('name','cost','price','stock')

    index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    @property
    def cart_profit(self):
        return self.price - self.cost

    objects = models.Manager()  # The default manager.
    cats = CategoryManager()  # Our custom manager

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images',)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


