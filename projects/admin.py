from django.contrib import admin
from .models import Project, Material

class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1

def approve_projects(modeladmin, request, queryset):
    queryset.update(status='approved_by_admin')
approve_projects.short_description = "Mark selected projects as approved by admin"

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'submitted_by', 'submission_date', 'status', 'global_markup')
    list_filter = ('status', 'submission_date')
    search_fields = ('name', 'submitted_by')
    actions = [approve_projects]
    inlines = [MaterialInline]

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'markup_percentage', 'total_cost', 'project')
    list_filter = ('project',)
    search_fields = ('name', 'project__name')