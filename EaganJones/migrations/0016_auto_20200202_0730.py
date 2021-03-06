# Generated by Django 2.2.4 on 2020-02-02 12:30

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('EaganJones', '0015_auto_20200202_0721'),
    ]

    operations = [
        migrations.CreateModel(
            name='JsonFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json_data', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.DeleteModel(
            name='Json',
        ),
        migrations.AddField(
            model_name='companies',
            name='json_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='EaganJones.JsonFile'),
        ),
    ]
