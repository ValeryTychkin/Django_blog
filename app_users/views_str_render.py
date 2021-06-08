from django.template.loader import render_to_string

from app_users import models


class TableMiniUsers:
    """
        Класс хранимый объекты пользователей и html код для отображения миниатюры объекта

        Сортировка при profile_objects=None: Количество лайков по убыванию
    """
    def __init__(self, profile_objects=None):
        if not profile_objects:
            profile_objects = models.Profile.objects.order_by('-like_counter', '-id')[:6]
        else:
            profile_objects = profile_objects
        self.__html_str = self.__html_table(profile_objects)

    @staticmethod
    def __html_table(profile_objects):
        context = {
            'objs_list': profile_objects,
        }
        return render_to_string('app_users/miniature/miniature_user.html', context)

    def get_html_str(self):
        return self.__html_str
