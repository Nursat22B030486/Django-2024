from django.db import models
from students.models import Student
from courses.models import Course
from users.models import User

# Create your models here.


class Grade (models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'Teacher'})
    grades = models.CharField(max_length=5)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.student.name} - {self.course.name} - {self.grade}"