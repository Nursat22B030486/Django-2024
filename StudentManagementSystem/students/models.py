from django.db import models
from users.models import User 

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    registration_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name