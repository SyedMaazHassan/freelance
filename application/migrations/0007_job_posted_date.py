# Generated by Django 3.1.2 on 2020-12-01 00:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='posted_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 30, 16, 21, 50, 235562)),
        ),
    ]