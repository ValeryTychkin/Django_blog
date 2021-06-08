from django.contrib import admin

from app_posts import models


class PhotoInLine(admin.TabularInline):
    model = models.PhotoToPost


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author_profile', 'short_text']
    inlines = [PhotoInLine]
