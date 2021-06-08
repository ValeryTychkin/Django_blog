from datetime import datetime
import pandas as pd

from app_posts.models import Post


class ProcessUploadCsvPosts:
    """
        Класс для обработки приходящих CSV файлов от пользователей
            init:
                file - Файл CSV
                author_profile - Объект профайла отправителя
    """

    def __init__(self, file, author_profile):
        self.__csv_file = file
        self.__author_profile = author_profile
        self.__read_csv()

    def __read_csv(self):
        columns_name = ['text', 'publication_date']
        self.__data_file = pd.read_csv(self.__csv_file, names=columns_name)

    def __add_objs_model(self):
        create_new_posts = False
        for index, row in self.__data_file.iterrows():
            Post.objects.create(
                text=row['text'],
                author_profile=self.__author_profile,
                publication_date=datetime.strptime(row['publication_date'], '%d-%m-%Y').date()
            )
            create_new_posts = True
        return create_new_posts

    def update_model(self):
        return self.__add_objs_model()

