# Generated by Django 3.0.2 on 2020-03-22 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_orderpmp'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpmp',
            name='total_sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
