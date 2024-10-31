from django import forms
from django.contrib.auth.models import User
from .models import Project, Material, ProjectElement

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'end_date', 'user', 'status']  # Changed to snake_case

class ProjectElementForm(forms.ModelForm):
    class Meta:
        model = ProjectElement
        exclude = ['created_at', 'updated_at']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ['created_at', 'updated_at']

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Project  # Ensure this is the correct model
        fields = ['name', 'start_date', 'end_date']  # Update fields based on the actual model
