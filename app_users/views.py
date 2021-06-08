from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from app_home.addons_for_views import PageNumsList
from app_users.forms import RegisterForm, LoginForm, UserPageForm
from app_users.models import Profile
from app_users.views_str_render import TableMiniUsers


class UserPage(View):
    def get(self, request, id_user):
        user_obj = Profile.objects.get(user_id=id_user)
        user_form = UserPageForm(initial={'f_name': user_obj.user.first_name,
                                          'l_name': user_obj.user.last_name,
                                          'about': user_obj.about,
                                          })
        context = {
            'user_obj': user_obj,
            'user_form': user_form,
        }
        return render(request, 'app_users/full_size/user_page.html', context)

    def post(self, request, id_user):
        user_change_form = UserPageForm(request.POST, request.FILES)
        if request.user.id == id_user:
            if user_change_form.is_valid():
                # Сохранение изменений в таблицу User
                user = User.objects.get(id=id_user)
                user.first_name = user_change_form.cleaned_data.get('f_name')
                user.last_name = user_change_form.cleaned_data.get('l_name')
                user.save()
                # Сохранение изменений в таблицу Profile
                user_profile = Profile.objects.get(user_id=id_user)
                user_profile.about = user_change_form.cleaned_data.get('about')
                if user_change_form.cleaned_data.get('avatar'):
                    user_profile.avatar = user_change_form.cleaned_data.get('avatar')
                user_profile.save()

        return redirect('user', id_user)


class UsersList(View):
    def get(self, request, page_num):
        users_profiles_list = PageNumsList(page_num=page_num,
                                           num_objs=8,
                                           model_objs=Profile.objects.all())
        context = {
            'title': 'Список Постов',
            'page_num': page_num,
            'page_nums_list': users_profiles_list.get_page_num_list(),
            'mini_users_list': TableMiniUsers(
                profile_objects=users_profiles_list.get_model_objs_list('-id')
            ).get_html_str()
        }
        return render(request, 'app_users/users_list.html', context)


class RegisterPage(View):
    def get(self, request):
        context = {
            'register_form': RegisterForm()
        }
        return render(request, 'app_users/full_size/sign_up.html', context)

    def post(self, request):
        user_reg_form = RegisterForm(request.POST, request.FILES)
        if user_reg_form.is_valid():
            user = user_reg_form.save()
            user_profile = Profile.objects.get(user_id=user.id)
            user_profile.about = user_reg_form.cleaned_data.get('about')
            if user_reg_form.cleaned_data.get('avatar'):
                user_profile.avatar = user_reg_form.cleaned_data.get('avatar')
            user_profile.save()
            username = user_reg_form.cleaned_data.get('username')
            raw_password = user_reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home page')
        else:
            context = {
                'register_form': user_reg_form
            }
            return render(request, 'app_users/full_size/sign_up.html', context)


class LoginInOut(View):
    """
        Происходит  верификация пользователей. В зависимости от post['action']: «login» или «logout»
    """
    def post(self, request):
        if request.POST['action'] == 'login':
            user_form = LoginForm(request.POST)
            if user_form.is_valid():
                username = user_form.cleaned_data['username']
                password = user_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect(request.META.get('HTTP_REFERER'))
                    else:
                        messages.error(request, 'Данная запись не активна')
                else:
                    messages.error(request, 'Логин или Пароль введены не верно')
                return redirect(request.META.get('HTTP_REFERER'))
        elif request.POST['action'] == 'logout':
            logout(request)
            return redirect(request.META.get('HTTP_REFERER'))
