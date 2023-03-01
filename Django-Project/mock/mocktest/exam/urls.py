from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('student-exam/', views.student_exam_view, name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view, name='take-exam'),
    path('google-exam/<int:pk>', views.google_exam_view, name='google-exam'),

    path('student-marks', views.student_marks_view, name='student-marks'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),



]
