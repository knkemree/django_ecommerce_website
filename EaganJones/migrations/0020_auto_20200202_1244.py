# Generated by Django 2.2.4 on 2020-02-02 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EaganJones', '0019_auto_20200202_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='markettier',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='companies',
            name='sicdescription',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
