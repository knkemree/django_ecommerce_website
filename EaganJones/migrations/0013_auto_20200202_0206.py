# Generated by Django 2.2.4 on 2020-02-02 07:06

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('EaganJones', '0012_auto_20200202_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_json', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.AlterField(
            model_name='companies',
            name='pd_dataframe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EaganJones.MyModel'),
        ),
    ]
