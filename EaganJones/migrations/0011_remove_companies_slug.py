# Generated by Django 2.2.4 on 2020-02-02 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EaganJones', '0010_auto_20200201_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companies',
            name='slug',
        ),
    ]
