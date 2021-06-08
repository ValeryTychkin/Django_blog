# Generated by Django 2.2 on 2021-06-01 21:23

import app_posts.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('publication_date', models.DateField(default=django.utils.timezone.now)),
                ('like_counter', models.IntegerField(default=0)),
                ('author_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoToPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=app_posts.models.get_upload_path_photo)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_posts.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_posts.Post')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='CsvModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to=app_posts.models.get_upload_path_csv)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_users.Profile')),
            ],
        ),
    ]