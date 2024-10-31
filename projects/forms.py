from django import forms
from .models import Project, Material

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'submitted_by', 'status', 'global_markup']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'markup_percentage','price', 'quantity']