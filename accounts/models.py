from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from departments.models import Department

class User(AbstractUser):
    STUDENT = 'ST'
    PROFESSOR = 'PR'
    VISITOR = 'VI'
    
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (PROFESSOR, 'Professor'),
        (VISITOR, 'Visitor'),
    ]
    
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=VISITOR,
    )
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    student_id = models.CharField(max_length=20, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_online = models.BooleanField(default=False)

    # Add these to resolve the reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )
    
    
    def __str__(self):
        return self.username

class Application(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    intended_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    application_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.intended_department}"