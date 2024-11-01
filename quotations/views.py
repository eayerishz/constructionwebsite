from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuotationForm, ProjectUpdateForm, ProjectElementForm, MaterialForm
from .models import Project, ProjectElement, Material
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime


def is_superuser(user):
    return user.is_superuser


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def project_detail(request, project_id):
    # All users can view project details
    project = get_object_or_404(Project, id=project_id)
    form = None

    if is_superuser(request.user):
        if request.method == "POST":
            form = ProjectUpdateForm(request.POST, instance=project)
            if form.is_valid():
                form.save()
                return redirect("project_list")
        else:
            form = ProjectUpdateForm(instance=project)

    return render(request, "project_detail.html", {"project": project, "form": form})


def home(request):
    # Show all projects to all authenticated users
    projects = (
        Project.objects.all()
        if request.user.is_authenticated
        else Project.objects.none()
    )
    return render(request, "quotations/home.html", {"projects": projects})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("project_list")
        else:
            form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "quotations/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def create_project(request):
    if request.method == "POST":
        area_size = request.POST.get("area_size")
        project_element = request.POST.get("projectElement")
        material = request.POST.get("material")

        project = Project(
            name=f"Project for {request.user.username}",
            status="Pending",
            start_date=datetime.date.today(),
            end_date=None,
            user=request.user,
        )
        project.save()
        print(
            f"Area Size: {area_size}, Element: {project_element}, Material: {material}"
        )

        return redirect("project_list")

    form = QuotationForm()
    return render(request, "create_project.html", {"form": form})


@login_required
def project_list(request):
    projects = {
        "pendings": Project.objects.filter(status="Pending"),
        "approved": Project.objects.filter(status="Approved"),
        "declined": Project.objects.filter(status="Declined"),
        "completed": Project.objects.filter(status="Completed"),
    }
    return render(request, "project_list.html", {"projects": projects})


def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = "Approved"
    project.save()
    return redirect("project_list")


def admin_dashboard(request):
    pending_projects = Project.objects.filter(status="Pending")
    approved_projects = Project.objects.filter(status="Approved")
    declined_projects = Project.objects.filter(status="Declined")
    completed_projects = Project.objects.filter(status="Completed")

    return render(
        request,
        "admin_dashboard.html",
        {
            "pending_projects": pending_projects,
            "approved_projects": approved_projects,
            "declined_projects": declined_projects,
            "completed_projects": completed_projects,
        },
    )


def add_project_element(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = None

    if is_superuser(request.user):
        if request.method == "POST":
            form = ProjectElementForm(request.POST, project=project)
            if form.is_valid():
                element = form.save(commit=False)
                element.project = project
                element.save()
                return redirect("project_list")
        else:
            form = ProjectElementForm(project=project)

    return render(
        request, "add_project_element.html", {"project": project, "form": form}
    )


def add_project_material(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = None

    if is_superuser(request.user):
        if request.method == "POST":
            form = MaterialForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("project_list")
        else:
            form = MaterialForm()

    return render(
        request, "add_project_material.html", {"project": project, "form": form}
    )


@login_required
def update_project(request, project_id):
    # Fetch the project or return a 404 error if not found
    project = get_object_or_404(Project, id=project_id)

    # Handle form submission
    if request.method == "POST":
        project.name = request.POST.get("name", project.name)  # Update project name
        project.status = request.POST.get(
            "status", project.status
        )  # Update project status
        project.save()  # Save changes to the database
        return redirect("project_list")  # Redirect to admin dashboard after saving

    # Fetch related project elements and materials to display in the form
    project_elements = ProjectElement.objects.filter(project=project)
    materials = Material.objects.filter(element__project=project)

    # Render the update form with the current project data
    return render(
        request,
        "update_project.html",
        {
            "project": project,
            "project_elements": project_elements,
            "materials": materials,
        },
    )


def remove_project_element(request, element_id):
    element = get_object_or_404(ProjectElement, id=element_id)
    element.delete()
    return JsonResponse({"message": "Element removed successfully."})


def remove_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return JsonResponse({"message": "Material removed successfully."})
