# Generated by Django 2.2.4 on 2020-01-19 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0008_productimage'),
        ('home', '0002_auto_20200112_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField(max_length=255)),
                ('status', models.IntegerField(choices=[(1, 'True'), (2, 'False')], default=0)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
