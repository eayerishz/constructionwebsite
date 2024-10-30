from django.shortcuts import render, redirect
from .models import Project, ProjectElement, Material
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def create_project(request):
    if request.method == 'POST':
        # Handle project creation logic here
        pass
    return render(request, 'create_project.html')

def project_list(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'project_list.html', {'projects': projects})

def home(request):
    return render(request, 'quotations/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project_list')  # Redirect to the project list after login
    else:
        form = AuthenticationForm()
    return render(request, 'quotations/login.html', {'form': form})