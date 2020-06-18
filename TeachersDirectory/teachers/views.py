from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TeacherForm
from .models import Teacher
from django.contrib import messages
import pandas as pd
import csv
from io import StringIO
import os
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from TeachersDirectory import settings


def index(request):
    teachers_list = []
    name = request.GET.get('name') if request.GET.get('name') else ""
    subject = request.GET.get('subject') if request.GET.get('subject') else ""

    teachers_list = Teacher.objects.filter(Q(subjects__icontains=subject),
                                             last_name__startswith=name)

    return render(request, 'teachers/index.html', {"teachers": teachers_list, 'name': name, 'subject': subject})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            messages.error(request, ('Invalid login details given!'))
            return HttpResponseRedirect(request.path_info)

    else:
        return render(request, 'users/login.html', {})


def signup(request):
    if request.method == 'POST':

        post_values = request.POST.copy()
        form = UserCreationForm(post_values)

        if form.is_valid():
            form.save()
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user_name, password=password)
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required(login_url="/login")
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login')


def add(request):
    if request.method == 'POST':

        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
            messages.error(request, form.errors)
            return render(request, 'teachers/add.html', {'form': form})

    else:
        form = TeacherForm
        return render(request, 'teachers/add.html', {'form': form})


def show(request):
    teacher = None
    try:
        teacher_id = request.GET.get('id')
        teacher = Teacher.objects.get(pk=teacher_id)
    except Exception as e:
        messages.error(request, (e.__str__()))

    return render(request, 'teachers/show.html', {'teacher': teacher})


def edit(request):
    teacher = None
    try:
        if request.method == 'POST':

            try:
                teacher = get_object_or_404(Teacher, pk=request.POST.get('id'))

            except:
                teacher = None

            form = TeacherForm(request.POST, request.FILES, instance=teacher)

            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                messages.error(request, form.errors)
                return render(request, 'teachers/edit.html', {'teacher': teacher})
        else:

            if request.GET.get('id'):
                teacher_id = request.GET.get('id')
                teacher = Teacher.objects.get(pk=teacher_id)

    except Exception as e:
        messages.error(request, (e.__str__()))

    return render(request, 'teachers/edit.html', {'teacher': teacher})


def delete(request):
    try:
        teacher = Teacher.objects.get(pk=request.POST.get('id'))
        if teacher.profile_picture:
            if os.path.isfile(os.path.join(settings.MEDIA_ROOT, teacher.profile_picture.name)):
                os.remove(os.path.join(settings.MEDIA_ROOT, teacher.profile_picture.name))
        teacher.delete()
    except Exception as e:
        messages.error("Error on deleting the item.")

    return HttpResponseRedirect('/')


@login_required(login_url="/login")
def file_import(request):

    try:
        file = request.FILES

        files = file.getlist('file_upload')
        _csv = list(filter(lambda x: x.name == "Teachers.csv", files))
        # df = pd.DataFrame(item)

        if len(_csv) > 0:
            file = _csv[0].read().decode('utf-8')

            csv_data = csv.reader(StringIO(file), delimiter=',')
            objs = []

            csv_data = iter(csv_data)
            next(csv_data)

            for row in csv_data:
                if row[0] and row[3]:
                    subject = ""
                    _image_file = []
                    if row[6]:
                        subject = row[6].lower().replace(" ", "")
                        subject = subject.split(',')[:5]
                        subject = ','.join(subject)
                    if row[2] is not None:
                        _image_file = list(filter(lambda x: x.name == row[2], files))
                    obj = Teacher(
                            first_name=row[0],
                            last_name=row[1] if row[1] else "",
                            profile_picture=row[2] if len(_image_file) > 0 else None,
                            email_address=row[3],
                            phone_number=row[4],
                            room_number=row[5] if row[5] else "",
                            subjects=subject
                        )

                    if len(_image_file) > 0:
                        obj.profile_picture.save(
                            os.path.splitext(_image_file[0].name)[1],
                            ContentFile(_image_file[0].read()),
                            save=False,
                        )

                    objs.append(obj)

            if len(objs) > 0:
                Teacher.objects.bulk_create(objs, ignore_conflicts=True)

        else:
            messages.error("Uploaded folder should contain a Teachers.csv and a sub folder containing teachers' profile pictures.")
    except Exception as e:
        messages.error("Error uploading data")

    return HttpResponseRedirect('/')