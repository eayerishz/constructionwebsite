from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectElement, Material
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import QuotationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Project

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

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

def home(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
    else:
        projects = Project.objects.none()
    return render(request, 'quotations/home.html', {'projects': projects})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project_list')
        else:
            # Add an error message here if desired
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'quotations/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_project(request):
    if request.method == 'POST':
        area_size = request.POST.get('area_size')
        project_element = request.POST.get('projectElement')
        material = request.POST.get('material')

        # Create a new Project instance with the logged-in user
        project = Project(
            name=f"Project for {request.user.username}",  # Customize this as needed
            status='Pending',  # Set status to 'Pending'
            start_date=datetime.date.today(),  # Ensure the field name matches your model
            end_date=None,  # Adjust based on your requirements
            user=request.user  # Set the user field to the current user
        )
        project.save()

        # Process the quotation data as needed
        print(f"Area Size: {area_size}, Element: {project_element}, Material: {material}")

        return redirect('project_list')  # Redirect to project list after saving

    form = QuotationForm()  # If you have a form to show on GET
    return render(request, 'create_project.html', {'form': form})

def project_list(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
    else:
        projects = Project.objects.none()  # Return an empty queryset if not authenticated
    return render(request, 'project_list.html', {'projects': projects})

@staff_member_required
def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = 'Approved'  # Set the project status to Approved
    project.save()
    return redirect('project_list')  # Redirect to project list view