# Generated by Django 2.0.7 on 2018-08-08 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertoire_manager', '0002_piecemodel_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piecemodel',
            name='level',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
