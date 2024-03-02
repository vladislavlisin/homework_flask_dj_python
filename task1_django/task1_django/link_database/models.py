from django.db import models

class University(models.Model):
    #verbose_name отвечает за то, как поле будет называться на страницах
    full_name = models.TextField(verbose_name="Полное название", max_length=20)
    short_name = models.CharField(verbose_name="Сокращенное название", max_length=20)
    foundation_date = models.DateField(verbose_name="Дата основания")

    #Переопределение метода str() нужно для того, чтобы вместо Company object(id) писалось просто название компании
    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return "/link_database/university_list"

# ФИО
# Дата рождения
# Университет(только из списка университетов, содержащихся в базе)
# Год поступления
class Student(models.Model):
    FIO = models.TextField(verbose_name = "ФИО")
    born_date = models.DateField(verbose_name = "Дата рождения")
    get_in_year = models.DateField(verbose_name = "Год поступления")
    university = models.ForeignKey(University, on_delete = models.CASCADE, verbose_name = "Университет")

    def __str__(self):
        return f"{self.FIO}_{self.born_date}"

    def get_absolute_url(self):
        return "/link_database/student_list"