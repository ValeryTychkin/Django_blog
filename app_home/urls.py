from django.urls import path

from app_home import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home page'),
]