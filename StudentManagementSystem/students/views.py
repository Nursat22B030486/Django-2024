from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import  Response
from rest_framework import status
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Student
from users.permissions import IsSelfOrAdmin, IsAdmin, IsTeacher

# Create your views here.
# class StudentCreateAPIView(generics.CreateAPIView):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer
#     permission_classes = [IsAdmin]

#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)

# student_create_view = StudentCreateAPIView.as_view()

class StudentListAPIView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin | IsTeacher]




class StudentDetailAPIView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


student_detail_view = StudentDetailAPIView.as_view()

class StudentUpdateAPIView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'pk'
    permission_classes = [IsSelfOrAdmin]

    

student_update_view = StudentUpdateAPIView.as_view()


class StudentDeleteAPIView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({
                "success": True,
                "message": "Student record deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to delete student record.",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



student_delete_view = StudentDeleteAPIView.as_view()