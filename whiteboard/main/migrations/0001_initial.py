# Generated by Django 4.0.6 on 2022-10-10 11:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnonymousParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 36, 423539))),
                ('permission', models.IntegerField(choices=[(1, 'Owner'), (2, 'Admin'), (3, 'Writer'), (4, 'Reader')], default=4)),
            ],
        ),
        migrations.CreateModel(
            name='AnonymousUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('creation_date', models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 36, 422540))),
                ('anonymous_users', models.ManyToManyField(related_name='boards', through='main.AnonymousParticipation', to='main.anonymoususer')),
            ],
        ),
        migrations.CreateModel(
            name='UserParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(default=datetime.datetime(2022, 10, 10, 13, 36, 36, 423539))),
                ('permission', models.IntegerField(choices=[(1, 'Owner'), (2, 'Admin'), (3, 'Writer'), (4, 'Reader')], default=4)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'board')},
            },
        ),
        migrations.AddField(
            model_name='board',
            name='users',
            field=models.ManyToManyField(related_name='boards', through='main.UserParticipation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='anonymousparticipation',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.board'),
        ),
        migrations.AddField(
            model_name='anonymousparticipation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.anonymoususer'),
        ),
        migrations.AlterUniqueTogether(
            name='anonymousparticipation',
            unique_together={('user', 'board')},
        ),
    ]
