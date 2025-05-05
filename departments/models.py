from django.db import models
from django.core.validators import FileExtensionValidator



class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='department_logos/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='department_banners/', null=True, blank=True)
    theme_color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    syllabus = models.FileField(
        upload_to='syllabus/',
        validators=[FileExtensionValidator(['pdf'])],
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.code} - {self.name}"