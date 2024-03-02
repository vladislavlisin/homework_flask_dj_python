from django.shortcuts import render
from . import forms
from . import models
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views.generic import UpdateView


def index(request):
    return TemplateResponse(request, "index.html")

# Вернет текст "About"
def about(request):
    return HttpResponse('Домашнее задание Django')


######################################################################################################################
#                                                    STUDENT                                                         #
######################################################################################################################

def student(request, student_id):
    try:
        curr_student = models.Student.objects.get(id=student_id)
        data = {"FIO": curr_student.FIO,
                "born_date" : curr_student.born_date,
                "get_in_year": curr_student.get_in_year,
                "university": curr_student.university,
                "student_id": student_id,
                "href": f"/link_database/student_list/{student_id}/update"}

        return TemplateResponse(request, "student.html", data)
    except models.Student.DoesNotExist:
        return HttpResponseNotFound("Студента с таким id не существует")

def add_student(request):

    if request.method == "POST":

        userform = forms.StudentForm(request.POST)
        if userform.is_valid():
            FIO = request.POST.get("FIO")
            born_date = request.POST.get("born_date")
            get_in_year = request.POST.get("get_in_year")

            university_id = request.POST.get("university")
            try:
                university = models.University.objects.get(id=university_id)
            except models.University.DoesNotExist:
                return HttpResponse("Недействительный ID университета")

            # Добавляем студента в базу данных
            student = models.Student.objects.create(FIO=FIO,
                                                    born_date=born_date,
                                                    get_in_year=get_in_year,
                                                    university=university
                                                    )
            # Получаем id добавленного для того, чтобы перейти на его страницу
            new_id = student.id
            return HttpResponseRedirect(f"/link_database/student_list/{new_id}")
        else:
            return HttpResponse("Invalid data")
    else:
        form = forms.StudentForm()
        data = {"form": form}
        return render(request, "add_student.html", data)

class UpdateStudentView(UpdateView):
    model = models.Student

    template_name = "add_student.html"
    form_class = forms.StudentForm

def student_list(request):
    #Получаем все продукты из базы
    all_students = models.Student.objects.all()
    data = {"students": all_students}
    return TemplateResponse(request, "student_list.html", data)

def delete_student(request, student_id):
    try:
        student = models.Student.objects.get(id=student_id)
        student.delete()
        return HttpResponseRedirect("/link_database/student_list")
    except models.Student.DoesNotExist:
        return HttpResponseNotFound("Студента с таким id не существует")

######################################################################################################################
#                                                 UNIVERSITY                                                         #
######################################################################################################################

def university(request, university):
    try:
        curr_university = models.University.objects.get(id=university)
        data = {"full_name": curr_university.full_name,
                "short_name": curr_university.short_name,
                "foundation_date": curr_university.foundation_date,
                "university": university,
                "href": f"/link_database/university_list/{university}/update"}

        return TemplateResponse(request, "university.html", data)
    except models.University.DoesNotExist:
        return HttpResponseNotFound("Университета с таким id не существует")
#
def university_list(request):
    #Получаем все продукты из базы
    all_university = models.University.objects.all()
    data = {"all_university": all_university}
    return TemplateResponse(request, "university_list.html", data)

def add_university(request):
    if request.method == "POST":

        userform = forms.UniversityForm(request.POST)
        if userform.is_valid():

            full_name = request.POST.get("full_name")
            short_name = request.POST.get("short_name")
            foundation_date = request.POST.get("foundation_date")


            #Добавляем продукт в базу данных
            university = models.University.objects.create(full_name = full_name,
                                                          short_name = short_name,
                                                          foundation_date = foundation_date)
            #Получаем id добавленного для того, чтобы перейти на его страницу
            new_id = university.id
            return HttpResponseRedirect(f"/link_database/university_list/{new_id}")
        else:
            return HttpResponse("Invalid data")
    else:
        data = {"form": forms.UniversityForm()}
        return TemplateResponse(request, "add_university.html", data)

def delete_university(request, university):
    try:
        university = models.University.objects.get(id=university)
        university.delete()
        return HttpResponseRedirect("/link_database/university_list")
    except models.University.DoesNotExist:
        return HttpResponseNotFound("Университета с таким id не существует")

class UpdateUniversityView(UpdateView):
    model = models.University

    template_name = "add_university.html"
    form_class = forms.UniversityForm