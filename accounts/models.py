from django.db import models

# Create your models here.
#User Model

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    ROLE_CHOICES = (
        ('trainer', 'Trainer'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username

#trainer profile

class TrainerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Student profile

class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    admission_number = models.CharField(max_length=50)
    course = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

