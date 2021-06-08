import os
from io import BytesIO

from PIL import Image

from django.conf import settings

from django.contrib.auth.models import Group
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from app_users.validations import max_file_size_avatar


def get_upload_path_avatar(instance, filename):
    """
    :return: Путь и имя аватарки пользователя
        /app_users/user_{id пользователя}/avatar.jpg
    """
    return os.path.join(
        f'app_users/user_{instance.user.id}/',  # path
        f'avatar.jpg'  # filename
    )


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.CharField(max_length=1500, blank=True)
    avatar = models.ImageField(validators=[max_file_size_avatar],
                               upload_to=get_upload_path_avatar,
                               default='../static/img/app_users/user.png')
    like_counter = models.IntegerField(default=0)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        """
            Если создается пользователь не через /app_users/full_size/sign_up.html
            то автоматически создается Profile данного пользователя
        """
        if created:
            Profile.objects.create(user=instance)

    @staticmethod
    def crop_square_center(obj_image):
        """
            Обрезка фотографии под соотношений 1x1
        :param obj_image: Объект фотографии
        :return: Обрезанную фотографию
        """
        img = Image.open(obj_image)
        img_width, img_height = img.size
        if img_width > img_height:
            crop = img_height
        else:
            crop = img_width
        img = img.crop(((img_width - crop) // 2,
                        (img_height - crop) // 2,
                        (img_width + crop) // 2,
                        (img_height + crop) // 2))
        img_io = BytesIO()
        img.save(img_io, 'JPEG')  # запись img в RAM память
        return File(img_io, name=obj_image.name)

    def save(self, *args, **kwargs):
        """
            Если у пользователя меняется аватарка, то если предыдущая не default, то она удаляется
            а новая записывается вместо нее
        """
        if not self._state.adding:
            old_avatar = Profile.objects.get(id=self.id).avatar
            if old_avatar != self.avatar:
                if old_avatar.url != '/static/img/app_users/user.png':
                    os.remove(old_avatar.path)
                self.avatar = self.crop_square_center(self.avatar)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
