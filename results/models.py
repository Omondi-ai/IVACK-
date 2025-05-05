from django.db import models
from django.contrib.auth import get_user_model
from departments.models import Course

User = get_user_model()

class Assessment(models.Model):
    EXAM = 'EX'
    QUIZ = 'QU'
    ASSIGNMENT = 'AS'
    PROJECT = 'PR'
    
    TYPE_CHOICES = [
        (EXAM, 'Exam'),
        (QUIZ, 'Quiz'),
        (ASSIGNMENT, 'Assignment'),
        (PROJECT, 'Project'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)
    max_score = models.PositiveIntegerField(default=100)
    date_given = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.get_assessment_type_display()}: {self.title}"

class Result(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('assessment', 'student')
    
    def __str__(self):
        return f"{self.student} - {self.assessment}: {self.score}"
    
    def grade(self):
        percentage = (self.score / self.assessment.max_score) * 100
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'