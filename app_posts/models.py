import os
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone

from app_users.models import Profile


def update_like(obj_post, user_profile, remove_like=False):
    """
        Обновляет лайк у поста и автора поста, помечает какой пользователь поставил лайк
    :param obj_post: Объект модели поста
    :param user_profile: Объект модели
    :param remove_like: Убрать ли лайк
    """
    if not remove_like:
        Like.objects.create(post=obj_post, user_profile=user_profile)
    else:
        Like.objects.get(post=obj_post, user_profile=user_profile).delete()
    obj_post.like_counter = Like.objects.filter(post_id=obj_post).count()
    obj_post.save()
    obj_post.author_profile.like_counter = Post.objects.filter(author_profile=obj_post.author_profile) \
        .aggregate(sum=models.Sum('like_counter'))['sum']
    obj_post.author_profile.save()


class Post(models.Model):
    text = models.TextField(max_length=10000)
    publication_date = models.DateField(default=timezone.now)
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like_counter = models.IntegerField(default=0)

    @property
    def short_text(self):
        return truncatechars(self.text, 50)

    @property
    def card_text(self):
        return truncatechars(self.text, 100)


def get_upload_path_photo(instance, filename):
    """
    :return: Путь и имя фотографии для поста
        /app_post/posts/post_{id поста}/{номер фотографии}.{формат фотографии}
    """
    num_ph = PhotoToPost.objects.filter(post_id=instance.post).count()
    ext = filename.split('.')[-1]
    return os.path.join(
        f'app_posts/posts/post_{instance.post.id}/',  # path
        f'{num_ph + 1}.{ext}'  # filename
    )


class PhotoToPost(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_upload_path_photo)


class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


def get_upload_path_csv(instance, filename):
    """
        :return: Путь и имя файла CSV с постами
            /app_posts/users_csv/user_{id отправителя}/{дата и время сохранения}.csv
        """
    return os.path.join(
        f'app_posts/users_csv/user_{instance.user_profile.id}/',  # path
        f'{datetime.now()}.csv'  # filename
    )


class CsvModel(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to=get_upload_path_csv)
