from django.template.loader import render_to_string

from app_posts import models


class PostWithPhotos:
    """
        Класс хранит объект модели поста и информацию:
            Есть ли у поста фото
                Если да -> Какая фотография первая
                      +--> Список всех фотографий

    """
    def __init__(self, post_obj):
        self.__post_obj = post_obj
        self.__checker_photo_post()

    def __checker_photo_post(self):
        if models.PhotoToPost.objects.filter(post_id=self.__post_obj.id).exists():
            self.__check_photo = True
            self.__photos_post_list = models.PhotoToPost.objects.filter(post_id=self.__post_obj.id).order_by('id')
        else:
            self.__check_photo = False

    def obj_model(self):
        return self.__post_obj

    def have_photo(self):
        return self.__check_photo

    def first_photo(self):
        if self.__check_photo:
            return self.__photos_post_list.first().photo
        else:
            return None

    def photos_list(self):
        if self.__check_photo:
            return [(num, self.__photos_post_list[num].photo) for num in range(self.__photos_post_list.count())]
        else:
            return None


class TableMiniPosts:
    """
        Класс хранимый объекты поста и html код для отображения миниатюры объекта

        Сортировка при post_objects=None: 6 объектов по убыванию количество лайков среди последних 8ти постов
    """
    def __init__(self, post_objects=None):
        if not post_objects:
            id_list = models.Post.objects.order_by('-publication_date', '-id').values_list('id', flat=True)[:8]
            self.__posts_obj_list = models.Post.objects.filter(id__in=id_list).order_by('-like_counter',
                                                                                        '-publication_date',
                                                                                        '-id')[:6]
        else:
            self.__posts_obj_list = post_objects
        mini_posts_list = self.__check_photo_post()
        self.__html_str = self.__html_table(mini_posts_list)

    @staticmethod
    def __html_table(mini_posts_list):
        context = {
            'objs_list': mini_posts_list,
        }
        return render_to_string('app_posts/miniature/miniature_post.html', context)

    def __check_photo_post(self):
        posts_n_photos_list = []
        for post in self.__posts_obj_list:
            posts_n_photos_list.append(PostWithPhotos(post))
        return posts_n_photos_list

    def get_html_str(self):
        return self.__html_str
