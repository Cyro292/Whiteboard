# Generated by Django 4.0.6 on 2022-10-10 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymousparticipation',
            name='join_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 40, 260787)),
        ),
        migrations.AlterField(
            model_name='board',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 40, 260787)),
        ),
        migrations.AlterField(
            model_name='userparticipation',
            name='join_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 40, 260787)),
        ),
    ]
