from django.urls import path
from app_users import views

urlpatterns = [
    path('sign-up/', views.RegisterPage.as_view(), name='sign-up'),
    path('log-in-out/', views.LoginInOut.as_view(), name='log-in/out process'),
    path('id<int:id_user>/', views.UserPage.as_view(), name='user'),
    path('list-<int:page_num>/', views.UsersList.as_view(), name='users list'),
]
