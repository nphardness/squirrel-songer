# Generated by Django 2.0.7 on 2018-08-12 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repertoire_manager', '0003_auto_20180808_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piecemodel',
            name='status',
            field=models.CharField(choices=[('NEW', 'new'), ('PROGRESS', 'in progress'), ('INACTIVE', 'inactive'), ('REJECTED', 'rejected'), ('DONE', 'done')], default='NEW', max_length=32),
        ),
    ]
