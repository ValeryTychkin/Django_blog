from django.shortcuts import render
from django.views import View

from app_posts.views_str_render import TableMiniPosts
from app_users.views_str_render import TableMiniUsers


class HomePage(View):
    title = 'Главная страница'

    def get(self, request):
        context = {
            'title': self.title,
            'mini_posts': TableMiniPosts().get_html_str(),
            'mini_users': TableMiniUsers().get_html_str()
        }
        return render(request, 'app_home/home_page.html', context)
