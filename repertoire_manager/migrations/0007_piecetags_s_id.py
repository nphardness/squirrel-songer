# Generated by Django 2.0.7 on 2018-11-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertoire_manager', '0006_auto_20181102_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='piecetags',
            name='s_id',
            field=models.IntegerField(default=-1),
        ),
    ]
