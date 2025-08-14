from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.postgres.indexes import GinIndex
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('admin', 'Admin'),  
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    phone = models.CharField(max_length=20, unique=True)
    avatar = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)   

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.username} - {self.role}"


class Course(models.Model):
    CHOOSE_LEVEL= (
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="course/thumbnails/", blank=True, null=True)
    code = models.CharField(max_length=20, unique=True) 
    level = models.CharField(max_length=50,choices=CHOOSE_LEVEL,default='beginner')
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="courses_created")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']
        unique_together = ('course', 'position')

    def save(self, *args, **kwargs ):
        if not self.slug:
            self.slug=f"module/{uuid.uuid4().hex[:20]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    position = models.PositiveIntegerField(default=0)
    resources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position']

class Enrollment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=(('student','student'),('auditor','auditor')))
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'course')


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='created_assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='submissions')
    content = models.JSONField(default=dict)  
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    grader = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='graded_submissions')

    class Meta:
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['assignment']),
        ]


# class Quiz(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
#     title = models.CharField(max_length=200)
#     pass_mark = models.IntegerField(default=50)
#     time_limit_seconds = models.PositiveIntegerField(null=True, blank=True)
#     created_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)    


# class Question(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
#     text = models.TextField()
#     metadata = models.JSONField(default=dict, blank=True)
#     weight = models.FloatField(default=1.0)
#     created_at = models.DateTimeField(auto_now_add=True)  
#     updated_at = models.DateTimeField(auto_now=True)    

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
#     text = models.CharField(max_length=1000)
#     is_correct = models.BooleanField(default=False)

# class Attempt(models.Model):
#     quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
#     student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     started_at = models.DateTimeField(auto_now_add=True)
#     finished_at = models.DateTimeField(null=True, blank=True)
#     score = models.FloatField(null=True, blank=True)
#     answers = models.JSONField(default=dict, blank=True)
#     is_auto_graded = models.BooleanField(default=True)

#     class Meta:
#         indexes = [models.Index(fields=['student']), GinIndex(fields=['answers'])]



