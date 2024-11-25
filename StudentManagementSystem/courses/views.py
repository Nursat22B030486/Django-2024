from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .models import Course, Enrollment
from .serializers import CourseSerializer , EnrollmentSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent
from students.models import Student

# Create your views here.
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdmin] 

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk' 
    

class CourseUpdateAPIView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdmin] 
    lookup_field = 'pk' 

class CourseDeleteAPIView(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdmin]


class EnrollmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        
        if user.role == "Student":
            try:
                student = Student.objects.get(user=user)
                return Enrollment.objects.filter(student=student)
            except Student.DoesNotExist:
                raise NotFound("Student profile does not exist.")
            except Enrollment.DoesNotExist:
                return Enrollment.objects.none()
        elif user.role == "Teacher":
            return Enrollment.objects.filter(course__instructor=user)
        else:
            return Enrollment.objects.all()
        
    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in ['Admin', 'Teacher']:
            raise PermissionDenied("You do not have permission to create enrollment.")
        
        student = serializer.validated_data.get('student')
        course = serializer.validated_data.get('course')

        if not Student.objects.filter(id=student.id).exists():
            raise ValidationError("The student does not exist.")
        if not Course.objects.filter(id=course.id).exists():
            raise ValidationError("The course does not exist.")

        serializer.save()


    # def perform_create(self, serializer):
    #     user = self.request.user
        
    #     if user.role != 'Student':
    #         raise PermissionDenied("Only students can enroll in courses.")
        
    #     student = Student.objects.get(user=user)
      
    #     # Get the course from the request data
    #     course_id = self.request.data.get('course')
        
    #     try:
    #         course = Course.objects.get(id=course_id)
    #     except Course.DoesNotExist:
    #         raise ValidationError("Course does not exist.")

    #     # Check if the student is already enrolled in the course
    #     if Enrollment.objects.filter(student=student, course=course).exists():
    #         raise ValidationError("You are already enrolled in this course.")

    #     # Save the enrollment with the associated student and course
    #     serializer.save(student=student, course=course)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class EnrollmentDetailAPIView(generics.RetrieveAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        enrollment_id = self.kwargs.get(self.lookup_field)

        if user.role == "Student":
            try:
                student = Student.objects.get(user=user)
                return Enrollment.objects.get(id=enrollment_id, student=student)
            except Enrollment.DoesNotExist:
                raise PermissionDenied("You do not have permission to access this enrollment.")
        elif user.role == "Teacher":
            try:
                return Enrollment.objects.get(id=enrollment_id, course__instructor=user)
            except Enrollment.DoesNotExist:
                raise PermissionDenied("You do not have permission to access this enrollment.")
        else:
            try:
                return Enrollment.objects.get(id=enrollment_id)
            except Enrollment.DoesNotExist:
                return NotFound("Enrollment not found")

class EnrollmentDeleteAPIView(generics.DestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)




