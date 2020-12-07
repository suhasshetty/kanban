from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Category, Task
from datetime import datetime

# Create your views here.


@login_required(login_url='/login/')
def index(request):
    tasks={}
    categories = Category.objects.all()
    for category in categories:
        tasks[category.name] = Task.objects.filter(category=category)
    template = loader.get_template('tasks/index.html')
    context = {
        'categories': categories,
        'tasks': tasks,
        'user': request.user
    }
    return render(request, 'tasks/index.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'tasks/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('index')
    return render(request,'tasks/register.html')

@login_required(login_url='/login/')
def details(request,task_id):
    details = Task.objects.get(pk=task_id)
    context = {
        'details' : details,
    }
    return render(request, 'tasks/details.html', context)

@login_required(login_url='/login/')
def create(request,category):
    form = TaskForm(request.POST)
    print(form.is_valid())
    if form.is_valid():
        task = form.save(commit=False)
        task.category = Category.objects.get(name=category)
        task.creator = request.user
        task.created_date = datetime.now()
        task.updated_date = datetime.now()
        task.save()
        return redirect('index')

    context = {'form': form}
    return render(request, 'tasks/create.html', context)

@login_required(login_url='/login/')
def edit(request,task_id):
    task_obj = Task.objects.get(pk=task_id)
    form = TaskForm(request.POST, instance=task_obj)
    if form.is_valid():
        task = form.save(commit=False)
        task.updated_date = datetime.now()
        task.save()
        return redirect('index')
    # form = TaskForm(initial = {'title': task_obj.title, 'content':task_obj.content, 'category':task_obj.category}),
    context = {'form': form, 'id': task_id}
    return render(request, 'tasks/edit.html', context)

@login_required(login_url='/login/')
def delete(request,task_id):
    Task.objects.get(pk=task_id).delete()
    return redirect('index')

@login_required(login_url='/login/')
def add_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        category = form.save(commit=False)
        category.save()
        return redirect('index')

    context = {'form': form}
    return render(request, 'tasks/category.html', context)