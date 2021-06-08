import math


class PageNumsList:
    """
        Класс работы над номерами страниц из списка объектов модели

        init:   page_num - Номер необходимой страницы
                num_objs - Необходимое количество объектов на странице
                model_objs - Объекты модели по которой необходимо проводить выборку (model.objects)

        get_model_objs_list: -> Отсортированные объекты для необходимой страницы
                *orders - по данных каких столбцов будет происходить сортировка

        get_page_num_list: -> Список номеров страниц для необходимой страницы
    """
    def __init__(self, page_num: int, num_objs: int, model_objs):
        self.__page_num = page_num
        self.__num_objs = num_objs
        self.__model_objs = model_objs
        self.__create_start_end_nums()
        self.__create_page_num_list()

    def __create_start_end_nums(self):
        self.__start_num = (self.__page_num - 1) * self.__num_objs
        self.__end_num = self.__page_num * self.__num_objs

    def __create_page_num_list(self):
        self.__page_nums_list = [1, 2, 3]
        nums_max_pages = math.ceil(self.__model_objs.count() / self.__num_objs)  # Округляю до большего целого числа
        if self.__page_num != 1:
            self.__page_nums_list = [self.__page_num - 1, self.__page_num, self.__page_num + 1]
            if self.__page_num + 1 > nums_max_pages:
                del self.__page_nums_list[-1]
        elif self.__page_num + 2 > nums_max_pages:
            del self.__page_nums_list[-1]
            if self.__page_num + 1 > nums_max_pages:
                del self.__page_nums_list[-1]

    def get_model_objs_list(self, *orders):
        return self.__model_objs.order_by(*orders)[self.__start_num:self.__end_num]

    def get_page_num_list(self):
        return self.__page_nums_list
