from django.urls import path

from app_posts import views

urlpatterns = [
    path('id<int:id_post>/', views.PostPage.as_view(), name='post page'),
    path('list-<int:page_num>/', views.PostsList.as_view(), name='posts list'),
    path('add-post/', views.CreatePost.as_view(), name='create post'),
]
