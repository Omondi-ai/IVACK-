from django.db import models
from django.contrib.auth import get_user_model
from departments.models import Department, Course

User = get_user_model()

class Post(models.Model):
    GENERAL = 'GE'
    DEPARTMENT = 'DE'
    COURSE = 'CO'
    PROFESSOR = 'PR'
    
    TARGET_CHOICES = [
        (GENERAL, 'General'),
        (DEPARTMENT, 'Department'),
        (COURSE, 'Course'),
        (PROFESSOR, 'Professor'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    target_type = models.CharField(max_length=2, choices=TARGET_CHOICES, default=GENERAL)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                                 related_name='targeted_posts')
    file = models.FileField(upload_to='post_files/', null=True, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']