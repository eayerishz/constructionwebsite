from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuotationForm
from .models import Project, ProjectElement, Material
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
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


@staff_member_required
def admin_dashboard(request):
    pending_projects = Project.objects.filter(status='Pending')
    approved_projects = Project.objects.filter(status='Approved')
    declined_projects = Project.objects.filter(status='Declined')
    completed_projects = Project.objects.filter(status='Completed')

    return render(request, 'admin_dashboard.html', {
        'pending_projects': pending_projects,
        'approved_projects': approved_projects,
        'declined_projects': declined_projects,
        'completed_projects': completed_projects,
    })

@staff_member_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project.name = request.POST.get('name', project.name)
        project.status = request.POST.get('status', project.status)
        project.save()

        # You can implement additional logic to add/remove elements/materials here.

        return redirect('admin_dashboard')

    project_elements = ProjectElement.objects.filter(project=project)
    materials = Material.objects.filter(element__project=project)

    return render(request, 'update_project.html', {
        'project': project,
        'project_elements': project_elements,
        'materials': materials,
    })

@staff_member_required
def remove_project_element(request, element_id):
    element = get_object_or_404(ProjectElement, id=element_id)
    element.delete()
    return JsonResponse({'message': 'Element removed successfully.'})

@staff_member_required
def remove_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return JsonResponse({'message': 'Material removed successfully.'})