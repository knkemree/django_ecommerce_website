# Generated by Django 3.0.2 on 2020-01-13 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='status',
        ),
        migrations.AddField(
            model_name='contact',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
