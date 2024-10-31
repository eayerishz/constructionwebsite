from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Material
from .forms import ProjectForm, MaterialForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def admin_dashboard(request):
    pending_projects = Project.objects.filter(status='pending')
    approved_projects = Project.objects.filter(status='approved')
    declined_projects = Project.objects.filter(status='declined')
    completed_projects = Project.objects.filter(status='completed')

    context = {
        'pending_projects': pending_projects,
        'approved_projects': approved_projects,
        'declined_projects': declined_projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'projects/admin_dashboard.html', context)

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('admin_dashboard')

    else:
        project_form = ProjectForm(instance=project)

    materials = project.materials.all()
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'project_form': project_form,
        'materials': materials,
        'material_form': MaterialForm(),
    })

def update_material(request, material_id):
    if request.method == 'POST':
        material = get_object_or_404(Material, id=material_id)
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'total_cost': material.total_cost})

    return JsonResponse({'success': False})

def add_material(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        material_form = MaterialForm(request.POST)
        if material_form.is_valid():
            material = material_form.save(commit=False)
            material.project = project
            material.save()
            return redirect('project_detail', project_id=project.id)

    return redirect('project_detail', project_id=project.id)

def remove_material(request, project_id, material_id):
    project = get_object_or_404(Project, id=project_id)
    material = get_object_or_404(Material, id=material_id)
    material.delete()
    return JsonResponse({'success': True})

@login_required
def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.is_staff:  # Admin can approve
        project.status = 'approved_by_admin'
        project.save()
        return redirect('admin_dashboard')
    return JsonResponse({'success': False})

@login_required
def user_approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.is_authenticated:  # User can approve
        project.status = 'approved_by_user'
        project.save()
        return redirect('project_detail', project_id=project.id)
    return JsonResponse({'success': False})

@login_required
def decline_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.is_authenticated:  # User can decline
        project.status = 'declined'
        project.save()
        return redirect('project_detail', project_id=project.id)
    return JsonResponse({'success': False})

@login_required
def complete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.is_staff and project.status == 'approved_by_user':
        project.status = 'completed'
        project.save()
        return redirect('admin_dashboard')
    return JsonResponse({'success': False})