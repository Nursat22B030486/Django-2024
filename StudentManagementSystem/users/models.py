from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self) -> str:
        return f'{self.username} - {self.role}'
