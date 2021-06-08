from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html

from app_users import models


class ProfileInline(admin.StackedInline):
    model = models.Profile


class CustomUserAdmin(UserAdmin):
    list_display = ('obj_avatar_img',
                    'username',
                    'first_name',
                    'last_name',
                    'obj_like_counter',
                    'date_joined'
                    )
    inlines = [ProfileInline]

    @staticmethod
    def obj_avatar_img(obj):
        return format_html(f'<img src="{obj.profile.avatar.url}" width="{70}" height="{70}" />')

    @staticmethod
    def obj_like_counter(obj):
        return obj.profile.like_counter


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
