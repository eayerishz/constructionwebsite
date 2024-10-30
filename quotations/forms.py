from django import forms
from django.contrib.auth.models import User
from .models import Project, Material, ProjectElement

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'startDate', 'endDate']

class ProjectElementForm(forms.ModelForm):
    class Meta:
        model = ProjectElement
        fields = ['project', 'createdAt', 'updatedAt']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description', 'unit']
