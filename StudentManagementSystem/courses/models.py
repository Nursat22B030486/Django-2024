from django.db import models

from users.models import User
from students.models import Student

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null= True, limit_choices_to={'role': 'Teacher'})

    def __str__(self):
        return f"{self.name} - {self.instructor}"
    
    
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enroll_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self) -> str:
        return f"{self.student} --> {self.course}"  
