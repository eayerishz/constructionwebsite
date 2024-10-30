from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area_size = models.FloatField()
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')

class ProjectElement(models.Model):
    project = models.ForeignKey(Project, related_name='elements', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

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