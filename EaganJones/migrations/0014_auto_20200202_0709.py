# Generated by Django 2.2.4 on 2020-02-02 12:09

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('EaganJones', '0013_auto_20200202_0206'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DatafileModel',
        ),
        migrations.DeleteModel(
            name='Jsonf',
        ),
        migrations.RemoveField(
            model_name='companies',
            name='pd_dataframe',
        ),
        migrations.AddField(
            model_name='companies',
            name='json_data',
            field=jsonfield.fields.JSONField(default=dict),
        ),
        migrations.DeleteModel(
            name='MyModel',
        ),
    ]
