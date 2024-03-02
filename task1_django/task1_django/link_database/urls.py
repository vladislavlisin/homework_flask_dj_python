from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    #Вызовет views.index при открытии главной страницы сайта
    path('', views.index, name="home"),

    #Вызовет views.about при /about
    path('about', views.about, name="home"),


    #При использовании параметров функции-представления, параметры указываются в системе маршрутизации
    path('student_list/<int:student_id>', views.student),
    path('university_list/<int:university>', views.university),

    path('add_university/', views.add_university),
    path('add_student/', views.add_student),

    path('university_list', views.university_list),
    path('student_list', views.student_list),

    path('delete_student/<int:student_id>', views.delete_student),
    path('delete_university/<int:university>', views.delete_university),

    path('student_list/<int:pk>/update', views.UpdateStudentView.as_view()),
    path('university_list/<int:pk>/update', views.UpdateUniversityView.as_view()),
    ]


