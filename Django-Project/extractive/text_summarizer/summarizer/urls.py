from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('after-login/', views.after_login, name='after_login'),

    path('text-input/', views.text_input, name='text_input'),
    path('file-input/', views.file_input, name='file_input'),


    path('text-output/', views.text_output, name='text_output'),
    path('file-output/', views.file_output, name='file_output'),


    path('download/', views.download_text_file, name='download'),



    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

]