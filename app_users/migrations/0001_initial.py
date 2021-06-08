# Generated by Django 2.2 on 2021-06-01 21:23

import app_users.models
import app_users.validations
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(blank=True, max_length=1500)),
                ('avatar', models.ImageField(default='../static/img/app_users/user.png', upload_to=app_users.models.get_upload_path_avatar, validators=[app_users.validations.max_file_size_avatar])),
                ('like_counter', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]