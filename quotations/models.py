from django.db import models
from django.contrib.auth.models import User  # Import the User model
import datetime

class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')  # ForeignKey to User
    status = models.CharField(max_length=20, default="pending", blank=True, null=True)
    def __str__(self):
        return self.name


class ProjectElement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Changed to snake_case
    updated_at = models.DateTimeField(auto_now=True)  # Changed to snake_case

    def __str__(self):
        return f"Element of {self.project.name}"


class Material(models.Model):
    element = models.ForeignKey(ProjectElement, related_name='materials', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qty = models.FloatField()
    unit = models.CharField(max_length=50)
    price_per_qty = models.FloatField()
    markup_percentage = models.FloatField()

    @property
    def total_cost(self):
        return self.qty * self.price_per_qty * (1 + self.markup_percentage / 100)

    def __str__(self):
        return self.name