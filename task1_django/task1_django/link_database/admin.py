from django.contrib import admin
from .models import University, Student

#Создаем специальный класс, в котором можно указывать различные параметры работы с моделью через панель администратора
class UniversityAdmin(admin.ModelAdmin):
    #Данная переменная указывает на поля, которые будут выводится в списке продуктов
    list_display = ('id', 'full_name', 'short_name', "foundation_date")

#Регистрируем наш созданный класс как ответственный за работу с моделью Product в панели администратора
admin.site.register(University, UniversityAdmin)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'FIO', "born_date", "get_in_year", "university")

admin.site.register(Student, StudentAdmin)
