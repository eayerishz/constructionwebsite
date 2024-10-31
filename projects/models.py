from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved_by_admin', 'Approved by Admin'),
        ('approved_by_user', 'Approved by User'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    submitted_by = models.CharField(max_length=255)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    global_markup = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Material(models.Model):
    project = models.ForeignKey(Project, related_name='materials', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    markup_percentage = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)  # Base price of the material
    quantity = models.PositiveIntegerField(default=1)  # Quantity of the material

    def __str__(self):
        return self.name

    @property
    def total_cost(self):
        return self.price * self.quantity * (1 + self.markup_percentage / 100)

class ProjectElement(models.Model):
    project = models.ForeignKey(Project, related_name='elements', on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description