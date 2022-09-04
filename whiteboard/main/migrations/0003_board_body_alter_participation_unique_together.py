# Generated by Django 4.0.6 on 2022-09-04 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_clients_participation_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='body',
            field=models.JSONField(null=True),
        ),
        migrations.AlterUniqueTogether(
            name='participation',
            unique_together={('client', 'board')},
        ),
    ]
