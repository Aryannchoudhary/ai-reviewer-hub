from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CodeReview(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    result = models.TextField(blank=True)  # Legacy plain text
    json_review = models.JSONField(default=dict, blank=True)  # Structured review
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.language}"

    def __str__(self):
        return f"{self.user.username} - {self.language}"

class CodeSubmission(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    code = models.TextField()
    review_result = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.language}"    
