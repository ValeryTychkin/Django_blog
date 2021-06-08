from django.core.exceptions import ValidationError


def max_file_size_avatar(value):
    """
        Валидация размера файла аватарки (<2mb)
    """
    filesize = value.size
    if filesize > 2*(1024*2):
        raise ValidationError("Размер файла не должен привышать 2Мбайта")
