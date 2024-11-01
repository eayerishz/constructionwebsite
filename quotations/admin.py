from . import models
from django.contrib import admin

# Register your models here.
admin.site.register(models.Material)
admin.site.register(models.Project)
admin.site.register(models.ProjectElement)
