from django.db import models
from students.models import Student
from courses.models import Course

# Create your models here.
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late') 
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Absent")

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self) -> str:   
        return f"{self.student.name} - {self.course.name} - {self.status}"  